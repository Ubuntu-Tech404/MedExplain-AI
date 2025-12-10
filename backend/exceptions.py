"""
Custom Exceptions for Mediclinic AI Dashboard
"""

class MediclinicException(Exception):
    """Base exception for Mediclinic application"""
    def __init__(self, message: str, code: str = None, status_code: int = 500):
        self.message = message
        self.code = code or "internal_error"
        self.status_code = status_code
        super().__init__(self.message)

class AuthenticationError(MediclinicException):
    """Authentication related errors"""
    def __init__(self, message: str = "Authentication failed", code: str = "auth_error"):
        super().__init__(message, code, 401)

class AuthorizationError(MediclinicException):
    """Authorization related errors"""
    def __init__(self, message: str = "Not authorized", code: str = "authz_error"):
        super().__init__(message, code, 403)

class ValidationError(MediclinicException):
    """Data validation errors"""
    def __init__(self, message: str = "Validation failed", code: str = "validation_error"):
        super().__init__(message, code, 422)

class NotFoundError(MediclinicException):
    """Resource not found errors"""
    def __init__(self, message: str = "Resource not found", code: str = "not_found"):
        super().__init__(message, code, 404)

class ModelError(MediclinicException):
    """AI model related errors"""
    def __init__(self, message: str = "AI model error", code: str = "model_error"):
        super().__init__(message, code, 503)

class DatabaseError(MediclinicException):
    """Database related errors"""
    def __init__(self, message: str = "Database error", code: str = "database_error"):
        super().__init__(message, code, 500)

class FileError(MediclinicException):
    """File operation errors"""
    def __init__(self, message: str = "File operation error", code: str = "file_error"):
        super().__init__(message, code, 400)

class RateLimitError(MediclinicException):
    """Rate limiting errors"""
    def __init__(self, message: str = "Rate limit exceeded", code: str = "rate_limit"):
        super().__init__(message, code, 429)

class ExternalServiceError(MediclinicException):
    """External service errors"""
    def __init__(self, message: str = "External service error", code: str = "external_error"):
        super().__init__(message, code, 502)

class ConfigurationError(MediclinicException):
    """Configuration errors"""
    def __init__(self, message: str = "Configuration error", code: str = "config_error"):
        super().__init__(message, code, 500)

# Utility function to handle exceptions
def handle_exception(exc: Exception):
    """Convert any exception to MediclinicException"""
    if isinstance(exc, MediclinicException):
        return exc
    
    # Convert common exceptions
    if isinstance(exc, ValueError):
        return ValidationError(str(exc))
    elif isinstance(exc, PermissionError):
        return AuthorizationError(str(exc))
    elif isinstance(exc, FileNotFoundError):
        return NotFoundError(str(exc))
    elif isinstance(exc, TimeoutError):
        return ExternalServiceError("Request timeout")
    
    # Default to generic error
    return MediclinicException(str(exc))