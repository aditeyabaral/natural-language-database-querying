import pickle
import time

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

from queryRetrieval import getRelevantVideo

cap = pickle.load(open("captions.pkl", "rb"))
ids = [int(i.strip()) for i in open("../Database/Video/ids.txt").readlines()]
cat = [int(i.strip()) for i in open("../Database/Video/category.txt").readlines()]
cat_map = dict((i, c) for i, c in zip(ids, cat))

cat_unique = list(set(cat))
acc_per_cat = {k:[0,0] for k in cat_unique}

vid_true = []
vid_pred = []
cat_true = []
cat_pred = []

cap_len_length = []
cap_len_scores = []

retrieval_times = []

for caption in cap:
    vid_true.append(caption[1])
    cat_true.append(cat_map[caption[1]])
    cap_len_length.append(len(caption[0]))
    start = time.time()
    pred_id = int(getRelevantVideo(caption[0])[0][3:-4])
    end = time.time()
    retrieval_times.append(end-start)
    vid_pred.append(pred_id)
    cat_pred.append(cat_map[pred_id])

    if caption[1] == pred_id:
        acc_per_cat[cat_true[-1]][0]+=1
        cap_len_scores.append(1)
    else:
        cap_len_scores.append(0)
    acc_per_cat[cat_true[-1]][1]+=1


av_time = sum(retrieval_times)/len(retrieval_times)
# print average time per retrieval
print(av_time)

# print accuracy per category
print(acc_per_cat)

# print cap_len_lengths and scores
print(cap_len_length)
print(cap_len_scores)

# print(confusion_matrix(vid_true, vid_pred))
print(classification_report(vid_true, vid_pred))
# print(confusion_matrix(cat_true, cat_pred))
print(classification_report(cat_true, cat_pred))
