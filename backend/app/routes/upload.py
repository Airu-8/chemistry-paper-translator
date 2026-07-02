from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
import os
from app.models.schemas import FileUploadResponse

router = APIRouter()

UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_UPLOAD_SIZE_MB", 50)) * 1024 * 1024

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload a PDF file for translation"""
    
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Read file and check size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    
    # Ensure upload directory exists
    UPLOAD_DIR.mkdir(exist_ok=True)
    
    # Save file
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as f:
        f.write(content)
    
    return FileUploadResponse(
        filename=file.filename,
        file_id=file_id,
        size=len(content),
        message="File uploaded successfully"
    )
