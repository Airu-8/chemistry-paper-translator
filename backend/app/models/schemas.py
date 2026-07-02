from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TranslationRequest(BaseModel):
    """Request model for translation"""
    filename: str
    target_language: str = "Japanese"
    preserve_formatting: bool = True

class TranslationResponse(BaseModel):
    """Response model for translation"""
    translation_id: str
    filename: str
    status: str
    progress: float
    translated_text: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TranslationHistory(BaseModel):
    """Translation history entry"""
    translation_id: str
    filename: str
    target_language: str
    status: str
    created_at: datetime
    file_size: int
    page_count: Optional[int] = None

class FileUploadResponse(BaseModel):
    """Response for file upload"""
    filename: str
    file_id: str
    size: int
    message: str

class TranslationProgressUpdate(BaseModel):
    """Real-time translation progress update"""
    translation_id: str
    status: str
    progress: float
    current_page: Optional[int] = None
    total_pages: Optional[int] = None
    message: str
