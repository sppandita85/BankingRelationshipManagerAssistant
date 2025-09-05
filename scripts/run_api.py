"""
Script to run the FastAPI server.
"""
import subprocess
import sys
import os

def run_api():
    """Run the FastAPI server."""
    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", "src.banking_rm_agent.interfaces.api_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nAPI server stopped.")
    except Exception as e:
        print(f"Error running API server: {e}")

if __name__ == "__main__":
    run_api()
