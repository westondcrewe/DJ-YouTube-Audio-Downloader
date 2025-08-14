from PIL import Image
import pytesseract
import datetime
import argparse
import re

def ocr_playlist_image(image_path):
    # Load image
    img = Image.open(image_path)

    # Run OCR - you can experiment with psm and oem modes for better results
    # psm 6 = Assume a single uniform block of text
    text = pytesseract.image_to_string(img, config='--psm 6')

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    songs = []
    # Simple heuristic: pair every two lines as Title + Artist
    for i in range(0, len(lines)-1, 2):
        title = lines[i]
        if re.findall("\s(E|G|F|H)\s", title) is False:
            re.sub("\s(E|G|F|H)\s", "", title)

        artist = lines[i+1]
        print(title, artist)
        songs.append(f"{title} | {artist}\n")

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
