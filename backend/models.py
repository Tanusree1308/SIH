# backend/models.py
from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated, List, Optional
from bson import ObjectId
from datetime import datetime, timezone

# Custom type for Mongo ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

# --- User Models ---
class UserBase(BaseModel):
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserInResponse(UserBase):
    id: PyObjectId = Field(alias="_id")

class UserInDB(UserBase):
    id: PyObjectId = Field(alias="_id")
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

# --- Analysis Models ---
class TraitScore(BaseModel):
    trait_name: str
    score: float

class AnalysisResult(BaseModel):
    id: PyObjectId = Field(alias="_id")
    user_id: str
    animal_type: str
    original_image_url: str
    annotated_image_url: str
    overall_score: float
    trait_scores: List[TraitScore]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))