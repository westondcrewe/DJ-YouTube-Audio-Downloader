#!/bin/bash

# ===============================
# CONFIGURATION
# ===============================
BROWSER="chrome"            # Change to firefox, brave, edge, etc.
MAX_JOBS=4                  # Parallel downloads (tune based on internet speed)


URLS_FILE=$1
COOKIES_FILE="yt_cookies.txt"

# ===============================
# PREPARE
# ===============================
if [ ! -f "$URLS_FILE" ]; then
    echo "❌ ERROR: $URLS_FILE not found. Run your Python script first."
    exit 1
fi

# ===============================
# EXPORT COOKIES
# Generates dummy cookie from requesting random YouTube video in browser
# ===============================
echo "📥 Exporting cookies from $BROWSER..."
yt-dlp --cookies-from-browser "$BROWSER" --cookies "$COOKIES_FILE" \
       "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
       --skip-download >/dev/null 2>&1

if [ ! -f "$COOKIES_FILE" ]; then
    echo "❌ ERROR: Failed to grab cookies from $BROWSER"
    exit 1
fi

# ===============================
# DOWNLOAD WITH COOKIES
# ===============================
current_datetime=$(date +"%Y-%m-%d_%H:%M:%S")
echo "🎵 Starting downloads from $URLS_FILE using cookies..."
cat "$URLS_FILE" | xargs -n 1 -P $MAX_JOBS -I {} yt-dlp \
  --extract-audio \
  --output "downloads/$current_datetime/%(title)s.%(ext)s" \
  --no-overwrites \
  -q \
  --no-warnings \
  --cookies "$COOKIES_FILE" \
  --extractor-args "youtube:player_client=android" \
  {}

echo "✅ All downloads attempted."