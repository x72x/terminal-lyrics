if __name__ == "__main__":
    import subprocess
    from syncedlyrics import search
    from colorama import Fore
    from time import sleep
    from shutil import get_terminal_size
    from threading import Thread
    from yt_dlp import YoutubeDL

    url = input(
        "Enter YT Music URL from https://music.youtube.com : \n - "
    )
    info = YoutubeDL({"format": "bestaudio[ext=m4a]"}).extract_info(
        url, download=False
    )
    path = info.get('url')
    title = info.get('title')
    artist = info.get('uploader')

    lrc = search(f"{title} {artist}", allow_plain_format=True)
    d, v = [], []
    for i in lrc.splitlines():
        time_ = i.split("[")[1].split("]")[0].strip()
        minute, seconds = int(time_.split(":")[0]), float(time_.split(":")[1])
        d.append([minute*60+seconds, i.split("]")[1]])

    print("\033c", end="")
    func = lambda : subprocess.run(
        args=f'ffplay "{path}"',
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )
    Thread(target=func).start()
    columns = get_terminal_size().columns
    for i in d:
        if d.index(i) == 0:
            sleep(i[0])
        else:
            print((Fore.LIGHTBLACK_EX + d[d.index(i) - 1][1]).center(columns)); v.append(d[d.index(i) - 1][1])
        print((Fore.WHITE + i[1]).center(columns)); v.append(i[1])
        count = 1
        for x in d:
            if count == 15: break
            if x[1] not in v: print((Fore.LIGHTBLACK_EX + x[1]).center(columns)); count += 1
        sleep(d[d.index(i) + 1][0] - i[0])
        print("\033c", end="")