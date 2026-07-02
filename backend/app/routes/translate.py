from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
import uuid
from datetime import datetime
from typing import List
from app.models.schemas import TranslationRequest, TranslationResponse, TranslationHistory
from app.services.pdf_processor import PDFProcessor
from app.services.translator import Translator

router = APIRouter()

# In-memory storage (replace with database in production)
translations = {}

@router.post("/translate", response_model=TranslationResponse)
async def translate_paper(request: TranslationRequest):
    """Start translation of a PDF paper"""
    
    translation_id = str(uuid.uuid4())
    
    # Find uploaded file
    upload_dir = Path("uploads")
    file_path = None
    
    for file in upload_dir.glob("*"):
        if request.filename in str(file):
            file_path = file
            break
    
    if not file_path or not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Extract text from PDF
        pdf_processor = PDFProcessor()
        extracted_text = pdf_processor.extract_text(str(file_path))
        
        # Translate text
        translator = Translator()
        translated_text = await translator.translate(
            extracted_text,
            target_language=request.target_language
        )
        
        # Store translation
        translations[translation_id] = {
            "filename": request.filename,
            "status": "completed",
            "translated_text": translated_text,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        return TranslationResponse(
            translation_id=translation_id,
            filename=request.filename,
            status="completed",
            progress=1.0,
            translated_text=translated_text,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@router.get("/history", response_model=List[TranslationHistory])
async def get_history():
    """Get translation history"""
    history = []
    for tid, data in translations.items():
        history.append(TranslationHistory(
            translation_id=tid,
            filename=data["filename"],
            target_language="Japanese",
            status=data["status"],
            created_at=data["created_at"],
            file_size=0,
            page_count=None
        ))
    return history

@router.get("/translation/{translation_id}", response_model=TranslationResponse)
async def get_translation(translation_id: str):
    """Get a specific translation result"""
    if translation_id not in translations:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    data = translations[translation_id]
    return TranslationResponse(
        translation_id=translation_id,
        filename=data["filename"],
        status=data["status"],
        progress=1.0,
        translated_text=data.get("translated_text"),
        created_at=data["created_at"],
        updated_at=data["updated_at"]
    )
