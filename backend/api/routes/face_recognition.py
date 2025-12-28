"""
Face recognition API routes
"""
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Form
from typing import Annotated

from backend.models import (
    UploadImageResponse,
    FaceRecognitionResponse,
    ErrorResponse
)
from backend.services import PersonService, FaceRecognitionService
from backend.api.dependencies import get_db_connection
from backend.config import settings

router = APIRouter(prefix="/face-recognition", tags=["face-recognition"])


@router.post("/upload", response_model=UploadImageResponse)
async def upload_person_image(
    image: Annotated[UploadFile, File(description="Face image file")],
    first_name: str = Form(..., description="First name"),
    last_name: str = Form(..., description="Last name"),
    conn = Depends(get_db_connection)
):
    """
    Upload a person's face image and create their record
    """
    try:
        # Validate file type
        if image.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        # Read image bytes
        image_bytes = await image.read()
        
        # Validate file size
        if len(image_bytes) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE} bytes"
            )
        
        # Create person with image
        service = PersonService(conn)
        result = service.create_person_with_image(
            first_name,
            last_name,
            image_bytes
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )
        
        return UploadImageResponse(
            message=result["message"],
            person_id=result["person_id"],
            first_name=first_name,
            last_name=last_name,
            filename=image.filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.post("/recognize", response_model=FaceRecognitionResponse)
async def recognize_face(
    image: Annotated[UploadFile, File(description="Face image to recognize")],
    conn = Depends(get_db_connection)
):
    """
    Recognize a person from their face image
    """
    try:
        # Validate file type
        if image.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        # Read image bytes
        image_bytes = await image.read()
        
        # Recognize face
        service = FaceRecognitionService(conn)
        result = service.recognize_face(image_bytes)
        
        if not result:
            return FaceRecognitionResponse(
                success=False,
                message="No face detected in image or no matching face found in database"
            )
        
        person_id, full_name, confidence = result
        
        return FaceRecognitionResponse(
            success=True,
            person_id=person_id,
            full_name=full_name,
            confidence=confidence,
            message=f"Face recognized as {full_name} with {confidence*100:.1f}% confidence"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to recognize face: {str(e)}"
        )
