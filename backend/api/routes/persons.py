"""
Person API routes
"""
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
from fastapi.responses import Response
from typing import List, Annotated
from uuid import UUID

from backend.models import PersonCreate, PersonResponse, ErrorResponse
from backend.services import PersonService, FaceRecognitionService
from backend.api.dependencies import get_db_connection
from database.repositories import ImageRepository, EncodingRepository
from backend.config import settings

router = APIRouter(prefix="/persons", tags=["persons"])


@router.post("/", response_model=PersonResponse, status_code=status.HTTP_201_CREATED)
async def create_person(
    person_data: PersonCreate,
    conn = Depends(get_db_connection)
):
    """Create a new person"""
    try:
        service = PersonService(conn)
        person_id = service.create_person(
            person_data.first_name,
            person_data.last_name
        )
        
        person = service.get_person(person_id)
        return person
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create person: {str(e)}"
        )


@router.get("/", response_model=List[PersonResponse])
async def get_all_persons(conn = Depends(get_db_connection)):
    """Get all persons"""
    try:
        service = PersonService(conn)
        persons = service.get_all_persons()
        return persons
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve persons: {str(e)}"
        )


@router.get("/{person_id}", response_model=PersonResponse)
async def get_person(person_id: UUID, conn = Depends(get_db_connection)):
    """Get a person by ID"""
    try:
        service = PersonService(conn)
        person = service.get_person(person_id)
        
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
        return person
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve person: {str(e)}"
        )


@router.put("/{person_id}", response_model=PersonResponse)
async def update_person(
    person_id: UUID,
    person_data: PersonCreate,
    conn = Depends(get_db_connection)
):
    """Update a person's information"""
    try:
        service = PersonService(conn)
        
        # Check if person exists
        existing = service.get_person(person_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
        # Update
        service.update_person(
            person_id,
            person_data.first_name,
            person_data.last_name
        )
        
        # Return updated person
        person = service.get_person(person_id)
        return person
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update person: {str(e)}"
        )


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(person_id: UUID, conn = Depends(get_db_connection)):
    """Delete a person"""
    try:
        service = PersonService(conn)
        
        # Check if person exists
        existing = service.get_person(person_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
        service.delete_person(person_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete person: {str(e)}"
        )


@router.get("/{person_id}/image")
async def get_person_image(person_id: UUID, conn = Depends(get_db_connection)):
    """Get a person's image"""
    try:
        image_repo = ImageRepository(conn)
        image_data = image_repo.get_by_person_id(person_id)
        
        if not image_data or not image_data.get('image'):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found for this person"
            )
        
        # Return image as response
        return Response(
            content=bytes(image_data['image']),
            media_type="image/jpeg"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve image: {str(e)}"
        )


@router.put("/{person_id}/image")
async def update_person_image(
    person_id: UUID,
    image: Annotated[UploadFile, File(description="New face image file")],
    conn = Depends(get_db_connection)
):
    """Update a person's image"""
    try:
        service = PersonService(conn)
        
        # Check if person exists
        existing = service.get_person(person_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Person not found"
            )
        
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
        
        # Update image using FaceRecognitionService
        face_service = FaceRecognitionService(conn)
        encoding_repo = EncodingRepository(conn)
        
        # Delete old encoding and image
        encoding_repo.delete_by_person_id(person_id)
        image_repo = ImageRepository(conn)
        image_repo.delete_by_person_id(person_id)
        
        # Add new image and encoding
        result = face_service.process_and_store_face(image_bytes, person_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No face detected in image or face could not be processed"
            )
        
        return {"message": "Image updated successfully", "person_id": str(person_id)}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update image: {str(e)}"
        )
