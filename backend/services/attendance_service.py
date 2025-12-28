"""
Attendance service - handles attendance tracking business logic
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime, date

from database.repositories.attendance_repository import AttendanceRepository
from backend.services.face_recognition_service import FaceRecognitionService
from database.repositories import PersonRepository


class AttendanceService:
    """Service for attendance management operations"""
    
    def __init__(self, conn):
        self.conn = conn
        self.attendance_repo = AttendanceRepository(conn)
        self.face_service = FaceRecognitionService(conn)
        self.person_repo = PersonRepository(conn)
    
    def mark_attendance_by_face(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Mark attendance by recognizing face from image
        Returns dict with success status, person info, and message
        """
        # Recognize face
        recognition_result = self.face_service.recognize_face(image_bytes)
        
        if not recognition_result:
            return {
                "success": False,
                "message": "No matching face found in database",
                "person_id": None,
                "full_name": None,
                "timestamp": None,
                "already_marked": False
            }
        
        person_id, full_name, confidence = recognition_result
        
        # Check if already marked today
        already_marked = self.attendance_repo.check_already_marked_today(person_id)
        
        if already_marked:
            return {
                "success": False,
                "message": f"Attendance already marked for {full_name} today",
                "person_id": person_id,
                "full_name": full_name,
                "timestamp": None,
                "already_marked": True,
                "confidence": confidence
            }
        
        try:
            # Mark attendance
            attendance_id = self.attendance_repo.mark_attendance(person_id)
            
            return {
                "success": True,
                "message": f"Attendance marked successfully for {full_name}",
                "person_id": person_id,
                "full_name": full_name,
                "timestamp": datetime.now(),
                "already_marked": False,
                "confidence": confidence,
                "attendance_id": attendance_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to mark attendance: {str(e)}",
                "person_id": person_id,
                "full_name": full_name,
                "timestamp": None,
                "already_marked": False
            }
    
    def mark_attendance_manual(self, person_id: UUID) -> Dict[str, Any]:
        """
        Manually mark attendance for a person by ID
        """
        # Check if person exists
        person = self.person_repo.get_by_id(person_id)
        
        if not person:
            return {
                "success": False,
                "message": "Person not found",
                "person_id": None,
                "full_name": None
            }
        
        # Check if already marked
        already_marked = self.attendance_repo.check_already_marked_today(person_id)
        
        if already_marked:
            return {
                "success": False,
                "message": f"Attendance already marked for {person['full_name']} today",
                "person_id": person_id,
                "full_name": person['full_name'],
                "already_marked": True
            }
        
        try:
            attendance_id = self.attendance_repo.mark_attendance(person_id)
            
            return {
                "success": True,
                "message": f"Attendance marked successfully for {person['full_name']}",
                "person_id": person_id,
                "full_name": person['full_name'],
                "timestamp": datetime.now(),
                "attendance_id": attendance_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to mark attendance: {str(e)}",
                "person_id": person_id,
                "full_name": person['full_name']
            }
    
    def get_today_attendance(self) -> List[Dict[str, Any]]:
        """Get all attendance records for today"""
        return self.attendance_repo.get_today_attendance()
    
    def get_attendance_by_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Get attendance records for a specific date"""
        return self.attendance_repo.get_attendance_by_date(target_date)
    
    def get_person_attendance(
        self, 
        person_id: UUID, 
        start_date: date = None, 
        end_date: date = None
    ) -> List[Dict[str, Any]]:
        """Get attendance records for a specific person"""
        return self.attendance_repo.get_attendance_by_person(person_id, start_date, end_date)
    
    def export_attendance_csv(self, records: List[Dict[str, Any]]) -> str:
        """
        Export attendance records to CSV format
        Returns CSV string
        """
        if not records:
            return "full_name,timestamp\n"
        
        csv_lines = ["full_name,timestamp"]
        
        for record in records:
            full_name = record.get('full_name', 'Unknown')
            timestamp = record.get('timestamp', '')
            if isinstance(timestamp, datetime):
                timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            csv_lines.append(f"{full_name},{timestamp}")
        
        return "\n".join(csv_lines)
