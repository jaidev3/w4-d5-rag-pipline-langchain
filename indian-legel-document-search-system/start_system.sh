#!/bin/bash

# Indian Legal Document Search System - Startup Script

echo "🚀 Starting Indian Legal Document Search System..."
echo "================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ to continue."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 to continue."
    exit 1
fi

# Install requirements if not already installed
echo "📦 Installing requirements..."
pip3 install -r requirements.txt

# Create logs directory
mkdir -p logs

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down services..."
    if [[ ! -z "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [[ ! -z "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "✅ Services stopped."
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start FastAPI backend
echo "🔧 Starting FastAPI backend..."
cd backend
python3 main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend started successfully on http://localhost:8000"
else
    echo "❌ Failed to start backend. Check logs/backend.log for details."
    cleanup
    exit 1
fi

# Start Streamlit frontend
echo "🎨 Starting Streamlit frontend..."
cd frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 5

# Check if frontend is running
if curl -s http://localhost:8501/ > /dev/null; then
    echo "✅ Frontend started successfully on http://localhost:8501"
else
    echo "❌ Failed to start frontend. Check logs/frontend.log for details."
    cleanup
    exit 1
fi

echo ""
echo "🎉 System started successfully!"
echo "================================================="
echo "🌐 Web Interface: http://localhost:8501"
echo "🔧 API Backend: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo "📝 Logs: logs/backend.log, logs/frontend.log"
echo ""
echo "Press Ctrl+C to stop the system"
echo "================================================="

# Keep the script running
wait 