from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from datetime import datetime
import json

from services.visualization_service import VisualizationService
from services.medical_analyzer import MedicalAnalyzer
from services.supabase_service import SupabaseService

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

visualization_service = VisualizationService()
medical_analyzer = MedicalAnalyzer()
supabase_service = SupabaseService()

@router.post("/charts/generate")
async def generate_chart(chart_request: Dict):
    """Generate medical chart"""
    try:
        chart_type = chart_request.get("type", "blood_work")
        data = chart_request.get("data", {})
        
        chart_result = visualization_service.generate_chart(chart_type, data)
        return chart_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/health/score")
async def calculate_health_score(lab_data: Dict):
    """Calculate overall health score from lab results"""
    try:
        health_score = medical_analyzer.calculate_health_score(lab_data)
        return health_score
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/risk/assess")
async def assess_risk(lab_data: Dict, patient_info: Optional[Dict] = None):
    """Assess health risks from lab data"""
    try:
        risk_assessment = medical_analyzer.detect_risk_factors(
            lab_data,
            patient_info.get("age", 50) if patient_info else 50
        )
        
        # Add visualization
        risk_chart = visualization_service.generate_chart("risk_assessment", {
            "risks": [
                {"category": risk["condition"], "score": 80 if risk["risk_level"] == "high" else 60}
                for risk in risk_assessment.get("detected_risks", [])
            ]
        })
        
        return {
            "risk_assessment": risk_assessment,
            "visualization": risk_chart,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/patient/{patient_id}/summary")
async def get_patient_summary(patient_id: str):
    """Get comprehensive patient health summary"""
    try:
        # Get patient profile
        profile = supabase_service.get_patient_profile(patient_id)
        
        # Get lab history
        lab_history = supabase_service.get_lab_history(patient_id, limit=5)
        
        # Get medications
        medications = supabase_service.get_medications(patient_id)
        
        # Get recent documents
        documents = supabase_service.get_patient_documents(patient_id)
        
        # Get upcoming appointments
        appointments = supabase_service.get_appointments(patient_id, upcoming=True)
        
        # Analyze latest lab if available
        latest_analysis = {}
        if lab_history and len(lab_history) > 0:
            latest_labs = lab_history[0].get("lab_data", {})
            latest_analysis = medical_analyzer.categorize_lab_results(latest_labs)
        
        # Calculate overall health score
        health_score = {"score": 0, "status": "Insufficient Data"}
        if latest_analysis:
            health_score = medical_analyzer.calculate_health_score(
                {k: v.get("value", 0) for k, v in latest_analysis.items() if "value" in v}
            )
        
        # Generate timeline
        timeline_data = []
        
        # Add lab dates
        for lab in lab_history[:3]:  # Last 3 labs
            timeline_data.append({
                "date": lab.get("test_date", datetime.now().isoformat()),
                "event": f"Lab Test: {', '.join(list(lab.get('lab_data', {}).keys())[:3])}",
                "type": "lab",
                "status": "completed"
            })
        
        # Add upcoming appointments
        for appt in appointments[:2]:
            timeline_data.append({
                "date": appt.get("date"),
                "event": f"Appointment: {appt.get('doctor_name', 'Doctor')}",
                "type": "appointment",
                "status": "scheduled"
            })
        
        # Add document uploads
        for doc in documents[:2]:
            timeline_data.append({
                "date": doc.get("uploaded_at"),
                "event": f"Document: {doc.get('filename', 'Document')}",
                "type": "document",
                "status": "completed"
            })
        
        # Sort timeline by date
        timeline_data.sort(key=lambda x: x["date"])
        
        # Generate charts
        charts = {}
        if latest_analysis:
            charts["blood_work"] = visualization_service.generate_chart("blood_work", {
                "results": latest_analysis
            })
        
        if timeline_data:
            charts["timeline"] = visualization_service.generate_chart("health_timeline", {
                "events": timeline_data[-5:]  # Last 5 events
            })
        
        return {
            "patient_id": patient_id,
            "profile": profile,
            "health_score": health_score,
            "latest_analysis": latest_analysis,
            "medications": medications,
            "document_count": len(documents),
            "lab_history_count": len(lab_history),
            "upcoming_appointments": len(appointments),
            "charts": charts,
            "summary_generated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trends")
async def analyze_trends(historical_labs: List[Dict]):
    """Analyze trends from historical lab data"""
    try:
        trends = medical_analyzer.generate_trend_analysis(historical_labs)
        
        # Generate trend chart
        trend_chart_data = {}
        for test, trend_info in trends.get("trends", {}).items():
            trend_chart_data[test] = {
                "values": [trend_info.get("first_value"), trend_info.get("last_value")],
                "dates": [trend_info.get("first_date"), trend_info.get("last_date")]
            }
        
        trend_chart = visualization_service.generate_chart("lab_trends", {
            "trends": trend_chart_data
        })
        
        return {
            "trend_analysis": trends,
            "trend_chart": trend_chart
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/body/systems")
async def analyze_body_systems(lab_data: Dict):
    """Analyze different body systems based on lab results"""
    try:
        # Categorize lab results by system
        categorized = medical_analyzer.categorize_lab_results(lab_data)
        
        # Group by category (body system)
        systems = {}
        for test, data in categorized.items():
            category = data.get("category", "Other")
            if category not in systems:
                systems[category] = {
                    "score": 0,
                    "issues": [],
                    "tests": []
                }
            
            systems[category]["tests"].append({
                "name": test,
                "value": data.get("value"),
                "status": data.get("status_text")
            })
            
            # Add to issues if abnormal
            if data.get("status") in ["warning", "critical"]:
                systems[category]["issues"].append(
                    f"{test}: {data.get('value')} {data.get('unit')} ({data.get('status_text')})"
                )
        
        # Calculate system scores
        for category, data in systems.items():
            # Simple scoring based on test status
            total_tests = len(data["tests"])
            normal_tests = sum(1 for test in data["tests"] if test["status"] == "Normal")
            score = (normal_tests / total_tests) * 100 if total_tests > 0 else 100
            systems[category]["score"] = round(score, 1)
        
        # Generate chart
        chart_data = {
            "systems": systems
        }
        chart = visualization_service.generate_chart("body_systems", chart_data)
        
        return {
            "body_systems": systems,
            "chart": chart,
            "analyzed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/vitals/dashboard")
async def generate_vitals_dashboard(vitals_data: Dict):
    """Generate vital signs dashboard"""
    try:
        dashboard = visualization_service.generate_chart("vital_signs", vitals_data)
        return dashboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))