"""
Face recognition service - handles all face recognition business logic
"""
import face_recognition
import numpy as np
import json
from typing import Optional, Tuple, List, Dict, Any
import cv2
from uuid import UUID

from database.repositories import EncodingRepository, PersonRepository
from backend.config import settings


class FaceRecognitionService:
    """Service for face recognition operations"""
    
    def __init__(self, conn):
        self.conn = conn
        self.encoding_repo = EncodingRepository(conn)
        self.person_repo = PersonRepository(conn)
        self.tolerance = settings.FACE_RECOGNITION_TOLERANCE
        self.model = settings.FACE_DETECTION_MODEL
    
    def extract_face_encoding(self, image_bytes: bytes) -> Optional[str]:
        """
        Extract face encoding from image bytes
        Returns JSON string of encoding or None if no face detected
        """
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img_bgr is None:
                print("Error: Could not decode image")
                return None
            
            # Convert to RGB
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            
            # First detect face locations
            face_locations = face_recognition.face_locations(img_rgb, model=self.model)
            
            if not face_locations:
                print("Error: No face detected in image")
                return None
            
            # Get face encodings for detected faces
            encodings = face_recognition.face_encodings(
                img_rgb,
                known_face_locations=face_locations,
                model="large"  # Use large model for better accuracy
            )
            
            if not encodings:
                print("Error: Could not extract face encoding")
                return None
            
            # Take first face found
            encoding = encodings[0]
            
            # Convert to JSON string
            encoding_json = json.dumps(encoding.tolist())
            
            return encoding_json
            
        except Exception as e:
            print(f"Error extracting face encoding: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def recognize_face(self, image_bytes: bytes) -> Optional[Tuple[UUID, str, float]]:
        """
        Recognize a face from image bytes
        Returns tuple of (person_id, full_name, confidence) or None if no match
        """
        try:
            # Extract encoding from input image
            input_encoding_json = self.extract_face_encoding(image_bytes)
            
            if not input_encoding_json:
                print("Warning: Could not extract encoding from input image")
                return None
            
            input_encoding = np.array(json.loads(input_encoding_json))
            
            # Get all stored encodings
            all_encodings = self.encoding_repo.get_all_with_person_info()
            
            if not all_encodings:
                print("Warning: No encodings found in database")
                return None
            
            print(f"Comparing against {len(all_encodings)} stored faces...")
            
            # Compare with all stored encodings
            best_match = None
            best_distance = float('inf')
            
            for record in all_encodings:
                # face_encoding is already a list from JSONB, no need to parse
                stored_encoding_data = record['face_encoding']
                if isinstance(stored_encoding_data, str):
                    stored_encoding = np.array(json.loads(stored_encoding_data))
                else:
                    stored_encoding = np.array(stored_encoding_data)
                
                # Calculate face distance
                distance = face_recognition.face_distance([stored_encoding], input_encoding)[0]
                
                print(f"Distance to {record['full_name']}: {distance:.4f} (tolerance: {self.tolerance})")
                
                if distance < best_distance and distance <= self.tolerance:
                    best_distance = distance
                    best_match = record
            
            if best_match:
                confidence = 1.0 - best_distance  # Convert distance to confidence
                print(f"✅ Match found: {best_match['full_name']} (confidence: {confidence:.2%})")
                return (
                    best_match['person_id'],
                    best_match['full_name'],
                    confidence
                )
            
            print(f"❌ No match found within tolerance {self.tolerance}")
            return None
            
        except Exception as e:
            print(f"Error recognizing face: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def verify_face(self, image_bytes: bytes, person_id: UUID) -> Tuple[bool, float]:
        """
        Verify if the face in image matches a specific person
        Returns tuple of (is_match, confidence)
        """
        try:
            # Extract encoding from input image
            input_encoding_json = self.extract_face_encoding(image_bytes)
            
            if not input_encoding_json:
                return False, 0.0
            
            input_encoding = np.array(json.loads(input_encoding_json))
            
            # Get stored encoding for person
            stored_record = self.encoding_repo.get_by_person_id(person_id)
            
            if not stored_record:
                return False, 0.0
            
            # face_encoding is already a list from JSONB, no need to parse
            stored_encoding_data = stored_record['face_encoding']
            if isinstance(stored_encoding_data, str):
                stored_encoding = np.array(json.loads(stored_encoding_data))
            else:
                stored_encoding = np.array(stored_encoding_data)
            
            # Compare encodings
            distance = face_recognition.face_distance([stored_encoding], input_encoding)[0]
            
            is_match = distance <= self.tolerance
            confidence = 1.0 - distance
            
            return is_match, confidence
            
        except Exception as e:
            print(f"Error verifying face: {e}")
            import traceback
            traceback.print_exc()
            return False, 0.0
    
    def detect_faces_count(self, image_bytes: bytes) -> int:
        """
        Count number of faces in an image
        """
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img_bgr is None:
                return 0
            
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(img_rgb, model=self.model)
            
            return len(face_locations)
            
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return 0
    
    def process_and_store_face(self, image_bytes: bytes, person_id: UUID) -> bool:
        """
        Extract face encoding from image and store it along with the image
        Returns True on success, False on failure
        """
        try:
            # Extract face encoding
            encoding_json = self.extract_face_encoding(image_bytes)
            
            if not encoding_json:
                return False
            
            # Store encoding
            self.encoding_repo.create(person_id, encoding_json)
            
            # Store image
            from database.repositories import ImageRepository
            image_repo = ImageRepository(self.conn)
            image_repo.create(person_id, image_bytes)
            
            return True
            
        except Exception as e:
            print(f"Error processing and storing face: {e}")
            return False
