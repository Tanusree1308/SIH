import os
import uuid
from datetime import timedelta, timezone, datetime
import traceback
import numpy as np # Import numpy for mock data generation

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

import database, models, security, config
from config import settings
# services.analysis_service is commented out because the class is defined below
# from services.analysis_service import AnalysisService

# --- MOCK Analysis Service (You will replace this) ---
class AnalysisService:
    def __init__(self):
        # In a real project, this is where you would load your models
        # For example: self.model = load_model('path/to/your/model.h5')
        print("✅ AnalysisService initialized.")
        pass

    def run_analysis(self, file_path: str):
        """
        This is the method that was missing. It now contains mock logic
        to simulate your deep learning model's output.

        You will replace the contents of this function with your actual
        YOLOv8, MediaPipe, and measurement/scoring logic.
        """
        # --- REPLACE THIS MOCK LOGIC WITH YOUR REAL CODE ---
        print(f"Simulating analysis for file: {file_path}")

        # 1. Simulate Measurement Calculation
        measurements = {
            "height_at_withers": f"{np.random.randint(120, 180)} cm",
            "body_length": f"{np.random.randint(150, 220)} cm",
            "chest_width": f"{np.random.randint(80, 110)} cm",
            "rump_angle": f"{np.random.randint(5, 25)} degrees"
        }
        
        # 2. Simulate ATC Scores (1-5)
        trait_scores = {
            "trait_1": np.random.randint(1, 6),
            "trait_2": np.random.randint(1, 6),
            "trait_3": np.random.randint(1, 6),
            "trait_4": np.random.randint(1, 6)
        }
        overall_score = sum(trait_scores.values()) / len(trait_scores)
        
        # 3. Simulate an annotated image path (for demonstration)
        # In a real scenario, your model would save an annotated image and return its path
        mock_annotated_path = os.path.join(UPLOADS_DIR, "annotated", "mock_annotated_image.png")
        if not os.path.exists(os.path.dirname(mock_annotated_path)):
            os.makedirs(os.path.dirname(mock_annotated_path))
        # Create a dummy file to avoid errors
        with open(mock_annotated_path, "w") as f:
            f.write("mock content")

        return {
            "animal_type": "Cattle", # A mock prediction
            "overall_score": round(overall_score, 2),
            "trait_scores": trait_scores,
            "annotated_image_path": mock_annotated_path
        }


# --- App Initialization ---
app = FastAPI(title="Bovilens API")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- Middleware ---
origins = [
    "https://bovilens-frontend.onrender.com", # <-- FRONTEND URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Uploads directory and annotated directory setup ---
UPLOADS_DIR = "backend/uploads"
ANNOTATED_DIR = os.path.join(UPLOADS_DIR, "annotated")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(ANNOTATED_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


# --- Global Analysis Service ---
analysis_service = None

@app.on_event("startup")
async def startup_event():
    global analysis_service
    try:
        analysis_service = AnalysisService()
        print("✅ AnalysisService initialized and models loaded.")
    except Exception as e:
        print(f"FATAL: Could not initialize AnalysisService: {e}")
        raise


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
    created_user = await database.user_collection.find_one({"username": user.username})
    return models.UserInResponse.model_validate(created_user)


@app.post("/auth/login", response_model=models.Token)
@limiter.limit("10/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await database.user_collection.find_one({"username": form_data.username})
    if not user or not security.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
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
@app.post("/analysis/", response_model=models.AnalysisResult)
@limiter.limit("15/hour")
async def create_analysis(
    request: Request,
    file: UploadFile = File(...),
    current_user: models.TokenData = Depends(security.get_current_user)
):
    # Save uploaded file
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOADS_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Run analysis
    try:
        if analysis_service is None:
            raise HTTPException(status_code=500, detail="Analysis service not initialized.")
        
        analysis_result = analysis_service.run_analysis(file_path)
        if analysis_result is None:
            raise HTTPException(status_code=400, detail="Invalid image: No cattle or buffalo could be detected.")
    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    # Prepare DB entry
    user = await database.user_collection.find_one({"username": current_user.username})
    
    annotated_path = analysis_result["annotated_image_path"]
    annotated_url = (
        f"/uploads/annotated/{os.path.basename(annotated_path)}"
        if annotated_path else None
    )

    db_entry = {
        "user_id": str(user["_id"]),
        "animal_type": analysis_result["animal_type"],
        "original_image_url": unique_filename,
        "annotated_image_url": annotated_url,
        "overall_score": analysis_result["overall_score"],
        "trait_scores": analysis_result["trait_scores"],
        "timestamp": datetime.now(timezone.utc)
    }
    
    inserted_doc = await database.analysis_collection.insert_one(db_entry)
    created_analysis = await database.analysis_collection.find_one({"_id": inserted_doc.inserted_id})
    return models.AnalysisResult.model_validate(created_analysis)


@app.get("/analysis/history", response_model=list[models.AnalysisResult])
async def get_analysis_history(current_user: models.TokenData = Depends(security.get_current_user)):
    user = await database.user_collection.find_one({"username": current_user.username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    history_cursor = database.analysis_collection.find(
        {"user_id": str(user["_id"])}
    ).sort("timestamp", -1).limit(5)
    
    history_list = await history_cursor.to_list(length=None) 
    return [models.AnalysisResult.model_validate(item) for item in history_list]
