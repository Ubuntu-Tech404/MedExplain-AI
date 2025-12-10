import time
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request/response logging"""
    
    async def dispatch(self, request: Request, call_next):
        # Log request
        start_time = time.time()
        
        # Get request body for logging (excluding large uploads)
        body = await self._get_request_body(request)
        
        logger.info(f"Request: {request.method} {request.url.path} | Body: {body}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.3f}s"
        )
        
        # Add headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    
    async def _get_request_body(self, request: Request) -> Dict[str, Any]:
        """Extract request body for logging"""
        try:
            # Skip body extraction for large files
            content_type = request.headers.get("content-type", "")
            if "multipart/form-data" in content_type:
                return {"type": "file_upload"}
            
            # Read body
            body_bytes = await request.body()
            if not body_bytes:
                return {}
            
            # Try to parse as JSON
            try:
                return json.loads(body_bytes.decode())
            except:
                return {"raw_body": body_bytes[:500].decode()}  # First 500 chars
        
        except Exception as e:
            logger.error(f"Error reading request body: {e}")
            return {"error": "could_not_read_body"}

class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware for security headers"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for error handling"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled error: {e}", exc_info=True)
            
            # Return JSON error response
            error_response = {
                "error": "internal_server_error",
                "message": "An internal server error occurred",
                "request_id": request.headers.get("X-Request-ID", "unknown")
            }
            
            return Response(
                content=json.dumps(error_response),
                status_code=500,
                media_type="application/json"
            )