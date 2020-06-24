import csv
import time

from nltk.stem import WordNetLemmatizer

import keywords
import speechRecognition

lemm = WordNetLemmatizer()


query, translated = speechRecognition.audio_to_text()
while not translated:
    time.sleep(2)
    query, translated = speechRecognition.audio_to_text()

print(query)
print(translated)

tags = list(map(lemm.lemmatize, keywords.getKeywordsRAKE(translated)))
print(tags)
vid_name, vid_tags = [], []
with open("videoTags.csv", "r") as tagsfile:
    reader = csv.reader(tagsfile)
    for row in reader:
        vid_tags.append(list(map(lemm.lemmatize, row[1:])))
        vid_name.append(row[0])

sim_scores = []
tags_set = set(tags)
for vid_tag_list in vid_tags:
    vid_tag_set = set(vid_tag_list)
    sim_scores.append(len(tags_set.intersection(vid_tag_set)))

position = sim_scores.index(max(sim_scores))
print("Score: ", sim_scores[position])
most_similar_video = vid_name[position]
print(most_similar_video)


# transform_mat = vid_tags + [" ".join(tags)]
