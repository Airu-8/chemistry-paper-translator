from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from dotenv import load_dotenv

from app.routes import upload, translate

# Load environment variables
load_dotenv()

# Create uploads directory if it doesn't exist
Path("uploads").mkdir(exist_ok=True)

app = FastAPI(
    title="Chemistry Paper Translator API",
    description="API for translating chemistry research papers from PDF",
    version="1.0.0"
)

# Configure CORS
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(translate.router, prefix="/api", tags=["translate"])

@app.get("/")
async def root():
    return {
        "message": "Chemistry Paper Translator API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
