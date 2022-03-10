import re
import string
import numpy as np

def clear_text(text):
    pattern = "[{}]".format(string.punctuation)
    text = [word.lower() for word in text]
    text = [[re.sub(pattern,"",word) for word in words.split()] for words in text]
    text = [[word for word in words if len(word)>1] for words in text]
    text = [' '.join(words) for words in text]
    return np.array(text)

def text_all(text):
    text_set = set()
    for w in [words.split() for words in text]:
        text_set.update(w)
    return np.array(list(text_set))

def fit_transform(text,words):
    return [1 if word in text.split() else 0 for word in words]

def cosine_similarity(v,w):
    result= np.dot(v,w)/np.sqrt(np.dot(v,v)*np.dot(w,w))
    return result

def text_simillarities(id_text,features, text, n_text):
    simillarity = [[cosine_similarity(features[id_text],feature), int(i)] for i, feature in enumerate(features)]
    simillarity=simillarity[:-1]
    simillarity = np.array(sorted(simillarity,key=lambda sim: sim[0], reverse=True))
    text_simillarity = [[text[y],simillarity[x,0]] for x,y in enumerate(np.int0(simillarity[1:,1]),1)]
    texts = []
    for t in text_simillarity:
        if len(t[0].split())>4:
            texts.append(t)
    return texts[:n_text]
