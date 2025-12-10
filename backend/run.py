#!/usr/bin/env python3
"""
Alternative startup script for Mediclinic AI Dashboard
"""

import uvicorn
import argparse
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI server"""
    
    print(f"""
    ╔══════════════════════════════════════════════════════╗
    ║     Mediclinic AI Dashboard - Starting Server        ║
    ╚══════════════════════════════════════════════════════╝
    
    🚀 Server starting...
    📍 Host: {host}
    🚪 Port: {port}
    🔄 Reload: {reload}
    
    📚 API Documentation: http://{host}:{port}/api/docs
    🏥 Health Check: http://{host}:{port}/health
    🎯 Demo Data: http://{host}:{port}/demo/data
    
    Press Ctrl+C to stop the server
    """)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mediclinic AI Dashboard Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--prod", action="store_true", help="Production mode")
    
    args = parser.parse_args()
    
    # Adjust settings for production
    if args.prod:
        args.reload = False
        print("⚠️  Running in production mode")
    
    run_server(args.host, args.port, args.reload)