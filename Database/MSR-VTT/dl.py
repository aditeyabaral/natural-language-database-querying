import datetime
import os

with open("urls.txt") as url, open("start.txt") as start, open("end.txt") as end:
    urli = list(i.strip() for i in url.readlines())
    starti = list(float(i.strip()) for i in start.readlines())
    endi = list(float(i.strip()) for i in end.readlines())
    for idx, (u, s, e) in enumerate(zip(urli, starti, endi)):
        # print(
        #     f"youtube-dl -f mp4 {u} --postprocessor-args '-ss {datetime.timedelta(seconds=s)} -t {datetime.timedelta(seconds=e-s)}'"
        # )
        if idx == 71:
            os.system(
                f"ffmpeg -ss {datetime.timedelta(seconds=s)} -i $(youtube-dl -f bestvideo --get-url {u}) -t {datetime.timedelta(seconds=e-s)} -c:v copy -c:a copy vid{idx}.mp4"
            )
