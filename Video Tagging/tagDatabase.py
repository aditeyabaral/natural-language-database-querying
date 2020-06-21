import csv
import os

import videoLookup

root_path = os.path.join(os.path.dirname(os.getcwd()), "Database", "Video")
# video_list = [f"{root_path}/{i}" for i in os.listdir(root_path)]
video_list = os.listdir(root_path)
with open("videoTags.csv", "w") as tags_file:
    writer = csv.writer(tags_file)
    # for path in video_list:
    path = "vid1.mp4"
    tags = videoLookup.getFilteredTags(path)
    writer.writerow([path] + tags)
    # break
