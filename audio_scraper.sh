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
echo "🎵 Starting downloads from $URLS_FILE using cookies..."
cat "$URLS_FILE" | xargs -n 1 -P $MAX_JOBS -I {} yt-dlp \
  --format "bestaudio[ext=m4a]/bestaudio/best" \
  --extract-audio \
  --output "downloads/%(title)s.%(ext)s" \
  --no-overwrites \
  {}

echo "✅ All downloads attempted."
