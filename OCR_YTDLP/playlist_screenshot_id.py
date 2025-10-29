from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import argparse
import datetime

def ocr_playlist_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.point(lambda x: 0 if x < 128 else 255, 'L')
    img = ImageEnhance.Contrast(img).enhance(2)

    custom_config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)

    # Collect all words with positions
    words_with_pos = []
    for i, word in enumerate(data['text']):
        if not word.strip() or int(data['conf'][i]) < 30:
            continue
        words_with_pos.append({
            'text': word.strip(),
            'left': data['left'][i],
            'top': data['top'][i],
            'width': data['width'][i],
            'height': data['height'][i]
        })

    if not words_with_pos:
        print("⚠️ No words detected")
        return []

    # Detect column boundary (find the large horizontal gap)
    left_positions = sorted(set(w['left'] for w in words_with_pos))
    if len(left_positions) < 2:
        print("⚠️ Could not detect two columns")
        return []
    
    # Find the midpoint or largest gap
    gaps = [(left_positions[i+1] - left_positions[i], left_positions[i]) 
            for i in range(len(left_positions)-1)]
    column_boundary = max(gaps, key=lambda x: x[0])[1] + max(gaps, key=lambda x: x[0])[0] // 2

    # Separate into left (titles) and right (artists) columns
    left_column = [w for w in words_with_pos if w['left'] < column_boundary]
    right_column = [w for w in words_with_pos if w['left'] >= column_boundary]

    # Group by rows within each column
    def group_by_rows(words, tolerance=10):
        rows = {}
        for w in words:
            matched = False
            for top in rows:
                if abs(top - w['top']) < tolerance:
                    rows[top].append(w)
                    matched = True
                    break
            if not matched:
                rows[w['top']] = [w]
        return rows

    left_rows = group_by_rows(left_column)
    right_rows = group_by_rows(right_column)

    # Pair titles with artists based on vertical alignment
    songs = []
    for left_top in sorted(left_rows.keys()):
        title_words = sorted(left_rows[left_top], key=lambda x: x['left'])
        title = " ".join(w['text'] for w in title_words)
        
        # Find closest right column row
        closest_artist = ""
        min_distance = float('inf')
        for right_top in right_rows:
            distance = abs(right_top - left_top)
            if distance < min_distance:
                min_distance = distance
                artist_words = sorted(right_rows[right_top], key=lambda x: x['left'])
                closest_artist = " ".join(w['text'] for w in artist_words)
        
        if title and closest_artist:
            songs.append(f"{title} - {closest_artist}")
            print(f"{title} - {closest_artist}")

    return songs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to the input file.")
    args = parser.parse_args()
    screenshot_path = args.input_file
    extracted_songs = ocr_playlist_image(screenshot_path)

    current_datetime = datetime.datetime.now()
    datetime_string = current_datetime.strftime("_%Y-%m-%d_%H:%M:%S")
    output_filename = "songs/songs" + datetime_string + ".txt"
    with open(output_filename, "w") as f:
        for song in extracted_songs:
            f.write(song + "\n")

    print(f"Extracted {len(extracted_songs)} songs into songs.txt")
