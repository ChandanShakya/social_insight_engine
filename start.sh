#!/bin/bash
# Master start script for Social Insight Engine

cd "$(dirname "$0")"

echo "=================================="
echo "Social Insight Engine"
echo "=================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 not found"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js not found"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "❌ npm not found"; exit 1; }

echo "✅ Python 3: $(python3 --version)"
echo "✅ Node.js: $(node --version)"
echo "✅ npm: $(npm --version)"
echo ""

# Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "Setting up backend virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    echo ""
fi

# Check if frontend node_modules exists
if [ ! -d "Frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd Frontend
    npm install
    cd ..
    echo ""
fi

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  WARNING: backend/.env file not found!"
    echo "Please create it with your API keys."
    echo "See .env.example for reference."
    echo ""
    read -p "Press Enter to continue or Ctrl+C to exit..."
    echo ""
fi

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
cd ..

# Start frontend
echo "Starting frontend server..."
cd Frontend
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"
cd ..

echo ""
echo "✅ Servers starting..."
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Backend log: tail -f /tmp/backend.log"
echo "Frontend log: tail -f /tmp/frontend.log"
echo ""
echo "To stop servers: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Waiting for servers to be ready..."
sleep 5

# Test if servers are responding
echo ""
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
fi

if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend failed to start"
fi

echo ""
echo "All done! Open http://localhost:5173 in your browser."
