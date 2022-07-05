from sklearn.datasets import fetch_20newsgroups
import sklearn.datasets
from nltk.tokenize import word_tokenize
import nltk
import util
import json
import window

newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))

data_tokens = []
documents = []


def save_state(data, tag):
    dstr = json.dumps(data)
    f = open(tag + '.state', 'w')
    f.write(dstr)
    f.close()

def load_state(tag):
    try:
        f = open(tag + '.state', 'r')
        dstr = f.read()
        f.close()
        data = json.loads(dstr)
    except:
        return None
    return data


data = load_state('preprocess')
if data == None:
    data = newsgroups_train.data[:200]
    for i, doc in enumerate(data):
        data[i] = util.preprocess_document(doc)

    save_state(data, 'preprocess')
else:
    print('preprocess: using previous state')

words = list(util.getCollectionBorder(data).keys())


jaccards = load_state('jaccard_calculation')

if jaccards == None:
    for i, word in enumerate(words):
        for j in range(i + 1, len(words)):
            jac = window.calculateJaccard(words[i], words[j])
            if jac > 0.9:
                print({'w1': words[i], 'w2': words[j], 'jaccard': jac})
