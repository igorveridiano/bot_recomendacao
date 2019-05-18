import re
import string
import numpy as np


def cosine_similarity(v, w):
    return np.dot(v, w) / np.sqrt(np.dot(v, v) * np.dot(w, w))


def recommender(movies, synopse):
    corpus = np.array([synopse, movies['text']])

    def clear_text(text):
        pattern = "[{}]".format(string.punctuation)
        text = [word.lower() for word in text]
        text = [[re.sub(pattern, "", word) for word in words.split()] for words in text]
        text = [[word for word in words if len(word) > 1] for words in text]
        text = [' '.join(words) for words in text]

        return np.array(text)

    corpus_clear = clear_text(corpus)

    def text_all(text):
        text_set = set()
        for w in [words.split() for words in text]:
            text_set.update(w)

        return np.array(list(text_set))

    vocabulary = text_all(corpus_clear)

    def fit_transform(text, words=vocabulary):
        return [1 if word in text.split() else 0 for word in words]

    features = np.array(list(map(fit_transform, corpus_clear)))

    def text_similarities(id_text1, id_text2):
        simillarity = [cosine_similarity(features[id_text1], features[id_text2])]
        simillarity = np.array(simillarity)
        return simillarity[0]

    return text_similarities(0, 1)
