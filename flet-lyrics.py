import flet as ft
from syncedlyrics import search
from time import sleep
from yt_dlp import YoutubeDL
from re import findall

import os

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.title = "Flet Lyrics"
    page.window_full_screen = True
    page.bgcolor = ft.colors.BACKGROUND

    def exit_full(e):
        if page.window_full_screen:
            page.window_full_screen = False
            page.window_height = 512
            page.window_width = 512
        else:
            page.window_full_screen = True
        page.update()

    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Enter Youtube Music URL"
            page.update()
        else:
            url = txt_name.value
            get_video_id = lambda url : url.split("watch?v=")[1].split("&")[0] if "&" in url else url.split("watch?v=")[1]
            try:
                value = f"Collecting {get_video_id(url)} informations.."
            except:
                txt_name.error_text = "Enter Youtube Music URL"
                return page.update()
            page.clean()
            page.add(
                ft.Row(
                    controls=[
                        ft.Text(value, text_align=ft.TextAlign.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )

            if not os.path.isdir("./cache"):
                os.mkdir("cache")

            if os.path.isfile(f"./cache/{get_video_id(url)}.m4a") and os.path.isfile(f"./cache/{get_video_id(url)}.lrc"):
                path = f"./cache/{get_video_id(url)}.m4a"
                with open(f"./cache/{get_video_id(url)}.lrc", "r", encoding="utf-8") as f:
                    lrc = f.read()
            else:
                page.clean()
                page.add(
                    ft.Row(
                        controls=[
                            ft.Text(f"Downloading {get_video_id(url)} ..", text_align=ft.TextAlign.CENTER)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
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

            page.clean()
            page.add(
                ft.Row(
                    controls=[
                        ft.Text(f"Proccossing {get_video_id(url)} ..")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )

            audio = ft.Audio(
                src=path
            )
            page.overlay.append(audio)
            page.clean()
            def play_sound(_):
                audio.play()
                page.window_height = 512
                page.window_width = 512
                page.controls.clear()
                page.add(
                    ft.Row(
                        controls=[ft.Text("♪", style=ft.TextThemeStyle.DISPLAY_LARGE, color=ft.colors.GREY)],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                )
                page.update()
                for i in d:
                    page.controls.clear()
                    if i[2] == 0:
                        sleep(i[0])
                    else:
                        page.add(
                            ft.Row(
                                controls=[ft.Text(d[d.index(i) - 1][1], style=ft.TextThemeStyle.TITLE_LARGE, color=ft.colors.GREY)],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                    count = 0
                    page.add(
                        ft.Row(
                            controls=[ft.Text(i[1], style=ft.TextThemeStyle.DISPLAY_MEDIUM, color=ft.colors.WHITE)],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    )
                    v.append(i[2])
                    for x in d:
                        if count == 7: break
                        if x[2] not in v:
                            page.add(
                                ft.Row(
                                    controls=[ft.Text(x[1], style=ft.TextThemeStyle.TITLE_LARGE, color=ft.colors.GREY)],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            )
                            count += 1
                    page.add(
                        ft.Row(
                            controls=[ft.ElevatedButton("-", on_click=exit_full, icon=ft.icons.FULLSCREEN_EXIT)],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND
                        )
                    )
                    page.update()
                    try:
                        sleep(d[d.index(i) + 1][0] - i[0])
                    except:
                        page.controls.clear()
                        txt_name = ft.TextField(label="Enter Youtube Music URL")
                        page.add(
                            ft.Row(
                                controls=[txt_name, ft.ElevatedButton("Submit", on_click=btn_click)],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        )
                        page.update()
            page.add(
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Play", on_click=play_sound, icon=ft.icons.PLAY_ARROW)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )

    txt_name = ft.TextField(label="Enter Youtube Music URL")

    page.add(
        ft.Row(
            controls=[txt_name, ft.ElevatedButton("Submit", on_click=btn_click)],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.add(
        ft.Row(
            controls=[ft.ElevatedButton("", on_click=exit_full, icon=ft.icons.FULLSCREEN_EXIT)],
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )
    )

ft.app(target=main)
