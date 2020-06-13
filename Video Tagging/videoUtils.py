import os
import subprocess
import shutil
from collections import Counter
import gensim.downloader as api
from sklearn.cluster import KMeans


def videoFrames(filename, framerate=1):
    """
    Returns a generator of frames from a video specified by FILEPATH
    """
    vid_file = os.path.join(os.path.dirname(os.getcwd()), "Database", "Video", filename)
    print(vid_file)
    assert os.path.isfile(vid_file), "Given path is not a valid file"
    tmpdir = os.path.join(os.getcwd(), "tmp")
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    os.mkdir(tmpdir)
    subprocess.run(
        [
            "ffmpeg",
            "-i",
            vid_file,
            "-r",
            f"{framerate}",
            os.path.join(tmpdir, "img_%04d.jpg"),
        ]
    )
    return [os.path.join(tmpdir, i) for i in os.listdir(tmpdir)]


def getTopKCounter(a, K):
    """
    Returns the top K frequent words from a list of words
    """
    r = []
    for i in a:
        r.extend(i)
    c = Counter(r)
    words = [i[0] for i in c.most_common(K)]
    return words


def clusterKeywords(keywords):
    model = api.load("fasttext-wiki-news-subwords-300")
    sim_matrix = []
    for word1 in keywords:
        word_sims = []
        for word2 in keywords:
            word_sims.append(model.similarity(word1, word2))
        sim_matrix.append(word_sims)

    clusterer = KMeans(n_clusters=2)
    cm = clusterer.fit(sim_matrix)
    biggest_cluster = max(cm.labels_, key=cm.labels_.count)
    relevant_keywords = []
    for word, label in zip(keywords, cm.labels_):
        if label == biggest_cluster:
            relevant_keywords.append(word)

    return relevant_keywords

