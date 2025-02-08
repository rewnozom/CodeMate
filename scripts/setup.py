# scripts/setup.py
import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Setup development environment"""
    try:
        # Install dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements/dev.txt"])
        
        # Create necessary directories
        directories = [
            "logs",
            "logs/metrics",
            "logs/errors",
            "temp",
            "temp/cache",
            "temp/workflow_states",
            "workspace"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
        print("Environment setup completed successfully")
        
    except Exception as e:
        print(f"Error setting up environment: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_environment()