"""
Attendance API routes
"""
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile, Response
from fastapi.responses import StreamingResponse
from typing import Annotated, List, Optional
from uuid import UUID
from datetime import date, datetime
import io

from backend.models import (
    AttendanceMarkResponse,
    AttendanceRecord,
    ErrorResponse
)
from backend.services import AttendanceService
from backend.api.dependencies import get_db_connection
from backend.config import settings

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("/mark/face", response_model=AttendanceMarkResponse)
async def mark_attendance_by_face(
    image: Annotated[UploadFile, File(description="Face image for attendance")],
    conn = Depends(get_db_connection)
):
    """
    Mark attendance by recognizing face from image
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
        
        # Mark attendance
        service = AttendanceService(conn)
        result = service.mark_attendance_by_face(image_bytes)
        
        return AttendanceMarkResponse(
            success=result["success"],
            person_id=result.get("person_id"),
            full_name=result.get("full_name"),
            timestamp=result.get("timestamp"),
            message=result["message"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark attendance: {str(e)}"
        )


@router.post("/mark/manual/{person_id}", response_model=AttendanceMarkResponse)
async def mark_attendance_manual(
    person_id: UUID,
    conn = Depends(get_db_connection)
):
    """
    Manually mark attendance for a person by ID
    """
    try:
        service = AttendanceService(conn)
        result = service.mark_attendance_manual(person_id)
        
        return AttendanceMarkResponse(
            success=result["success"],
            person_id=result.get("person_id"),
            full_name=result.get("full_name"),
            timestamp=result.get("timestamp"),
            message=result["message"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark attendance: {str(e)}"
        )


@router.get("/today", response_model=List[AttendanceRecord])
async def get_today_attendance(conn = Depends(get_db_connection)):
    """
    Get all attendance records for today
    """
    try:
        service = AttendanceService(conn)
        records = service.get_today_attendance()
        return records
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attendance: {str(e)}"
        )


@router.get("/date/{target_date}", response_model=List[AttendanceRecord])
async def get_attendance_by_date(
    target_date: date,
    conn = Depends(get_db_connection)
):
    """
    Get attendance records for a specific date
    """
    try:
        service = AttendanceService(conn)
        records = service.get_attendance_by_date(target_date)
        return records
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attendance: {str(e)}"
        )


@router.get("/person/{person_id}", response_model=List[AttendanceRecord])
async def get_person_attendance(
    person_id: UUID,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    conn = Depends(get_db_connection)
):
    """
    Get attendance records for a specific person
    """
    try:
        service = AttendanceService(conn)
        records = service.get_person_attendance(person_id, start_date, end_date)
        return records
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attendance: {str(e)}"
        )


@router.get("/export/today")
async def export_today_attendance_csv(conn = Depends(get_db_connection)):
    """
    Export today's attendance as CSV file
    """
    try:
        service = AttendanceService(conn)
        records = service.get_today_attendance()
        csv_content = service.export_attendance_csv(records)
        
        # Create CSV response
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=attendance_{datetime.now().strftime('%Y-%m-%d')}.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export attendance: {str(e)}"
        )


@router.get("/export/date/{target_date}")
async def export_attendance_csv_by_date(
    target_date: date,
    conn = Depends(get_db_connection)
):
    """
    Export attendance for a specific date as CSV file
    """
    try:
        service = AttendanceService(conn)
        records = service.get_attendance_by_date(target_date)
        csv_content = service.export_attendance_csv(records)
        
        # Create CSV response
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=attendance_{target_date}.csv"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export attendance: {str(e)}"
        )
