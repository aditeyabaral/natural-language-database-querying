import json
import pickle

a = json.load(open("videodatainfo_2017.json"))
ids = [int(i.strip()) for i in open("ids.txt").readlines()]

wanted_captions = [
    (i["caption"], int(i["video_id"][5:])) for i in a["sentences"] if int(i["video_id"][5:]) in ids
]

pickle.dump(wanted_captions, open("captions.pkl", "wb"))
