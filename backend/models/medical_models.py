from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class BloodType(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class DocumentType(str, Enum):
    LAB_REPORT = "lab_report"
    DOCTOR_NOTE = "doctor_note"
    PRESCRIPTION = "prescription"
    IMAGING = "imaging"
    INSURANCE = "insurance"
    GENERAL = "general"

class MedicationStatus(str, Enum):
    ACTIVE = "active"
    DISCONTINUED = "discontinued"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"

class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class PatientProfile(BaseModel):
    """Patient profile model"""
    id: str = Field(..., description="Patient unique identifier")
    name: str = Field(..., description="Patient full name")
    email: str = Field(..., description="Patient email address")
    date_of_birth: datetime = Field(..., description="Date of birth")
    gender: Gender = Field(..., description="Gender")
    blood_type: Optional[BloodType] = Field(None, description="Blood type")
    height_cm: Optional[float] = Field(None, ge=0, le=300, description="Height in centimeters")
    weight_kg: Optional[float] = Field(None, ge=0, le=500, description="Weight in kilograms")
    allergies: List[str] = Field(default_factory=list, description="List of allergies")
    chronic_conditions: List[str] = Field(default_factory=list, description="Chronic medical conditions")
    emergency_contact: Dict[str, str] = Field(default_factory=dict, description="Emergency contact information")
    primary_physician: Optional[str] = Field(None, description="Primary care physician")
    insurance_provider: Optional[str] = Field(None, description="Insurance provider")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

class MedicalDocument(BaseModel):
    """Medical document model"""
    id: str = Field(..., description="Document unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    filename: str = Field(..., description="Original filename")
    document_type: DocumentType = Field(..., description="Type of document")
    file_path: str = Field(..., description="Storage path")
    processed_data: Dict[str, Any] = Field(default_factory=dict, description="Extracted/processed data")
    uploaded_at: datetime = Field(default_factory=datetime.now, description="Upload timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    description: Optional[str] = Field(None, description="Document description")
    file_size_kb: Optional[float] = Field(None, description="File size in KB")

class LabResult(BaseModel):
    """Laboratory test result model"""
    id: str = Field(..., description="Lab result unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    test_date: datetime = Field(..., description="Test date")
    results: Dict[str, float] = Field(..., description="Test results with values")
    reference_ranges: Dict[str, Dict[str, float]] = Field(default_factory=dict, description="Reference ranges for tests")
    units: Dict[str, str] = Field(default_factory=dict, description="Measurement units")
    lab_name: Optional[str] = Field(None, description="Laboratory name")
    ordering_physician: Optional[str] = Field(None, description="Ordering physician")
    analysis: Dict[str, Any] = Field(default_factory=dict, description="Analysis results")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

class Medication(BaseModel):
    """Medication model"""
    id: str = Field(..., description="Medication unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    name: str = Field(..., description="Medication name")
    generic_name: Optional[str] = Field(None, description="Generic name")
    dosage: str = Field(..., description="Dosage amount")
    frequency: str = Field(..., description="Frequency of administration")
    route: Optional[str] = Field(None, description="Route of administration")
    instructions: str = Field("", description="Special instructions")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date if applicable")
    prescribing_doctor: str = Field(..., description="Prescribing doctor")
    pharmacy: Optional[str] = Field(None, description="Pharmacy information")
    status: MedicationStatus = Field(MedicationStatus.ACTIVE, description="Medication status")
    side_effects: List[str] = Field(default_factory=list, description="Reported side effects")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

class Appointment(BaseModel):
    """Medical appointment model"""
    id: str = Field(..., description="Appointment unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    doctor_name: str = Field(..., description="Doctor's name")
    doctor_specialty: Optional[str] = Field(None, description="Doctor's specialty")
    appointment_date: datetime = Field(..., description="Appointment date and time")
    duration_minutes: int = Field(60, ge=15, le=240, description="Appointment duration in minutes")
    reason: str = Field(..., description="Reason for appointment")
    location: str = Field(..., description="Appointment location")
    status: AppointmentStatus = Field(AppointmentStatus.SCHEDULED, description="Appointment status")
    notes: Optional[str] = Field(None, description="Additional notes")
    follow_up_required: bool = Field(False, description="Whether follow-up is required")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

class HealthMetrics(BaseModel):
    """Health metrics/vital signs model"""
    id: str = Field(..., description="Metrics unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    recorded_at: datetime = Field(..., description="Recording timestamp")
    metrics: Dict[str, Any] = Field(..., description="Health metrics dictionary")
    source: str = Field("manual", description="Source of metrics (manual, device, etc.)")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

class DiagnosisExplanation(BaseModel):
    """Diagnosis explanation model"""
    diagnosis: str = Field(..., description="Medical diagnosis")
    simple_explanation: str = Field(..., description="Simple explanation for patients")
    detailed_explanation: Optional[str] = Field("", description="Detailed medical explanation")
    treatment_options: List[str] = Field(default_factory=list, description="Treatment options")
    lifestyle_recommendations: List[str] = Field(default_factory=list, description="Lifestyle recommendations")
    questions_for_doctor: List[str] = Field(default_factory=list, description="Questions to ask doctor")
    severity: Optional[str] = Field(None, description="Condition severity")
    prognosis: Optional[str] = Field(None, description="Expected prognosis")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    model_used: Optional[str] = Field(None, description="AI model used for explanation")

class RiskAssessment(BaseModel):
    """Health risk assessment model"""
    id: str = Field(..., description="Assessment unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    assessed_at: datetime = Field(..., description="Assessment timestamp")
    overall_risk: float = Field(..., ge=0, le=100, description="Overall risk score (0-100)")
    risk_factors: List[Dict[str, Any]] = Field(..., description="List of risk factors")
    recommendations: List[str] = Field(..., description="Risk reduction recommendations")
    next_assessment: Optional[datetime] = Field(None, description="Recommended next assessment date")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

class MedicalAlert(BaseModel):
    """Medical alert/notification model"""
    id: str = Field(..., description="Alert unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    alert_type: str = Field(..., description="Type of alert (critical, warning, info)")
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    related_data: Dict[str, Any] = Field(default_factory=dict, description="Related data")
    priority: str = Field("medium", description="Alert priority")
    acknowledged: bool = Field(False, description="Whether alert has been acknowledged")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")

class HealthGoal(BaseModel):
    """Health goal model"""
    id: str = Field(..., description="Goal unique identifier")
    patient_id: str = Field(..., description="Patient ID")
    goal_type: str = Field(..., description="Type of goal (weight, exercise, medication, etc.)")
    description: str = Field(..., description="Goal description")
    target_value: Optional[float] = Field(None, description="Target value")
    current_value: Optional[float] = Field(None, description="Current value")
    unit: Optional[str] = Field(None, description="Measurement unit")
    start_date: datetime = Field(..., description="Start date")
    target_date: Optional[datetime] = Field(None, description="Target completion date")
    progress_percentage: float = Field(0.0, ge=0, le=100, description="Progress percentage")
    status: str = Field("active", description="Goal status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")