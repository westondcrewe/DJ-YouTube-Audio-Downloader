import yt_dlp
import datetime
import argparse
import time
import os

# YOUTUBE_WATCH = "https://www.youtube.com/watch?v="

# def get_first_youtube_result(query):
#     # We only need URLs, not media. Use flat extraction to avoid format resolution.
#     ydl_opts = {
#         "quiet": True,
#         "skip_download": True,
#         "no_warnings": True,
#         "ignoreerrors": True,
#         # Flat extraction returns lightweight entries (id, title, etc.) without formats
#         # so yt-dlp never tries to pick unavailable formats.
#         "extract_flat": True,
#         "noplaylist": True,
#         # Optional: make yt-dlp treat bare strings as ytsearch
#         "default_search": "ytsearch",
#     }

#     search_queries = [
#         f"ytsearch1:{query}",
#         f"ytsearch1:{query} official audio",
#         f"ytsearch1:{query} audio",
#         # extra fallback that often helps when titles are messy:
#         f"ytsearchdate1:{query}",
#     ]

#     for search_query in search_queries:
#         try:
#             print(f"  🔍 Searching: {search_query}")
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(search_query, download=False)
#             if not info or "entries" not in info or not info["entries"]:
#                 continue

#             entry = info["entries"][0]
#             # In flat mode, you’ll usually get an 'id' and sometimes 'url' or 'webpage_url'
#             video_id = entry.get("id")
#             webpage_url = entry.get("webpage_url") or entry.get("url")

#             if webpage_url and webpage_url.startswith("http"):
#                 print(f"  ✓ Found: {entry.get('title', 'Unknown')}")
#                 return webpage_url
#             if video_id:  # construct watch URL ourselves
#                 print(f"  ✓ Found: {entry.get('title', 'Unknown')}")
#                 return f"{YOUTUBE_WATCH}{video_id}"

#         except Exception as e:
#             print(f"  ⚠️ Search failed: {str(e)[:120]}")
#             continue

#     return None

import unicodedata
import re

YOUTUBE_WATCH = "https://www.youtube.com/watch?v="

def _normalize_query(raw: str) -> str:
    # Normalize Unicode (turn fancy dashes/quotes into simple ASCII equivalents)
    s = unicodedata.normalize("NFKC", raw)
    # Replace common unicode dashes with ASCII hyphen
    s = s.replace("–", "-").replace("—", "-")
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()
    return s

def _simple_score(query: str, title: str, uploader: str | None) -> float:
    """
    Very lightweight scoring: token overlap + small bonus if uploader hints at 'Official' or matches artist.
    You can swap this for rapidfuzz if you want stronger scoring.
    """
    q = query.lower()
    t = (title or "").lower()
    u = (uploader or "").lower()

    # Token overlap
    q_tokens = set(re.findall(r"\w+", q))
    t_tokens = set(re.findall(r"\w+", t))
    overlap = len(q_tokens & t_tokens) / max(1, len(q_tokens))

    bonus = 0.0
    if "official" in t or "official" in u:
        bonus += 0.05
    # Light nudge if uploader contains a likely artist token (left of dash)
    artist_guess = q.split(" - ")[-1] if " - " in q else q.split("-")[-1]
    artist_guess = artist_guess.strip().lower()
    if artist_guess and artist_guess in u:
        bonus += 0.05

    # Prefer non-live, non-lyrics slightly if the query said "official audio"
    if "official audio" in q and ("live" in t or "lyrics" in t):
        bonus -= 0.05

    return overlap + bonus

def get_first_youtube_result(query: str):
    q_raw = query
    q = _normalize_query(q_raw)

    # Debug print to catch hidden characters
    print(f"  🔎 Query (normalized): {q!r}")
    print("  🧪 Hex bytes:", q.encode("utf-8").hex())  # lets you see odd bytes if any

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "extract_flat": True,   # important: avoids format selection
        "noplaylist": True,
        "default_search": "ytsearch",
    }

    # pull top 10; we’ll pick the best
    search_strings = [
        f"ytsearch10:{q}",
        f"ytsearch10:{q} official audio",
        f"ytsearch10:{q} audio",
    ]

    best = None
    best_score = -1.0

    for s in search_strings:
        print(f"  🔍 Searching: {s}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(s, download=False)
        except Exception as e:
            print("  ⚠️ search error:", str(e)[:160])
            continue

        if not info or "entries" not in info:
            continue

        for e in (info["entries"] or []):
            if not e:
                continue
            vid = e.get("id")
            title = e.get("title")
            uploader = e.get("uploader") or e.get("uploader_id") or ""
            url = e.get("webpage_url") or e.get("url") or (YOUTUBE_WATCH + vid if vid else None)
            if not url or not vid or not title:
                continue

            score = _simple_score(q, title, uploader)
            if score > best_score:
                best_score = score
                best = (title, url)

        # If we already found a good score, we can break early
        if best_score >= 0.8:
            break

    if best:
        print(f"  ✓ Picked: {best[0]}  (score={best_score:.3f})")
        return best[1]

    print("  ❌ No acceptable match found")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    args = parser.parse_args()
    input_filename = args.filename

    with open(input_filename, "r") as file:
        songs = [line.strip() for line in file if line.strip()]

    print(f"\n{'='*60}")
    print(f"Processing {len(songs)} songs...")
    print(f"{'='*60}\n")

    urls = []
    failed_songs = []

    for i, song in enumerate(songs, 1):
        print(f"[{i}/{len(songs)}] {song}")
        url = get_first_youtube_result(song)

        if url:
            print(f"  ✅ Success: {url}\n")
            urls.append(f"{song}|{url}")
        else:
            print(f"  ❌ Failed to find URL\n")
            failed_songs.append(song)

        if i < len(songs):
            time.sleep(args.delay)

    current_datetime = datetime.datetime.now()
    datetime_string = current_datetime.strftime("_%Y-%m-%d_%H:%M:%S")

    os.makedirs("urls", exist_ok=True)

    if urls:
        output_filename = f"urls/urls{datetime_string}.txt"
        with open(output_filename, "w") as f:
            f.write("\n".join(u.split("|", 1)[1] for u in urls))

    print(f"\n{'='*60}")
    print(f"RESULTS:")
    print(f"{'='*60}")
    print(f"✅ Successfully found: {len(urls)}/{len(songs)} songs")
    print(f"❌ Failed to find: {len(failed_songs)}/{len(songs)} songs")

    if urls:
        print(f"\n📁 Output saved to: {output_filename}")

    print(f"\n{'='*60}")
