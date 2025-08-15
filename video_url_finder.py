import yt_dlp
import datetime
import argparse

def get_first_youtube_result(query):
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query} official audio -live -cover", download=False)
        if "entries" in info and len(info["entries"]) > 0:
            return info["entries"][0]["webpage_url"]
    return None
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    input_filename = args.filename
    with open(input_filename, 'r') as file:
        songs = file.readlines()
    urls = ""
    for song in songs:
        # get url (str) and append data to output string
        url = get_first_youtube_result(song)
        if url is None:
            print(f"No URL found for {song}")
            continue
        print(f"{song} → {url}")
        urls += str(url + "\n")

    # output song url data to txt file
    # use datetime data in filename to record run instances for testing and validation
    current_datetime = datetime.datetime.now()
    datetime_string = current_datetime.strftime("_%Y-%m-%d_%H:%M:%S")
    output_filename = "urls/urls" + datetime_string + ".txt"
    with open(output_filename, 'w') as f:
        f.write(urls)
