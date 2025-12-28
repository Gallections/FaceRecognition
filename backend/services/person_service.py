"""
Person management service - handles person-related business logic
"""
from typing import Optional, List, Dict, Any
from uuid import UUID

from database.repositories import PersonRepository, EncodingRepository, ImageRepository
from backend.services.face_recognition_service import FaceRecognitionService


class PersonService:
    """Service for person management operations"""
    
    def __init__(self, conn):
        self.conn = conn
        self.person_repo = PersonRepository(conn)
        self.encoding_repo = EncodingRepository(conn)
        self.image_repo = ImageRepository(conn)
        self.face_service = FaceRecognitionService(conn)
    
    def create_person(self, first_name: str, last_name: str) -> UUID:
        """Create a new person"""
        return self.person_repo.create(first_name, last_name)
    
    def create_person_with_image(
        self, 
        first_name: str, 
        last_name: str, 
        image_bytes: bytes
    ) -> Dict[str, Any]:
        """
        Create a new person with face image
        Returns dict with person_id, success status, and message
        """
        # Extract face encoding
        encoding_json = self.face_service.extract_face_encoding(image_bytes)
        
        if not encoding_json:
            return {
                "success": False,
                "message": "No face detected in the image",
                "person_id": None
            }
        
        try:
            # Create person record
            person_id = self.person_repo.create(first_name, last_name)
            
            # Store encoding
            self.encoding_repo.create(person_id, encoding_json)
            
            # Store image
            self.image_repo.create(person_id, image_bytes)
            
            return {
                "success": True,
                "message": "Person created successfully",
                "person_id": person_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create person: {str(e)}",
                "person_id": None
            }
    
    def get_person(self, person_id: UUID) -> Optional[Dict[str, Any]]:
        """Get person by ID"""
        return self.person_repo.get_by_id(person_id)
    
    def get_all_persons(self) -> List[Dict[str, Any]]:
        """Get all persons"""
        return self.person_repo.get_all()
    
    def update_person(
        self, 
        person_id: UUID, 
        first_name: str = None, 
        last_name: str = None
    ) -> bool:
        """Update person information"""
        return self.person_repo.update(person_id, first_name, last_name)
    
    def delete_person(self, person_id: UUID) -> bool:
        """Delete a person (cascades to encodings and images)"""
        return self.person_repo.delete(person_id)
    
    def get_person_image(self, person_id: UUID) -> Optional[bytes]:
        """Get stored image for a person"""
        image_record = self.image_repo.get_by_person_id(person_id)
        if image_record:
            return image_record['image']
        return None
