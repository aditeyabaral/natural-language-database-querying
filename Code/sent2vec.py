import numpy as np
from sklearn.decomposition import PCA


def sentences_to_vec(sentence_list, wordvec_func, embedding_size=300):
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(embedding_size)
        sentence_length = 1
        for word in sentence.split():
            try:
                vs = np.add(vs, wordvec_func(word))
                sentence_length += 1
            except:
                pass

        vs = np.divide(np.nan_to_num(vs), sentence_length)
        sentence_set.append(vs)

    pca = PCA()
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]
    u = np.multiply(u, np.transpose(u))

    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)

    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u, vs)
        sentence_vecs.append(np.subtract(vs, sub))

    return sentence_vecs
