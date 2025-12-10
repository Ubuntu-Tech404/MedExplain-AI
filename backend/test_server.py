from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
import json
import os

# Create FastAPI app
app = FastAPI(
    title="Mediclinic AI Dashboard Test Server",
    description="Test backend for Mediclinic AI Dashboard",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directory if it doesn't exist
os.makedirs("static/uploads", exist_ok=True)

# ========== TEST ENDPOINTS ==========

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "Mediclinic AI Dashboard Test Server",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "/health": "Health check",
            "/demo/data": "Demo patient data",
            "/api/test": "API test endpoint",
            "/api/explain": "Medical text explanation",
            "/api/upload": "File upload test",
            "/docs": "API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "mediclinic-test-server",
        "timestamp": datetime.now().isoformat(),
        "environment": "development"
    }

@app.get("/demo/data")
async def demo_data():
    """Demo patient data"""
    return {
        "patient": {
            "id": "demo-patient-001",
            "name": "John Doe",
            "age": 45,
            "gender": "male",
            "blood_type": "O+",
            "height_cm": 175,
            "weight_kg": 80,
            "conditions": ["Type 2 Diabetes", "Hypertension"],
            "allergies": ["Penicillin"]
        },
        "lab_results": {
            "glucose": 145,
            "hba1c": 6.8,
            "cholesterol": 220,
            "ldl": 140,
            "hdl": 42,
            "triglycerides": 185,
            "creatinine": 1.1
        },
        "medications": [
            {"name": "Metformin", "dosage": "500mg", "frequency": "Twice daily", "status": "active"},
            {"name": "Lisinopril", "dosage": "10mg", "frequency": "Once daily", "status": "active"}
        ],
        "vitals": {
            "blood_pressure": {"systolic": 135, "diastolic": 85},
            "heart_rate": 72,
            "temperature": 98.6,
            "respiratory_rate": 16
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test")
async def api_test():
    """Test API endpoint"""
    return {
        "message": "API is working correctly!",
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "data": {
            "test": "passed",
            "code": 200
        }
    }

@app.post("/api/explain")
async def explain_text(text: str, context: str = ""):
    """Explain medical text"""
    explanations = {
        "diabetes": "Diabetes is a condition where your body has trouble managing sugar levels.",
        "hypertension": "Hypertension means high blood pressure, which can strain your heart.",
        "cholesterol": "Cholesterol is a type of fat in your blood. High levels can increase heart disease risk.",
        "metformin": "Metformin is a medication that helps control blood sugar in type 2 diabetes.",
        "lisinopril": "Lisinopril is a blood pressure medication that relaxes your blood vessels."
    }
    
    text_lower = text.lower()
    explanation = "This appears to be medical information. Please consult with your healthcare provider for accurate information."
    
    for key, value in explanations.items():
        if key in text_lower:
            explanation = value
            break
    
    return {
        "original": text,
        "explanation": explanation,
        "context": context,
        "confidence": "high" if explanation != "This appears to be medical information..." else "medium",
        "timestamp": datetime.now().isoformat(),
        "model": "test-model",
        "note": "Using test data - connect AI model for real explanations"
    }

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    document_type: str = Form("lab_report"),
    patient_id: str = Form("demo-patient-001")
):
    """Test file upload endpoint"""
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{patient_id}_{timestamp}_{file.filename}"
    file_path = f"static/uploads/{filename}"
    
    try:
        # Read file content
        content = await file.read()
        
        # Save to disk
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Get file info
        file_size_kb = len(content) / 1024
        
        return {
            "success": True,
            "message": "File uploaded successfully",
            "file_info": {
                "filename": file.filename,
                "original_name": file.filename,
                "size_kb": round(file_size_kb, 2),
                "mime_type": file.content_type,
                "uploaded_at": datetime.now().isoformat(),
                "file_path": file_path,
                "url": f"/{file_path}"
            },
            "metadata": {
                "document_type": document_type,
                "patient_id": patient_id,
                "processing": {
                    "status": "completed",
                    "extracted_data": {"test": "data extracted successfully"}
                }
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "File upload failed"
            }
        )

@app.post("/api/analyze")
async def analyze_labs(lab_data: dict):
    """Analyze lab results"""
    analysis = {
        "overall": "Your lab results show some areas that need attention.",
        "details": [
            {"test": "Glucose", "value": lab_data.get("glucose", 0), "status": "high" if lab_data.get("glucose", 0) > 100 else "normal"},
            {"test": "Cholesterol", "value": lab_data.get("cholesterol", 0), "status": "high" if lab_data.get("cholesterol", 0) > 200 else "normal"},
            {"test": "HDL", "value": lab_data.get("hdl", 0), "status": "low" if lab_data.get("hdl", 0) < 40 else "normal"}
        ],
        "recommendations": [
            "Follow up with your doctor",
            "Maintain healthy diet",
            "Exercise regularly"
        ],
        "timestamp": datetime.now().isoformat()
    }
    
    return {
        "analysis": analysis,
        "lab_data": lab_data,
        "summary": f"Analyzed {len(lab_data)} lab values",
        "model": "test-analyzer"
    }

@app.get("/api/documents")
async def get_documents(patient_id: str = "demo-patient-001"):
    """Get patient documents"""
    return {
        "patient_id": patient_id,
        "documents": [
            {
                "id": "doc_001",
                "filename": "blood_test.pdf",
                "type": "lab_report",
                "uploaded_at": "2024-01-15T10:30:00",
                "size_kb": 125,
                "url": "/static/uploads/demo_lab.pdf"
            },
            {
                "id": "doc_002",
                "filename": "doctor_note.docx",
                "type": "doctor_note",
                "uploaded_at": "2024-01-10T14:20:00",
                "size_kb": 89,
                "url": "/static/uploads/demo_note.docx"
            }
        ],
        "count": 2,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/chart")
async def generate_chart(chart_type: str = "blood_work"):
    """Generate test chart data"""
    
    chart_data = {
        "blood_work": {
            "type": "bar",
            "data": {
                "labels": ["Glucose", "Cholesterol", "HDL", "LDL", "Triglycerides"],
                "datasets": [
                    {
                        "label": "Your Values",
                        "data": [145, 220, 42, 140, 185],
                        "backgroundColor": ["#EF4444", "#F59E0B", "#10B981", "#F59E0B", "#EF4444"]
                    },
                    {
                        "label": "Normal Range Max",
                        "data": [100, 200, 60, 100, 150],
                        "type": "line",
                        "borderColor": "#3B82F6",
                        "fill": False
                    }
                ]
            },
            "options": {
                "title": "Blood Work Analysis",
                "responsive": True
            }
        },
        "vitals": {
            "type": "gauge",
            "data": {
                "heart_rate": 72,
                "blood_pressure": "135/85",
                "temperature": 98.6
            }
        }
    }
    
    return {
        "chart_type": chart_type,
        "chart_data": chart_data.get(chart_type, chart_data["blood_work"]),
        "timestamp": datetime.now().isoformat()
    }

# ========== RUN THE SERVER ==========

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 STARTING MEDICLINIC TEST SERVER")
    print("=" * 60)
    print()
    print("📊 Server Information:")
    print(f"   Name: Mediclinic AI Dashboard Test Server")
    print(f"   Version: 1.0.0")
    print(f"   Environment: Development")
    print()
    print("🌐 Endpoints:")
    print(f"   📍 API: http://localhost:8000")
    print(f"   📚 Documentation: http://localhost:8000/docs")
    print(f"   🏥 Health Check: http://localhost:8000/health")
    print(f"   🎯 Demo Data: http://localhost:8000/demo/data")
    print()
    print("🔌 Test these endpoints:")
    print("   curl http://localhost:8000/")
    print("   curl http://localhost:8000/health")
    print("   curl -X POST http://localhost:8000/api/explain -H 'Content-Type: application/json' -d '{\"text\":\"diabetes\"}'")
    print()
    print("🔄 Server starting...")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )