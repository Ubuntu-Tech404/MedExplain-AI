from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
import os
from datetime import datetime
import shutil
import json
import logging

from config import settings
from database import db
from middleware import LoggingMiddleware, SecurityMiddleware, ErrorHandlingMiddleware
from services.llama_service import LlamaMedicalService
from services.supabase_service import SupabaseService

# Import routers
from routers.medical import router as medical_router
from routers.documents import router as documents_router
from routers.analysis import router as analysis_router
from routers.auth import router as auth_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
llama_service = LlamaMedicalService()
supabase_service = SupabaseService()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered medical dashboard with Llama 3.2 11B",
    version=settings.app_version,
    docs_url=f"{settings.api_prefix}/docs" if settings.debug else None,
    redoc_url=f"{settings.api_prefix}/redoc" if settings.debug else None,
    openapi_url=f"{settings.api_prefix}/openapi.json" if settings.debug else None,
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = "static"
os.makedirs(static_dir, exist_ok=True)
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs("static/charts", exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routers with API prefix
app.include_router(medical_router, prefix=settings.api_prefix)
app.include_router(documents_router, prefix=settings.api_prefix)
app.include_router(analysis_router, prefix=settings.api_prefix)
app.include_router(auth_router, prefix=settings.api_prefix)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    # Connect to database
    if db.connect():
        logger.info("Database connected successfully")
    else:
        logger.warning("Using local storage (database not connected)")
    
    # Check Llama model
    if llama_service.model_loaded:
        logger.info("Llama 3.2 11B model loaded successfully")
    else:
        logger.warning("Llama model not loaded - some features may be limited")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down application")
    db.disconnect()

# Root endpoint
@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "operational",
        "ai_model": "Llama 3.2 11B",
        "api_endpoints": {
            "medical": f"{settings.api_prefix}/medical",
            "documents": f"{settings.api_prefix}/documents",
            "analysis": f"{settings.api_prefix}/analysis",
            "auth": f"{settings.api_prefix}/auth"
        },
        "documentation": f"{settings.api_prefix}/docs" if settings.debug else "disabled",
        "timestamp": datetime.now().isoformat()
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "llama_model": "loaded" if llama_service.model_loaded else "not_loaded",
            "database": db.health_check(),
            "environment": settings.environment
        },
        "version": settings.app_version
    }
    return JSONResponse(content=health_status)

# Demo endpoints
@app.get("/demo/data")
async def get_demo_data():
    """Get demo data for testing"""
    return {
        "patient": {
            "id": "demo-patient-001",
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "conditions": ["Type 2 Diabetes", "Hypertension"],
            "blood_type": "O+"
        },
        "lab_results": {
            "glucose": 145,
            "hba1c": 6.8,
            "cholesterol": 220,
            "ldl": 140,
            "hdl": 42,
            "triglycerides": 185,
            "creatinine": 1.1,
            "sodium": 140
        },
        "medications": [
            {"name": "Metformin", "dosage": "500mg", "frequency": "Twice daily", "status": "active"},
            {"name": "Lisinopril", "dosage": "10mg", "frequency": "Once daily", "status": "active"}
        ],
        "vitals": {
            "blood_pressure": {"systolic": 135, "diastolic": 85},
            "heart_rate": 72,
            "temperature": 98.6,
            "weight_kg": 85.5,
            "height_cm": 175
        }
    }

@app.post("/demo/analyze")
async def demo_analysis():
    """Demo analysis endpoint"""
    demo_data = {
        "glucose": 145,
        "hba1c": 6.8,
        "cholesterol": 220,
        "ldl": 140,
        "hdl": 42,
        "triglycerides": 185
    }
    
    try:
        analysis = llama_service.analyze_lab_results(demo_data)
        
        return JSONResponse(content={
            "success": True,
            "demo_data": demo_data,
            "analysis": analysis,
            "note": "This is demo analysis using sample data",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Demo analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# File upload demo endpoint
@app.post("/demo/upload")
async def demo_upload(file: UploadFile = File(...)):
    """Demo file upload endpoint"""
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("static/uploads/demo", exist_ok=True)
        
        # Save file
        file_path = f"static/uploads/demo/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file info
        file_size_kb = os.path.getsize(file_path) / 1024
        
        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "file_size_kb": round(file_size_kb, 2),
            "file_path": f"/{file_path}",
            "message": "File uploaded successfully (demo)",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Demo upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Status endpoint
@app.get("/status")
async def status_check():
    """Application status check"""
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "environment": settings.environment,
        "debug_mode": settings.debug,
        "current_time": datetime.now().isoformat(),
        "uptime": "unknown"  # You can add uptime calculation here
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )