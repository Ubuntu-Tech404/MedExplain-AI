from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class ExplanationRequest(BaseModel):
    """Request model for medical text explanation"""
    text: str = Field(..., description="Medical text to explain")
    context: Optional[str] = Field("", description="Additional context")
    language: str = Field("english", description="Output language")
    simplify_level: str = Field("patient", description="Simplification level (patient, student, professional)")
    include_examples: bool = Field(True, description="Include examples in explanation")
    max_length: Optional[int] = Field(500, description="Maximum explanation length")

class DiagnosisRequest(BaseModel):
    """Request model for diagnosis explanation"""
    diagnosis: str = Field(..., description="Medical diagnosis to explain")
    notes: Optional[str] = Field("", description="Doctor's notes or additional information")
    patient_age: Optional[int] = Field(None, ge=0, le=120, description="Patient age")
    patient_gender: Optional[str] = Field(None, description="Patient gender")
    include_treatments: bool = Field(True, description="Include treatment options")
    include_prognosis: bool = Field(True, description="Include prognosis information")
    include_prevention: bool = Field(True, description="Include prevention strategies")

class LabAnalysisRequest(BaseModel):
    """Request model for lab result analysis"""
    lab_data: Dict[str, float] = Field(..., description="Laboratory test results")
    patient_info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Patient information")
    previous_results: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Previous lab results for comparison")
    include_trends: bool = Field(True, description="Include trend analysis")
    include_recommendations: bool = Field(True, description="Include recommendations")
    alert_threshold: float = Field(0.2, description="Threshold for critical alerts")

class MedicationExplanationRequest(BaseModel):
    """Request model for medication explanation"""
    medication_name: str = Field(..., description="Medication name")
    dosage: Optional[str] = Field("", description="Medication dosage")
    frequency: Optional[str] = Field("", description="Administration frequency")
    patient_conditions: Optional[List[str]] = Field(default_factory=list, description="Patient's medical conditions")
    include_interactions: bool = Field(True, description="Include drug interactions")
    include_side_effects: bool = Field(True, description="Include side effects")
    include_contraindications: bool = Field(True, description="Include contraindications")

class SymptomAnalysisRequest(BaseModel):
    """Request model for symptom analysis"""
    symptoms: List[str] = Field(..., min_items=1, description="List of symptoms")
    duration_days: Optional[int] = Field(None, ge=1, description="Duration of symptoms in days")
    severity: Optional[str] = Field("mild", description="Symptom severity")
    patient_info: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Patient information")
    include_possible_conditions: bool = Field(True, description="Include possible conditions")
    include_when_to_seek_help: bool = Field(True, description="Include when to seek medical help")
    include_home_remedies: bool = Field(True, description="Include home remedies")

class HealthReportRequest(BaseModel):
    """Request model for health report generation"""
    patient_id: str = Field(..., description="Patient ID")
    include_labs: bool = Field(True, description="Include lab results")
    include_medications: bool = Field(True, description="Include medications")
    include_documents: bool = Field(False, description="Include document summaries")
    include_vitals: bool = Field(True, description="Include vital signs")
    time_period_days: Optional[int] = Field(365, ge=1, description="Time period to include")
    format: str = Field("summary", description="Report format (summary, detailed, printable)")
    language: str = Field("english", description="Report language")

class ChartGenerationRequest(BaseModel):
    """Request model for chart generation"""
    chart_type: str = Field(..., description="Type of chart to generate")
    data: Dict[str, Any] = Field(..., description="Chart data")
    title: Optional[str] = Field(None, description="Chart title")
    width: int = Field(800, description="Chart width in pixels")
    height: int = Field(500, description="Chart height in pixels")
    color_scheme: str = Field("medical", description="Color scheme")
    include_annotations: bool = Field(True, description="Include annotations")

class RiskAssessmentRequest(BaseModel):
    """Request model for risk assessment"""
    patient_data: Dict[str, Any] = Field(..., description="Patient data including labs, vitals, etc.")
    assessment_type: str = Field("cardiovascular", description="Type of risk assessment")
    include_prevention: bool = Field(True, description="Include prevention strategies")
    include_comparison: bool = Field(False, description="Include comparison to population averages")
    timeframe_years: int = Field(10, ge=1, le=30, description="Timeframe for risk assessment")

class TreatmentComparisonRequest(BaseModel):
    """Request model for treatment comparison"""
    diagnosis: str = Field(..., description="Medical diagnosis")
    treatments: List[str] = Field(..., min_items=2, description="Treatments to compare")
    patient_profile: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Patient profile")
    comparison_criteria: List[str] = Field(default_factory=list, description="Criteria for comparison")
    include_cost: bool = Field(False, description="Include cost comparison")
    include_success_rates: bool = Field(True, description="Include success rates")

class MedicationInteractionRequest(BaseModel):
    """Request model for medication interaction check"""
    medications: List[str] = Field(..., min_items=2, description="List of medications to check")
    patient_conditions: Optional[List[str]] = Field(default_factory=list, description="Patient conditions")
    include_severity: bool = Field(True, description="Include interaction severity")
    include_alternative: bool = Field(True, description="Include alternative suggestions")

class HealthRecommendationRequest(BaseModel):
    """Request model for health recommendations"""
    patient_data: Dict[str, Any] = Field(..., description="Patient health data")
    goal_type: str = Field("general", description="Type of health goal")
    timeframe: str = Field("short_term", description="Timeframe for recommendations")
    include_specifics: bool = Field(True, description="Include specific recommendations")
    include_resources: bool = Field(True, description="Include additional resources")

class AIResponse(BaseModel):
    """Base model for AI responses"""
    success: bool = Field(..., description="Whether the request was successful")
    data: Dict[str, Any] = Field(..., description="Response data")
    message: Optional[str] = Field(None, description="Additional message")
    model_used: Optional[str] = Field(None, description="AI model used")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    suggestion: Optional[str] = Field(None, description="Suggested solution")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")