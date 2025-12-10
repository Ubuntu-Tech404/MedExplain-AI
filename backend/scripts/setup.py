#!/usr/bin/env python3
"""
Setup script for Mediclinic AI Dashboard
"""

import os
import sys
import shutil
from pathlib import Path

def setup_environment():
    """Setup the environment for Mediclinic AI Dashboard"""
    
    print("=" * 60)
    print("Mediclinic AI Dashboard - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print("✓ Python version check passed")
    
    # Create necessary directories
    directories = [
        "static/uploads",
        "static/charts",
        "logs",
        "cache",
        "data",
        "scripts"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Check for .env file
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✓ Created .env file from example")
            print("⚠️  Please edit .env file with your configurations")
        else:
            print("❌ .env.example file not found")
            sys.exit(1)
    else:
        print("✓ .env file already exists")
    
    # Create requirements.txt if not exists
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit the .env file with your configurations")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: python main.py")
    print("4. Access the API at: http://localhost:8000")
    print("=" * 60)

def check_dependencies():
    """Check if all required dependencies are installed"""
    
    print("\nChecking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "transformers",
        "torch",
        "langchain",
        "supabase"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    print("\n✓ All dependencies are installed")
    return True

def generate_secret_key():
    """Generate a secure secret key"""
    import secrets
    
    secret_key = secrets.token_hex(32)
    print("\nGenerated secret key:")
    print(f"SECRET_KEY={secret_key}")
    print("\nAdd this to your .env file")
    return secret_key

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Mediclinic AI Dashboard Setup")
    parser.add_argument("--check", action="store_true", help="Check dependencies only")
    parser.add_argument("--generate-key", action="store_true", help="Generate secret key")
    
    args = parser.parse_args()
    
    if args.generate_key:
        generate_secret_key()
    elif args.check:
        check_dependencies()
    else:
        setup_environment()