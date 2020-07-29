import csv
import time

import gensim.downloader as api
import numpy as np
from nltk.stem import WordNetLemmatizer

import keywords
import speechRecognition
from sent2vec import sentences_to_vec

model = api.load("fasttext-wiki-news-subwords-300")

lemm = WordNetLemmatizer()


# query, translated = speechRecognition.audio_to_text()
# while not translated:
#     time.sleep(2)
#     query, translated = speechRecognition.audio_to_text()

# translated = "I want to see an advertisement for kotak mahindra bank"


def getRelevantVideo(translated):
    # print(translated)
    tags = list(map(lemm.lemmatize, keywords.getKeywordsRAKE(translated)))
    vid_name, vid_tags = [], []
    with open("tag_databases/tags_test_3.csv", "r") as tagsfile:  # tags_framek_frameo_online_filter or tags_framek_frameo_filter 
        reader = csv.reader(tagsfile)
        for row in reader:
            vid_tags.append(list(map(lemm.lemmatize, row[1:])))
            vid_name.append(row[0])

    vectors = sentences_to_vec(
        [" ".join(t) for t in vid_tags] + [" ".join(tags)], model.wv.get_vector
    )
    vid_vectors = vectors[:-1]
    tag_vector = vectors[-1]

    sim_scores = []
    for idx, vec in enumerate(vid_vectors):
        sim = np.dot(vec, tag_vector) / (
            np.linalg.norm(vec) * np.linalg.norm(tag_vector)
        )
        sim_scores.append(sim)

    # tags_set = set(tags)
    # for vid_tag_list in vid_tags:
    #     vid_tag_set = set(vid_tag_list)
    #     sim_scores.append(len(tags_set.intersection(vid_tag_set)))
    #
    position = sim_scores.index(max(sim_scores))
    # print("Score: ", sim_scores[position])
    most_similar_video = vid_name[position]
    return most_similar_video, translated
