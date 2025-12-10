from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
import json

from models.ai_models import (
    ExplanationRequest,
    DiagnosisRequest,
    LabAnalysisRequest,
    MedicationExplanationRequest,
    SymptomAnalysisRequest
)
from services.llama_service import LlamaMedicalService
from services.diagnosis_explainer import DiagnosisExplainer
from services.medical_analyzer import MedicalAnalyzer

router = APIRouter(prefix="/api/medical", tags=["medical"])

llama_service = LlamaMedicalService()
diagnosis_explainer = DiagnosisExplainer()
medical_analyzer = MedicalAnalyzer()

@router.post("/explain")
async def explain_medical(request: ExplanationRequest):
    """Explain medical text in simple terms"""
    try:
        explanation = llama_service.explain_medical_text(
            text=request.text,
            context=request.context
        )
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/diagnosis/explain")
async def explain_diagnosis(request: DiagnosisRequest):
    """Explain medical diagnosis"""
    try:
        # Use diagnosis explainer for comprehensive explanation
        explanation = diagnosis_explainer.explain_diagnosis(
            diagnosis=request.diagnosis,
            patient_context={
                "age": request.patient_age,
                "gender": request.patient_gender,
                "notes": request.notes
            }
        )
        
        # Also get Llama's perspective
        llama_explanation = llama_service.explain_diagnosis(
            diagnosis=request.diagnosis,
            notes=request.notes
        )
        
        return {
            "structured_explanation": explanation,
            "ai_explanation": llama_explanation,
            "combined_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/labs/analyze")
async def analyze_labs(request: LabAnalysisRequest):
    """Analyze lab results"""
    try:
        # Get AI analysis
        ai_analysis = llama_service.analyze_lab_results(request.lab_data)
        
        # Get medical analyzer categorization
        categorization = medical_analyzer.categorize_lab_results(request.lab_data)
        
        # Calculate health score
        health_score = medical_analyzer.calculate_health_score(request.lab_data)
        
        # Detect risk factors
        risk_factors = medical_analyzer.detect_risk_factors(
            request.lab_data,
            request.patient_info.get("age", 50) if request.patient_info else 50
        )
        
        # Generate health report
        health_report = medical_analyzer.generate_health_report(
            request.lab_data,
            request.patient_info
        )
        
        return {
            "ai_analysis": ai_analysis,
            "categorization": categorization,
            "health_score": health_score,
            "risk_factors": risk_factors,
            "health_report": health_report,
            "analyzed_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/medications/explain")
async def explain_medication(request: MedicationExplanationRequest):
    """Explain medication"""
    try:
        explanation = llama_service.explain_medication(request.medication_name)
        
        # Add context about patient conditions
        if request.patient_conditions:
            explanation["patient_context"] = {
                "conditions": request.patient_conditions,
                "note": "This medication may interact with your conditions. Consult your doctor."
            }
        
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/symptoms/analyze")
async def analyze_symptoms(request: SymptomAnalysisRequest):
    """Analyze symptoms and suggest possible conditions"""
    try:
        analysis = diagnosis_explainer.analyze_symptoms(
            symptoms=request.symptoms,
            patient_info=request.patient_info
        )
        
        # Add Llama analysis for context
        symptom_text = ", ".join(request.symptoms)
        llama_context = llama_service.explain_medical_text(
            f"Symptoms: {symptom_text}",
            "What could these symptoms indicate?"
        )
        
        analysis["ai_context"] = llama_context
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/health/report")
async def generate_health_report(request: LabAnalysisRequest):
    """Generate comprehensive health report"""
    try:
        report = medical_analyzer.generate_health_report(
            request.lab_data,
            request.patient_info
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conditions/common")
async def get_common_conditions():
    """Get information about common medical conditions"""
    conditions = [
        {
            "name": "Type 2 Diabetes",
            "description": "Chronic condition affecting blood sugar regulation",
            "common_symptoms": ["Increased thirst", "Frequent urination", "Fatigue"],
            "prevalence": "Common"
        },
        {
            "name": "Hypertension",
            "description": "High blood pressure",
            "common_symptoms": ["Often asymptomatic", "Headaches", "Shortness of breath"],
            "prevalence": "Very Common"
        },
        {
            "name": "Hyperlipidemia",
            "description": "High cholesterol and triglycerides",
            "common_symptoms": ["Usually asymptomatic"],
            "prevalence": "Common"
        },
        {
            "name": "Coronary Artery Disease",
            "description": "Narrowing of heart arteries",
            "common_symptoms": ["Chest pain", "Shortness of breath", "Fatigue"],
            "prevalence": "Common"
        }
    ]
    return conditions

@router.post("/trends/analyze")
async def analyze_trends(historical_data: List[dict]):
    """Analyze trends from historical health data"""
    try:
        trends = medical_analyzer.generate_trend_analysis(historical_data)
        return trends
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))