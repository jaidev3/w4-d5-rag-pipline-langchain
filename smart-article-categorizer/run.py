#!/usr/bin/env python3
"""
Simple runner script for the Smart Article Categorizer
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    print("🚀 Starting Smart Article Categorizer...")
    print("📰 Streamlit UI will be available at: http://localhost:8501")
    print("⚙️  Backend API will be available at: http://localhost:8000 (when implemented)")
    print("=" * 60)
    
    try:
        # Change to the correct directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.serverAddress=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down Smart Article Categorizer...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("💡 Try running: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 