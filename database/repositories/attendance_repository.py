"""
Attendance repository for tracking attendance records
"""
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime, date
from psycopg.rows import dict_row


class AttendanceRepository:
    """Repository for attendance-related database operations"""
    
    def __init__(self, conn):
        self.conn = conn
    
    def mark_attendance(self, person_id: UUID) -> UUID:
        """Mark attendance for a person"""
        try:
            query = """
                INSERT INTO attendance (person_id, timestamp)
                VALUES (%s, %s)
                RETURNING id
            """
            with self.conn.cursor() as cursor:
                cursor.execute(query, (person_id, datetime.now()))
                attendance_id = cursor.fetchone()[0]
            self.conn.commit()
            return attendance_id
        except Exception as e:
            self.conn.rollback()
            raise e
    
    def get_today_attendance(self) -> List[Dict[str, Any]]:
        """Get all attendance records for today"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT a.*, n.first_name, n.last_name, n.full_name
                    FROM attendance a
                    JOIN name n ON a.person_id = n.id
                    WHERE DATE(a.timestamp) = CURRENT_DATE
                    ORDER BY a.timestamp DESC
                    """
                )
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def get_attendance_by_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Get attendance records for a specific date"""
        try:
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT a.*, n.first_name, n.last_name, n.full_name
                    FROM attendance a
                    JOIN name n ON a.person_id = n.id
                    WHERE DATE(a.timestamp) = %s
                    ORDER BY a.timestamp DESC
                    """,
                    (target_date,)
                )
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def get_attendance_by_person(self, person_id: UUID, start_date: date = None, end_date: date = None) -> List[Dict[str, Any]]:
        """Get attendance records for a specific person"""
        try:
            query = """
                SELECT a.*, n.first_name, n.last_name, n.full_name
                FROM attendance a
                JOIN name n ON a.person_id = n.id
                WHERE a.person_id = %s
            """
            params = [person_id]
            
            if start_date:
                query += " AND DATE(a.timestamp) >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND DATE(a.timestamp) <= %s"
                params.append(end_date)
            
            query += " ORDER BY a.timestamp DESC"
            
            with self.conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def check_already_marked_today(self, person_id: UUID) -> bool:
        """Check if person has already marked attendance today"""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM attendance
                    WHERE person_id = %s AND DATE(timestamp) = CURRENT_DATE
                    """,
                    (person_id,)
                )
                count = cursor.fetchone()[0]
                return count > 0
        except Exception as e:
            raise e
