from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import argparse
import datetime

def ocr_playlist_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.filter(ImageFilter.MedianFilter())
    img = ImageEnhance.Contrast(img).enhance(2)

    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    rows = {}
    for i, word in enumerate(data['text']):
        if int(data['conf'][i]) < 50 or not word.strip():
            continue  # skip low-confidence or empty words
        top = data['top'][i]
        left = data['left'][i]
        if top not in rows:
            rows[top] = []
        rows[top].append((left, word.strip()))

    # Process rows: separate left/right
    songs = []
    for top in sorted(rows.keys()):
        words = rows[top]
        # Sort words by X position
        words.sort(key=lambda x: x[0])
        # Split left/right roughly by midpoint of image
        midpoint = img.width // 2
        title = " ".join(w for l, w in words if l < midpoint)
        artist = " ".join(w for l, w in words if l >= midpoint)

        # Clean stray characters
        title = re.sub(r"\s(E|G|F|H)\s", "", title)
        artist = re.sub(r"\s(E|G|F|H)\s", "", artist)

        if title and artist:
            songs.append(f"{title} - {artist}")
            print(f"{title} - {artist}")

    return songs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    screenshot_path = args.filename
    print(f"{screenshot_path=}")
    extracted_songs = ocr_playlist_image(screenshot_path)

    current_datetime = datetime.datetime.now()
    datetime_string = current_datetime.strftime("_%Y-%m-%d_%H:%M:%S")
    output_filename = "songs/songs" + datetime_string + ".txt"
    with open(output_filename, "w") as f:
        for song in extracted_songs:
            print(f"{song}")
            f.write(song + "\n")

    print(f"Extract {len(extracted_songs)} songs into songs.txt")
