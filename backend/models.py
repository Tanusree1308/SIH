# backend/models.py

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Any
from datetime import datetime, timezone
from bson import ObjectId
from pydantic_core import core_schema

# --- Custom Pydantic ObjectId Type ---
class PydanticObjectId(ObjectId):
    @classmethod
    def validate(cls, v: Any, info):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)    

    @classmethod
    def _get_pydantic_core_schema_(cls, source_type: Any, handler: Any):
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

# --- User Models ---
class UserBase(BaseModel):
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserInResponse(UserBase):
    id: PydanticObjectId = Field(alias="_id")
    class Config:
        arbitrary_types_allowed = True

class UserInDB(UserBase):
    id: PydanticObjectId = Field(alias="_id")
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
    id: PydanticObjectId = Field(alias="_id")
    user_id: str
    animal_type: str  # <-- unified field name
    original_image_url: str
    annotated_image_url: str
    overall_score: float
    trait_scores: List[TraitScore]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True