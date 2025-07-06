#!/bin/bash

echo "Starting LyricStamp..."

# Start Flask server in background
echo "Starting Flask server..."
python3 web_lyricstamp.py &
FLASK_PID=$!

# Wait for Flask server to start
echo "Waiting for Flask server to start..."
for i in {1..30}; do
    if curl -s http://localhost:5734 > /dev/null; then
        echo "Flask server is running!"
        break
    fi
    sleep 1
done

# Open the Tauri app
echo "Opening LyricStamp app..."
open src-tauri/target/release/bundle/macos/lyricstamp.app

# Keep the script running to keep Flask server alive
echo "LyricStamp is running. Press Ctrl+C to stop."
wait $FLASK_PID 