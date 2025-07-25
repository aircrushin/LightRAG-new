#!/bin/bash

# Start the backend server in the background
echo "Starting backend server..."
python3 -m lightrag.api.lightrag_server &
BACKEND_PID=$!

# Wait a few seconds for the backend to initialize
sleep 3

# Navigate to the frontend directory
echo "Navigating to frontend directory..."
cd lightrag_webui

# Install frontend dependencies
# echo "Installing frontend dependencies with bun..."
# bun install

# Start the frontend development server
echo "Starting frontend development server..."
bun run dev &
FRONTEND_PID=$!

# Function to clean up background processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap script exit and call cleanup
trap cleanup SIGINT SIGTERM

# Wait for both processes to complete
wait $BACKEND_PID
wait $FRONTEND_PID 