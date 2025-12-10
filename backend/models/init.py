"""
Medical AI Models Package

This package contains all Pydantic models for the Mediclinic AI Dashboard.
These models are used for data validation, serialization, and type safety.
"""

from .medical_models import (
    PatientProfile,
    MedicalDocument,
    LabResult,
    Medication,
    Appointment,
    HealthMetrics,
    DiagnosisExplanation,
    RiskAssessment,
    MedicalAlert,
    HealthGoal,
    Gender,
    BloodType,
    DocumentType,
    MedicationStatus,
    AppointmentStatus,
    RiskLevel
)

from .ai_models import (
    ExplanationRequest,
    DiagnosisRequest,
    LabAnalysisRequest,
    MedicationExplanationRequest,
    SymptomAnalysisRequest,
    HealthReportRequest,
    ChartGenerationRequest,
    RiskAssessmentRequest,
    TreatmentComparisonRequest,
    MedicationInteractionRequest,
    HealthRecommendationRequest,
    AIResponse,
    ErrorResponse
)

__all__ = [
    # Medical Models
    "PatientProfile",
    "MedicalDocument",
    "LabResult",
    "Medication",
    "Appointment",
    "HealthMetrics",
    "DiagnosisExplanation",
    "RiskAssessment",
    "MedicalAlert",
    "HealthGoal",
    "Gender",
    "BloodType",
    "DocumentType",
    "MedicationStatus",
    "AppointmentStatus",
    "RiskLevel",
    
    # AI Models
    "ExplanationRequest",
    "DiagnosisRequest",
    "LabAnalysisRequest",
    "MedicationExplanationRequest",
    "SymptomAnalysisRequest",
    "HealthReportRequest",
    "ChartGenerationRequest",
    "RiskAssessmentRequest",
    "TreatmentComparisonRequest",
    "MedicationInteractionRequest",
    "HealthRecommendationRequest",
    "AIResponse",
    "ErrorResponse"
]

__version__ = "1.0.0"
__author__ = "Mediclinic AI Team"