if __name__ == "__main__":
    from syncedlyrics import search
    from colorama import Fore
    from time import sleep
    from shutil import get_terminal_size
    from yt_dlp import YoutubeDL
    from pydub import AudioSegment
    from pydub.playback import play
    from threading import Thread
    from re import findall
    import os

    get_video_id = lambda url : url.split("watch?v=")[1].split("&")[0] if "&" in url else url.split("watch?v=")[1]

    if not os.path.isdir("./cache"):
        os.mkdir("cache")

    url = input(
        "Enter YT Music URL from https://music.youtube.com : \n - "
    )
    print(get_video_id(url))
    if os.path.isfile(f"./cache/{get_video_id(url)}.m4a") and os.path.isfile(f"./cache/{get_video_id(url)}.lrc"):
        path = f"./cache/{get_video_id(url)}.m4a"
        with open(f"./cache/{get_video_id(url)}.lrc", "r", encoding="utf-8") as f:
            lrc = f.read()
    
    else:
        info = YoutubeDL({"format": "bestaudio[ext=m4a]", "outtmpl": "./cache/%(id)s.m4a"}).extract_info(
            url, download=True
        )
        title = info.get('title')
        artist = info.get('uploader')
        path = "./cache/"+info.get('id')+".m4a"

        lrc = search(f"{title} {artist}", allow_plain_format=True, save_path=f"./cache/{info.get('id')}.lrc")

    d, v, count = [], [], 0
    for i in lrc.splitlines():
        if i:
            time_ = i.split("[")[1].split("]")[0].strip()
            if not findall("[a-zA-Z]+", time_):
                minute, seconds = int(time_.split(":")[0]), float(time_.split(":")[1])
                d.append([minute*60+seconds, "♪" if i.split("]")[1] == " " else i.split("]")[1], count])
                count += 1

    print("\033c", end="")
    audio = AudioSegment.from_file(path)
    Thread(target=play, args=(audio,)).start()
    columns = get_terminal_size().columns
    print("\033c", end="")
    count = 1
    for i in d:
        if count == 15: break
        print((Fore.LIGHTBLACK_EX + i[1]).center(columns)); count+=1
    for i in d:
        if i[2] == 0:
            sleep(i[0])
            print("\033c", end="")
        else:
            print((Fore.LIGHTBLACK_EX + d[d.index(i) - 1][1]).center(columns))
        print((Fore.WHITE + i[1]).center(columns)); v.append(i[2])
        count = 1
        for x in d:
            if count == 15: break
            if x[2] not in v: print((Fore.LIGHTBLACK_EX + x[1]).center(columns)); count += 1
        try:
            sleep(d[d.index(i) + 1][0] - i[0])
        except:
            pass
        print("\033c", end="")
