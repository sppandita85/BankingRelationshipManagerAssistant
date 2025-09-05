"""
Script to run the Streamlit web interface.
"""
import subprocess
import sys
import os

def run_streamlit():
    """Run the Streamlit application."""
    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "src/banking_rm_agent/interfaces/streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\nStreamlit app stopped.")
    except Exception as e:
        print(f"Error running Streamlit: {e}")

if __name__ == "__main__":
    run_streamlit()
