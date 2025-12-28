"""
Database repository layer - handles all database operations
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
import psycopg
from psycopg.rows import dict_row


class PersonRepository:
    """Repository for person-related database operations"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def create(self, first_name: str, last_name: str, full_name: str = "") -> UUID:
        """Create a new person record"""
        if not full_name:
            full_name = f"{first_name} {last_name}"
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO name (first_name, last_name, full_name) 
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (first_name, last_name, full_name)
                )
                new_id = cursor.fetchone()[0]
            self.conn.commit()
            return new_id
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def get_by_id(self, person_id: UUID) -> Optional[Dict[str, Any]]:
        """Get person by ID"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT * FROM name WHERE id = %s",
                    (person_id,)
                )
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all persons"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM name ORDER BY date_created DESC")
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def delete(self, person_id: UUID) -> bool:
        """Delete a person by ID"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM name WHERE id = %s", (person_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def update(self, person_id: UUID, first_name: str = None, last_name: str = None) -> bool:
        """Update person information"""
        updates = []
        params = []
        
        if first_name:
            updates.append("first_name = %s")
            params.append(first_name)
        
        if last_name:
            updates.append("last_name = %s")
            params.append(last_name)
        
        if first_name or last_name:
            updates.append("full_name = %s")
            params.append(f"{first_name or ''} {last_name or ''}".strip())
        
        if not updates:
            return False
        
        params.append(person_id)
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"UPDATE name SET {', '.join(updates)} WHERE id = %s",
                    params
                )
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e


class EncodingRepository:
    """Repository for face encoding operations"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def create(self, person_id: UUID, encoding: str) -> UUID:
        """Store face encoding for a person"""
        try:
            query = """
                INSERT INTO encoding (person_id, face_encoding)
                VALUES (%s, %s)
                RETURNING id
            """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (person_id, encoding))
                encoding_id = cursor.fetchone()[0]
            self.conn.commit()
            return encoding_id
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def get_by_person_id(self, person_id: UUID) -> Optional[Dict[str, Any]]:
        """Get encoding for a specific person"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT * FROM encoding WHERE person_id = %s",
                    (person_id,)
                )
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all face encodings"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("SELECT * FROM encoding")
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def get_all_with_person_info(self) -> List[Dict[str, Any]]:
        """Get all encodings with associated person information"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT e.*, n.first_name, n.last_name, n.full_name
                    FROM encoding e
                    JOIN name n ON e.person_id = n.id
                    """
                )
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def delete(self, encoding_id: UUID) -> bool:
        """Delete an encoding by ID"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM encoding WHERE id = %s", (encoding_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def delete_by_person_id(self, person_id: UUID) -> bool:
        """Delete all encodings for a specific person"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM encoding WHERE person_id = %s", (person_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e


class ImageRepository:
    """Repository for image storage operations"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def create(self, person_id: UUID, image_bytes: bytes) -> UUID:
        """Store image bytes for a person"""
        try:
            query = """
                INSERT INTO images (person_id, image)
                VALUES (%s, %s)
                RETURNING id
            """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (person_id, image_bytes))
                image_id = cursor.fetchone()[0]
            self.conn.commit()
            return image_id
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def get_by_person_id(self, person_id: UUID) -> Optional[Dict[str, Any]]:
        """Get image for a specific person"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    "SELECT * FROM images WHERE person_id = %s",
                    (person_id,)
                )
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def delete(self, image_id: UUID) -> bool:
        """Delete an image by ID"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM images WHERE id = %s", (image_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def delete_by_person_id(self, person_id: UUID) -> bool:
        """Delete all images for a specific person"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM images WHERE person_id = %s", (person_id,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e
