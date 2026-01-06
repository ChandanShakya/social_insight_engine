#!/bin/bash
# Start the backend server

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup first..."
    ./setup.sh
fi

source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
