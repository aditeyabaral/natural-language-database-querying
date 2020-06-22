import speechRecognition
import keywords
import time
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


query, translated = speechRecognition.audio_to_text()
while not translated:
  time.sleep(2)
  query, translated = speechRecognition.audio_to_text()

tags = keywords.getKeywordsRAKE(translated)
vid_name, vid_tags = [], []
with open("videoTags.csv", "r") as tagsfile:
  reader = csv.reader(tagsfile)
  for row in reader:
    vid_tags.append(" ".join(row[1:]))
    vid_name.append(row[0])

transform_mat = vid_tags + [" ".join(tags)]

vectorizer = CountVectorizer()
model = vectorizer.fit_transform(transform_mat)
for vid in model[:-1]:
  print(cosine_similarity(model[-1], vid))

