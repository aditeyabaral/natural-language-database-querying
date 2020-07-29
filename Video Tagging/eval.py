import pickle
import time

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

from queryRetrieval import getRelevantVideo

cap = pickle.load(open("captions.pkl", "rb"))
ids = [int(i.strip()) for i in open("../Database/Video/ids.txt").readlines()]
cat = [int(i.strip()) for i in open("../Database/Video/category.txt").readlines()]

cat_map = dict((i, c) for i, c in zip(ids, cat))
vid_true = []
vid_pred = []
cat_true = []
cat_pred = []
start = time.time()
for caption in cap:
    vid_true.append(caption[1])
    cat_true.append(cat_map[caption[1]])
    pred_id = int(getRelevantVideo(caption[0])[0][3:-4])
    vid_pred.append(pred_id)
    cat_pred.append(cat_map[pred_id])
end = time.time()

time_taken = end - start
av_time = time_taken/len(cap)
print(av_time)

# print(confusion_matrix(vid_true, vid_pred))
print(classification_report(vid_true, vid_pred))
# print(confusion_matrix(cat_true, cat_pred))
print(classification_report(cat_true, cat_pred))
