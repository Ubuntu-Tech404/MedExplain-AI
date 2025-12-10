"""
Health check endpoints and monitoring
"""

from typing import Dict, Any, List
from datetime import datetime
import logging
from fastapi import APIRouter

from config import settings
from services.llama_service import LlamaMedicalService
from database import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])

class HealthChecker:
    """Health check service"""
    
    def __init__(self):
        self.llama_service = LlamaMedicalService()
        self.checks = [
            self.check_database,
            self.check_llama_model,
            self.check_storage,
            self.check_services,
        ]
    
    def check_database(self) -> Dict[str, Any]:
        """Check database connection"""
        try:
            db_status = db.health_check()
            return {
                "service": "database",
                "status": db_status.get("status", "unknown"),
                "details": db_status,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "service": "database",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_llama_model(self) -> Dict[str, Any]:
        """Check Llama model status"""
        try:
            if self.llama_service.model_loaded:
                return {
                    "service": "llama_model",
                    "status": "healthy",
                    "model": settings.hf_model_name,
                    "loaded": True,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "service": "llama_model",
                    "status": "degraded",
                    "model": settings.hf_model_name,
                    "loaded": False,
                    "warning": "Model not loaded, using fallback",
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Llama model health check failed: {e}")
            return {
                "service": "llama_model",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_storage(self) -> Dict[str, Any]:
        """Check storage availability"""
        try:
            import os
            import shutil
            
            # Check upload directory
            upload_dir = settings.upload_dir
            os.makedirs(upload_dir, exist_ok=True)
            
            # Test write permission
            test_file = os.path.join(upload_dir, ".health_check")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            
            # Get disk usage
            total, used, free = shutil.disk_usage(upload_dir)
            
            return {
                "service": "storage",
                "status": "healthy",
                "upload_dir": upload_dir,
                "disk_space": {
                    "total_gb": round(total / (1024**3), 2),
                    "used_gb": round(used / (1024**3), 2),
                    "free_gb": round(free / (1024**3), 2),
                    "free_percent": round((free / total) * 100, 2)
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Storage health check failed: {e}")
            return {
                "service": "storage",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def check_services(self) -> Dict[str, Any]:
        """Check external services"""
        services_status = []
        
        # Check Hugging Face API
        try:
            import requests
            response = requests.get("https://huggingface.co/api/health", timeout=5)
            services_status.append({
                "service": "huggingface_api",
                "status": "healthy" if response.status_code == 200 else "degraded",
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            services_status.append({
                "service": "huggingface_api",
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        return {
            "service": "external_services",
            "status": "healthy" if all(s["status"] == "healthy" for s in services_status) else "degraded",
            "services": services_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = []
        overall_status = "healthy"
        
        for check in self.checks:
            try:
                result = check()
                results.append(result)
                
                if result["status"] != "healthy":
                    overall_status = "degraded"
                    
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                results.append({
                    "service": "unknown",
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                overall_status = "degraded"
        
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "environment": settings.environment,
            "version": settings.app_version,
            "checks": results
        }

# Create health checker instance
health_checker = HealthChecker()

@router.get("/")
async def health_check():
    """Comprehensive health check endpoint"""
    return health_checker.run_all_checks()

@router.get("/simple")
async def simple_health_check():
    """Simple health check - just returns status"""
    checks = health_checker.run_all_checks()
    return {"status": checks["status"]}

@router.get("/readiness")
async def readiness_check():
    """Readiness check for Kubernetes/containers"""
    checks = health_checker.run_all_checks()
    is_ready = checks["status"] in ["healthy", "degraded"]
    
    return {
        "ready": is_ready,
        "status": checks["status"],
        "timestamp": datetime.now().isoformat()
    }

@router.get("/liveness")
async def liveness_check():
    """Liveness check for Kubernetes/containers"""
    return {
        "alive": True,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/version")
async def version_info():
    """Get version information"""
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "python_version": "3.8+",
        "api_version": "v2",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/status")
async def status_check():
    """Get detailed status information"""
    import psutil
    import platform
    
    # System information
    system_info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "disk_usage_percent": psutil.disk_usage('/').percent,
    }
    
    # Process information
    process = psutil.Process()
    process_info = {
        "pid": process.pid,
        "name": process.name(),
        "memory_mb": round(process.memory_info().rss / (1024**2), 2),
        "cpu_percent": process.cpu_percent(),
        "threads": process.num_threads(),
        "uptime_seconds": round((datetime.now() - datetime.fromtimestamp(process.create_time())).total_seconds(), 2)
    }
    
    # Combine with health checks
    health_status = health_checker.run_all_checks()
    
    return {
        **health_status,
        "system": system_info,
        "process": process_info,
        "settings": {
            "debug": settings.debug,
            "demo_mode": settings.demo_mode,
            "model_loaded": health_checker.llama_service.model_loaded
        }
    }