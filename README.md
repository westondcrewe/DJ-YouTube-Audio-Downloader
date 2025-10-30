# DJ Setlist Downloader

Automatically extract song information from playlist screenshots and download audio files from YouTube. Built for DJs who want to quickly build their library from setlists without manually searching and downloading each track.

## Demo Video
![Watch the Demo Video Here!](djsetlistdownloaderdemosped.gif)

## What It Does

1. **OCR Extraction** - Reads song titles and artists from playlist screenshots
2. **YouTube Search** - Finds the best matching YouTube video for each track
3. **Audio Download** - Downloads high-quality MP3s using yt-dlp

**Success Rate:** ~85% of tracks successfully identified and downloaded

## Requirements

### System Dependencies
- **Python 3.12+**
- **Tesseract OCR** - Required for text extraction from images
  ```bash
  # macOS
  brew install tesseract
  
  # Ubuntu/Debian
  sudo apt-get install tesseract-ocr
  
  # Windows
  # Download from: https://github.com/UB-Mannheim/tesseract/wiki
  ```

### Python Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
Pillow>=10.0.0
pytesseract>=0.3.10
yt-dlp>=2023.0.0
```

## Quick Start

### 1. Setup Project Structure
The script expects these directories (they'll be created automatically if they don't exist):
```
youtube_audio_scraper/
├── screenshots/    # Place your playlist screenshots here
├── songs/          # OCR output (song lists)
├── urls/           # YouTube URLs
├── downloads/      # Final MP3 files
└── tests/          # Test cases
```

### 2. Add Your Screenshot
Place a playlist screenshot in the `screenshots/` folder. The script will automatically use the most recent one.

**Supported Formats:**
- Rekordbox playlists
- Serato playlists  
- Apple Music (desktop)
- Any two-column layout: **Track Title (left)** | **Artist (right)**

### 3. Run the Pipeline
```bash
chmod +x run.sh
./run.sh
```

The script will:
1. Extract songs from your screenshot using OCR
2. Search YouTube for each track
3. Download audio files to `downloads/`

## Project Structure

```
youtube_audio_scraper/
├── playlist_screenshot_id.py   # OCR and song extraction
├── video_url_finder.py         # YouTube URL search
├── audio_scraper.sh            # yt-dlp download script
├── run.sh                      # Main pipeline runner
├── move_downloads.sh           # Utility script
├── screenshots/                # Input images
├── songs/                      # Extracted song lists (timestamped)
├── urls/                       # YouTube URLs (timestamped)
├── downloads/                  # Final MP3 files
└── tests/                      # Test cases
```

## Manual Usage

If you want to run steps individually:

### Step 1: Extract Songs from Screenshot
```bash
python3 playlist_screenshot_id.py screenshots/your_playlist.png
```
Output: `songs/songs_YYYY-MM-DD_HH:MM:SS.txt`

### Step 2: Find YouTube URLs
```bash
python3 video_url_finder.py songs/songs_YYYY-MM-DD_HH:MM:SS.txt
```
Output: `urls/urls_YYYY-MM-DD_HH:MM:SS.txt`

### Step 3: Download Audio
```bash
./audio_scraper.sh urls/urls_YYYY-MM-DD_HH:MM:SS.txt
```
Output: MP3 files in `downloads/`

## Configuration

### Adjust Search Delay (Avoid Rate Limiting)
```bash
python3 video_url_finder.py songs/songs.txt --delay 2.0
```

### OCR Confidence Threshold
Edit `playlist_screenshot_id.py`:
```python
if int(data['conf'][i]) < 30:   # Adjust this value (0-100)
```

## Screenshot Requirements

### Works Best With:
- **Two-column layout** (Title | Artist)
- High contrast text (dark text on light background or vice versa)
- Clear, readable fonts
- Full playlist visible (not cropped)

### Known Limitations:
- Only supports two-column layouts
- Special characters may cause issues
- Very long track names might get truncated
- Live versions and remixes may not match exactly

### Example Screenshot Format:
```
Track Title              | Artist Name
-------------------------|------------------
Desire                   | Chris Stussy
The One (Obskür Remix)   | Chloé Caillet & Luke Aless
Get Stupid               | Julian Fijma
Riva de Biasio          | Chris Stussy
```

## Troubleshooting

### OCR Returns Gibberish
- Increase image contrast
- Try a higher resolution screenshot
- Ensure text is clearly visible
- Check Tesseract installation: `tesseract --version`

### YouTube URLs Not Found
- Check your internet connection
- Songs may have unusual spellings or special characters
- Try manually searching YouTube to verify the track exists
- Check `urls/failed_TIMESTAMP.txt` for failed searches

### Format Error When Downloading
The script has been updated to handle this automatically. If you still see format errors:
```bash
yt-dlp --list-formats [youtube-url]
```

## Roadmap

### Coming Soon:
- [ ] **Accuracy Metrics** - Track success/failure rates
- [ ] **Testing Suite** - Automated testing with sample playlists
- [ ] **Web Frontend** - GUI for easier screenshot upload and management
- [ ] **Spotify API Integration** - Verify song names before YouTube search
- [ ] **Batch Processing** - Handle multiple screenshots at once
- [ ] **Smart Retry** - Automatically retry failed downloads

### Potential Features:
- Support for single-column layouts
- Audio quality selection (320kbps vs 128kbps)
- Playlist metadata export (JSON, CSV)
- Duplicate detection

## Output Files

All output files are timestamped to preserve history:

- `songs/songs_2024-10-30_14:30:00.txt` - Extracted song list
- `urls/urls_2024-10-30_14:32:00.txt` - YouTube URLs
- `urls/urls_detailed_2024-10-30_14:32:00.txt` - URLs with song names
- `urls/failed_2024-10-30_14:32:00.txt` - Songs that couldn't be found
- `downloads/*.mp3` - Final audio files

## Legal Disclaimer

**This tool is for personal use only.** 

- Respect copyright laws in your jurisdiction
- YouTube's Terms of Service prohibit unauthorized downloading
- Use this tool responsibly and ethically
- Consider supporting artists by purchasing music legally

The developers are not responsible for any misuse of this software.

## Contributing

Found a bug? Have a feature suggestion? Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- OCR powered by [Tesseract](https://github.com/tesseract-ocr/tesseract)
- Image processing with [Pillow](https://python-pillow.org/)

---

**Questions?** Open an issue or check the troubleshooting section above.