import csv
import os

import videoLookup

root_path = os.path.join(os.path.dirname(os.getcwd()), "Database", "Video")
video_list = [i for i in os.listdir(root_path) if i.endswith("mp4")]
with open("tag_databases/tags_test_3.csv", "w") as tags_file:
    writer = csv.writer(tags_file)
    for idx, path in enumerate(video_list):
        tags = videoLookup.getFilteredTags(path)
        print(tags)
        writer.writerow([path] + tags)
