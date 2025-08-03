#!/bin/bash
echo "🚀 Starting PropAI Full Stack..."
echo "Backend: http://localhost:5001"
echo "Frontend: http://localhost:3000"
echo ""

# Start backend in background
cd backend && npm start &
BACKEND_PID=$!

# Start frontend in background
cd ../frontend && npm start &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 