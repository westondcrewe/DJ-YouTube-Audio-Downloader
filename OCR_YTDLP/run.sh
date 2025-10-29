#!/bin/bash

set -e  # exit on any error

# Config: adjust paths as needed
SCREENSHOTS_DIR="screenshots"
PLAYLIST_SCREENSHOT=$(ls -t "$SCREENSHOTS_DIR"/*.png 2>/dev/null | head -n 1)          # pass screenshot path as first arg
SONGS_DIR="songs"
URLS_DIR="urls"


echo "▶️  Step 1: Extract songs from screenshot at $PLAYLIST_SCREENSHOT..."
python3 playlist_screenshot_id.py "$PLAYLIST_SCREENSHOT"

echo "▶️  Step 2: Find YouTube URLs for songs..."
# Find most recent songs file
SONGS=$(ls -t "$SONGS_DIR"/*.txt 2>/dev/null | head -n 1)
if [ -z "$SONGS" ]; then
  echo "❌ No songs file found in $SONGS_DIR"
  exit 1
fi
echo "✅ Found songs file: $SONGS"

python3 video_url_finder.py "$SONGS"

# Find most recent urls file

echo "▶️  Step 3: Download audio from URLs..."
URLS_FILE=$(ls -t "$URLS_DIR"/*.txt 2>/dev/null | head -n 1)
./audio_scraper.sh "$URLS_FILE"

echo "🎉 Pipeline complete! Songs downloaded to downloads/"
