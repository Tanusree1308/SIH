import os
import uuid
from datetime import timedelta, timezone, datetime
import traceback

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from . import database, models, security, services
from .services import analysis_service
from .config import settings

# --- App Initialization ---
app = FastAPI(title="Bovilens API")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static File Serving ---
os.makedirs("backend/uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="backend/uploads"), name="uploads")

# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Bovilens API"}

# --- Authentication Routes ---
@app.post("/auth/register", response_model=models.UserInResponse, status_code=201)
@limiter.limit("5/minute")
async def register_user(user: models.UserCreate, request: Request):
    existing_user = await database.user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = security.get_password_hash(user.password)
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    
    new_user = await database.user_collection.insert_one(user_dict)
    created_user = await database.user_collection.find_one({"_id": new_user.inserted_id})
    return models.UserInResponse.model_validate(created_user)

@app.post("/auth/login", response_model=models.Token)
@limiter.limit("10/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await database.user_collection.find_one({"username": form_data.username})
    if not user or not security.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# --- User Routes ---
@app.get("/users/me", response_model=models.UserInResponse)
async def read_users_me(current_user: models.TokenData = Depends(security.get_current_user)):
    user = await database.user_collection.find_one({"username": current_user.username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return models.UserInResponse.model_validate(user)

@app.put("/users/me", response_model=models.UserInResponse)
async def update_user_me(user_update: models.UserBase, current_user: models.TokenData = Depends(security.get_current_user)):
    user = await database.user_collection.find_one({"username": current_user.username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    if "username" in update_data:
        del update_data["username"]

    await database.user_collection.update_one({"_id": user["_id"]}, {"$set": update_data})
    updated_user = await database.user_collection.find_one({"_id": user["_id"]})
    return models.UserInResponse.model_validate(updated_user)

@app.put("/users/me/password")
async def change_user_password(password_data: models.PasswordChange, current_user: models.TokenData = Depends(security.get_current_user)):
    user = await database.user_collection.find_one({"username": current_user.username})
    if not user or not security.verify_password(password_data.current_password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    hashed_password = security.get_password_hash(password_data.new_password)
    await database.user_collection.update_one({"_id": user["_id"]}, {"$set": {"hashed_password": hashed_password}})
    return {"message": "Password updated successfully"}

# --- Analysis Routes ---
# --- Analysis Routes ---
@app.post("/analysis/", response_model=models.AnalysisResult)
@limiter.limit("15/hour")
async def create_analysis(request: Request, file: UploadFile = File(...), current_user: models.TokenData = Depends(security.get_current_user)):
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"backend/uploads/{unique_filename}"
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        analysis_result = analysis_service.run_full_analysis(file_path)
        if analysis_result is None:
            raise HTTPException(status_code=400, detail="Invalid image: No cattle or buffalo could be detected.")
    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="An unexpected error occurred during analysis.")

    user = await database.user_collection.find_one({"username": current_user.username})
    
    annotated_path = analysis_result["annotated_image_path"]
    annotated_url = annotated_path.replace("backend", "").replace('\\', '/')

    # --- FIX START ---
    # The 'animal_type' field must be included to match the AnalysisResult model
    db_entry = {
        "user_id": str(user["_id"]),
        "animal_type": analysis_result["class_name"],  # Add this line
        "original_image_url": f"/uploads/{unique_filename}",
        "annotated_image_url": annotated_url,
        "overall_score": analysis_result["scores"]["overall_score"],
        "trait_scores": analysis_result["scores"]["trait_scores"],
        "timestamp": datetime.now(timezone.utc)
    }
    # --- FIX END ---
    
    inserted_doc = await database.analysis_collection.insert_one(db_entry)
    created_analysis = await database.analysis_collection.find_one({"_id": inserted_doc.inserted_id})
    return models.AnalysisResult.model_validate(created_analysis)

@app.get("/analysis/history", response_model=list[models.AnalysisResult])
async def get_analysis_history(current_user: models.TokenData = Depends(security.get_current_user)):
    """
    Fetches the 5 most recent analysis results for the currently authenticated user.
    """
    user = await database.user_collection.find_one({"username": current_user.username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Find, sort by newest, and then limit to 5 results
    history_cursor = database.analysis_collection.find(
        {"user_id": str(user["_id"])}
    ).sort("timestamp", -1).limit(5)
    
    # Fetch all items from the limited cursor
    history_list = await history_cursor.to_list(length=None) 
    return [models.AnalysisResult.model_validate(item) for item in history_list]
# ... other routes ...

@app.post("/analysis/", response_model=models.AnalysisResult)
@limiter.limit("15/hour")
async def create_analysis(request: Request, file: UploadFile = File(...), current_user: models.TokenData = Depends(security.get_current_user)):
    # ... (file saving and analysis call logic remains the same) ...
    
    try:
        analysis_result = analysis_service.run_full_analysis(file_path)
        if analysis_result is None:
            raise HTTPException(status_code=400, detail="Invalid image: No cattle or buffalo could be detected.")
    except Exception as e:
        # ... error handling ...

     user = await database.user_collection.find_one({"username": current_user.username})
    
    annotated_path = analysis_result["annotated_image_path"]
    annotated_url = annotated_path.replace("backend", "").replace('\\', '/')

    db_entry = {
        "user_id": str(user["_id"]),
        "animal_type": analysis_result["class_name"],  # <-- CHANGE "animal_type" to "class_name" HERE
        "original_image_url": f"/uploads/{unique_filename}",
        "annotated_image_url": annotated_url,
        "overall_score": analysis_result["scores"]["overall_score"],
        "trait_scores": analysis_result["scores"]["trait_scores"],
        "timestamp": datetime.now(timezone.utc)
    }
    
    # ... (database insertion logic remains the same) ...
    inserted_doc = await database.analysis_collection.insert_one(db_entry)
    created_analysis = await database.analysis_collection.find_one({"_id": inserted_doc.inserted_id})
    return models.AnalysisResult.model_validate(created_analysis)

# ... other routes ...

