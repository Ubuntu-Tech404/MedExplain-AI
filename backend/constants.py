"""
Application Constants
"""

# API Response Messages
API_SUCCESS = "success"
API_ERROR = "error"
API_VALIDATION_ERROR = "validation_error"
API_NOT_FOUND = "not_found"
API_UNAUTHORIZED = "unauthorized"
API_FORBIDDEN = "forbidden"

# Medical Constants
NORMAL_RANGES = {
    "glucose": {"min": 70, "max": 100, "unit": "mg/dL"},
    "hba1c": {"min": 4.0, "max": 5.6, "unit": "%"},
    "cholesterol": {"min": 125, "max": 200, "unit": "mg/dL"},
    "ldl": {"min": 0, "max": 100, "unit": "mg/dL"},
    "hdl": {"min": 40, "max": 60, "unit": "mg/dL"},
    "triglycerides": {"min": 0, "max": 150, "unit": "mg/dL"},
    "creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL"},
    "bun": {"min": 7, "max": 20, "unit": "mg/dL"},
    "sodium": {"min": 135, "max": 145, "unit": "mmol/L"},
    "potassium": {"min": 3.5, "max": 5.0, "unit": "mmol/L"},
}

# Risk Levels
RISK_LEVELS = {
    "low": {"color": "#10B981", "description": "Low risk"},
    "moderate": {"color": "#F59E0B", "description": "Moderate risk"},
    "high": {"color": "#EF4444", "description": "High risk"},
    "critical": {"color": "#7F1D1D", "description": "Critical risk"},
}

# Document Types
DOCUMENT_TYPES = {
    "lab_report": "Laboratory Report",
    "doctor_note": "Doctor's Note",
    "prescription": "Prescription",
    "imaging": "Imaging Report",
    "insurance": "Insurance Document",
    "general": "General Medical",
}

# Chart Types
CHART_TYPES = {
    "blood_work": "Blood Work Analysis",
    "vital_signs": "Vital Signs Dashboard",
    "risk_assessment": "Risk Assessment Radar",
    "health_timeline": "Health Timeline",
    "lab_trends": "Lab Trends Over Time",
    "health_score": "Health Score Gauge",
    "body_systems": "Body Systems Overview",
}

# User Roles
USER_ROLES = {
    "patient": "Patient",
    "doctor": "Healthcare Provider",
    "nurse": "Nursing Staff",
    "admin": "Administrator",
}

# Error Messages
ERROR_MESSAGES = {
    "invalid_credentials": "Invalid email or password",
    "user_not_found": "User not found",
    "token_expired": "Token has expired",
    "token_invalid": "Invalid token",
    "permission_denied": "Permission denied",
    "file_too_large": "File size exceeds maximum allowed",
    "invalid_file_type": "File type not allowed",
    "model_not_loaded": "AI model not loaded",
    "database_error": "Database error occurred",
    "validation_error": "Validation error",
}

# Success Messages
SUCCESS_MESSAGES = {
    "login_success": "Login successful",
    "logout_success": "Logout successful",
    "upload_success": "File uploaded successfully",
    "analysis_success": "Analysis completed successfully",
    "explanation_success": "Explanation generated successfully",
    "update_success": "Update successful",
    "delete_success": "Delete successful",
}

# API Rate Limits
RATE_LIMITS = {
    "default": "100/hour",
    "auth": "10/minute",
    "upload": "20/hour",
    "analysis": "50/hour",
}

# File Size Limits (in bytes)
FILE_SIZE_LIMITS = {
    "pdf": 50 * 1024 * 1024,  # 50MB
    "docx": 10 * 1024 * 1024,  # 10MB
    "image": 5 * 1024 * 1024,  # 5MB
    "text": 1 * 1024 * 1024,  # 1MB
}

# Supported Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "hi": "Hindi",
    "ar": "Arabic",
}

# Health Status Levels
HEALTH_STATUS = {
    "excellent": {"min_score": 85, "color": "#10B981", "description": "Excellent health"},
    "good": {"min_score": 70, "color": "#3B82F6", "description": "Good health"},
    "fair": {"min_score": 50, "color": "#F59E0B", "description": "Fair health"},
    "poor": {"min_score": 0, "color": "#EF4444", "description": "Needs attention"},
}

# Cache TTL (Time to Live in seconds)
CACHE_TTL = {
    "short": 300,  # 5 minutes
    "medium": 3600,  # 1 hour
    "long": 86400,  # 24 hours
}