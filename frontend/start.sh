#!/bin/bash
# Start the frontend development server

cd "$(dirname "$0")"

if [ ! -d "node_modules" ]; then
    echo "Node modules not found. Running npm install first..."
    npm install
fi

npm run dev
