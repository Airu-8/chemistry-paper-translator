import PyPDF2
import pdfplumber
from pathlib import Path
from typing import List, Dict

class PDFProcessor:
    """Extract and process text from PDF files"""
    
    def __init__(self):
        self.max_pages = None
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF while preserving structure"""
        text = ""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                self.max_pages = len(pdf.pages)
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        
        return text
    
    def extract_metadata(self, pdf_path: str) -> Dict:
        """Extract PDF metadata"""
        metadata = {}
        
        try:
            with PyPDF2.PdfReader(pdf_path) as pdf:
                metadata = dict(pdf.metadata) if pdf.metadata else {}
                metadata["pages"] = len(pdf.pages)
        except Exception as e:
            raise Exception(f"Error extracting metadata: {str(e)}")
        
        return metadata
    
    def get_page_count(self, pdf_path: str) -> int:
        """Get number of pages in PDF"""
        try:
            with PyPDF2.PdfReader(pdf_path) as pdf:
                return len(pdf.pages)
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
