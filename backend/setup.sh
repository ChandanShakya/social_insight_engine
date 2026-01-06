#!/bin/bash
# Setup script for Social Insight Engine Backend

echo "=================================="
echo "Social Insight Engine - Backend Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  WARNING: .env file not found!"
    echo "Please create .env file with your API keys."
    echo "See .env.example in the project root for reference."
    echo ""
    echo "Required variables:"
    echo "  - FB_PAGE_ID"
    echo "  - FB_ACCESS_TOKEN"
    echo "  - GEMINI_API_KEY"
    echo ""
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python -m uvicorn main:app --reload"
echo ""
echo "Or run: ./start.sh"
