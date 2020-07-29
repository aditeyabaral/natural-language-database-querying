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

acc_per_cat = {k:v[0]/v[1]for k,v in acc_per_cat.items()}

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

d = acc_per_cat 
lengths, scores = cap_len_length, cap_len_scores

items = list(zip(lengths, scores))
items.sort(key = lambda x: x[0])

lens = [i[0] for i in items]
scs = [i[1] for i in items]

plt.figure(figsize = (10,5))
plt.bar(d.keys(), d.values())
plt.xticks(range(0, max(d.keys())+1))
plt.xlabel("Category")
plt.ylabel("Accuracy")
plt.title("Accuracy per Category")
plt.savefig("Accuracy per Category.png", dpi = 1000)
plt.close()

plt.figure(figsize = (10,5))
k = [i[0] for i in items if i[1]>0]
cm = plt.cm.get_cmap('Spectral')
n, bins, patches = plt.hist(k, bins = 10)
bin_centers = 0.5 * (bins[:-1] + bins[1:])
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
plt.ylabel("Number of Correct Retrievals")
plt.xlabel("Length of Query")
plt.xticks(range(0, max(k)+20, 20))
plt.title("Correct Retrievals vs Length of Query")
plt.savefig("Correct Retrievals vs Length of Query.png", dpi = 1000)
plt.close()


acc_len = {k:[0, 0] for k in range(0,200,10)}
for i in items:
    key, value = i
    key = round(key, -1)
    acc_len[key][1]+= 1
    acc_len[key][0]+= value
    
tmp = {}
for i in acc_len:
    if acc_len[i][1]!=0:
        tmp[i] = acc_len[i][0]/acc_len[i][1]
        
plt.figure(figsize = (10,5))        
plt.plot(list(tmp.keys()), list(tmp.values()))
plt.xlabel("Length of Query")
plt.ylabel("Accuracy of Retrievals")
plt.title("Accuracy vs Length of Query")
plt.savefig("Accuracy vs Length of Query", dpi = 1000)
plt.close()
