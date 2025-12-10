from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
import shutil
import os
from datetime import datetime

from services.document_processor import DocumentProcessor
from services.supabase_service import SupabaseService

router = APIRouter(prefix="/api/documents", tags=["documents"])

document_processor = DocumentProcessor()
supabase_service = SupabaseService()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form("lab_report"),
    patient_id: str = Form(...),
    description: Optional[str] = Form("")
):
    """Upload and process medical document"""
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.docx', '.txt', '.jpg', '.png', '.jpeg'}
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Create upload directory if not exists
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{patient_id}_{timestamp}_{file.filename.replace(' ', '_')}"
        file_path = os.path.join(upload_dir, safe_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        processed_data = document_processor.process_document(file_path, document_type)
        
        # Save to database
        document_record = {
            "patient_id": patient_id,
            "filename": file.filename,
            "document_type": document_type,
            "file_path": file_path,
            "description": description,
            "processed_data": processed_data,
            "uploaded_at": datetime.now().isoformat(),
            "file_size": os.path.getsize(file_path)
        }
        
        success = supabase_service.save_document(document_record)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save document to database")
        
        return {
            "success": True,
            "message": "Document uploaded and processed successfully",
            "document": {
                "id": f"doc_{timestamp}",
                "filename": file.filename,
                "type": document_type,
                "size_kb": round(os.path.getsize(file_path) / 1024, 2),
                "processed_data": processed_data,
                "download_url": f"/static/uploads/{safe_filename}",
                "uploaded_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patient/{patient_id}")
async def get_patient_documents(
    patient_id: str,
    document_type: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Get documents for a patient"""
    try:
        all_documents = supabase_service.get_patient_documents(patient_id)
        
        # Filter by type if specified
        if document_type:
            filtered_docs = [doc for doc in all_documents if doc.get("document_type") == document_type]
        else:
            filtered_docs = all_documents
        
        # Apply pagination
        paginated_docs = filtered_docs[offset:offset + limit]
        
        return {
            "documents": paginated_docs,
            "total": len(filtered_docs),
            "limit": limit,
            "offset": offset,
            "types": list(set(doc.get("document_type") for doc in all_documents))
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_document(document_id: str, patient_id: str):
    """Delete a document"""
    try:
        # In a real implementation, you would:
        # 1. Get document from database
        # 2. Delete file from storage
        # 3. Remove record from database
        
        # For demo, just return success
        return {
            "success": True,
            "message": f"Document {document_id} deleted (demo mode)",
            "deleted_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process/text")
async def process_text_document(
    text: str = Form(...),
    document_type: str = Form("doctor_note"),
    patient_id: str = Form(...)
):
    """Process text as a document"""
    try:
        # Process the text
        if document_type == "lab_report":
            processed_data = document_processor.process_lab_report(text)
        elif document_type == "doctor_note":
            processed_data = document_processor.process_doctor_notes(text)
        elif document_type == "prescription":
            processed_data = document_processor.process_prescription(text)
        else:
            processed_data = document_processor.process_general_document(text)
        
        # Save to database
        document_record = {
            "patient_id": patient_id,
            "filename": f"text_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "document_type": document_type,
            "file_path": "text_input",
            "processed_data": processed_data,
            "uploaded_at": datetime.now().isoformat(),
            "file_size": len(text.encode('utf-8'))
        }
        
        success = supabase_service.save_document(document_record)
        
        return {
            "success": success,
            "processed_data": processed_data,
            "document_id": f"text_{datetime.now().timestamp()}",
            "processed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/types")
async def get_document_types():
    """Get supported document types"""
    return {
        "document_types": [
            {"id": "lab_report", "name": "Lab Report", "description": "Blood tests, urine tests, etc."},
            {"id": "doctor_note", "name": "Doctor's Note", "description": "Clinical notes from healthcare provider"},
            {"id": "prescription", "name": "Prescription", "description": "Medication prescriptions"},
            {"id": "imaging", "name": "Imaging Report", "description": "X-ray, MRI, CT scan reports"},
            {"id": "insurance", "name": "Insurance Document", "description": "Insurance claims and EOBs"},
            {"id": "general", "name": "General Medical", "description": "Other medical documents"}
        ]
    }