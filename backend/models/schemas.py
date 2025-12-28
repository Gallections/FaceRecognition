"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID


class PersonCreate(BaseModel):
    """Request model for creating a new person"""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip()


class PersonResponse(BaseModel):
    """Response model for person data"""
    id: UUID
    first_name: str
    last_name: str
    full_name: str
    date_created: datetime
    
    class Config:
        from_attributes = True


class PersonWithEncodingCreate(BaseModel):
    """Request model for creating person with face encoding"""
    first_name: str
    last_name: str
    # Image will be uploaded as multipart form data


class UploadImageResponse(BaseModel):
    """Response model for image upload"""
    message: str
    person_id: UUID
    first_name: str
    last_name: str
    filename: str


class FaceRecognitionRequest(BaseModel):
    """Request model for face recognition"""
    # Image will be uploaded as multipart form data
    pass


class FaceRecognitionResponse(BaseModel):
    """Response model for face recognition"""
    success: bool
    person_id: Optional[UUID] = None
    full_name: Optional[str] = None
    confidence: Optional[float] = None
    message: str


class AttendanceRecord(BaseModel):
    """Model for attendance record"""
    id: UUID
    person_id: UUID
    full_name: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AttendanceMarkRequest(BaseModel):
    """Request model for marking attendance"""
    # Image will be uploaded as multipart form data
    pass


class AttendanceMarkResponse(BaseModel):
    """Response model for marking attendance"""
    success: bool
    person_id: Optional[UUID] = None
    full_name: Optional[str] = None
    timestamp: Optional[datetime] = None
    message: str


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
