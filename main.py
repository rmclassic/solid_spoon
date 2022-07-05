from sklearn.datasets import fetch_20newsgroups
import sklearn.datasets
from nltk.tokenize import word_tokenize
import nltk
import util
import json
import window

print(window.ejtema('hey', 'wowy'))
input()
newsgroups_train = fetch_20newsgroups(subset='train')

data_tokens = []
documents = []
# for d in newsgroups_train.data:
#   # data_tokens.append(word_tokenize(d))
#   sentences = nltk.sent_tokenize(d)
#   documents.append(sentences)
#
#
# sims = {}
# for i in range(200):#range(len(documents)):
#     d = documents[i]
#     #if i % 100 == 0:
#     print('processed ', i, '/', len(documents),' documents')
#
#     jacs = getWindowJaccard(d)
#     for jac in jacs:
#         if jac['jaccard'] > 0.5:
#             if jac['w1'] in sims:
#                 if jac['w1'] != jac['w2']:
#                     sims[jac['w1']].append(jac['w2'])
#             else:
#                 sims[jac['w1']] = [jac['w2'],]
#
# print(sims)

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
    data = []
    for doc in newsgroups_train.data[:2000]:
        data += util.preprocess_document_sent(doc)

    for i, doc in enumerate(data):
        data[i] = util.preprocess_document(doc)

    save_state(data, 'preprocess')
else:
    print('preprocess: using previous state')

base_border = util.getCollectionBorder(data)

word_borders = load_state('border_generation')

if word_borders == None:
    word_borders = []
    for i, word in enumerate(base_border):
        print('generating word border for \'' + word + '\':' , i, '/', len(base_border))
        w_border = util.getWordBorder(base_border, word, data)
        print({'word': word, 'border': w_border})
        word_borders.append({'word': word, 'border': w_border})

    save_state(word_borders, 'border_generation')
else:
    print('border_generation: using previous state')

print('calculating similarities')

similarities = load_state('similarity_calculation')

if similarities == None:
    similarities = []
    for i, w1_border in enumerate(word_borders):
        for j, w2_border in enumerate(word_borders[i + 1:]):
            w_sim = util.calculateBorderSimilarity(w1_border, w2_border)

            if w_sim != 0 and w_sim > 0.1:
                similarities.append({'w1': w1_border['word'], 'w2': w2_border['word'], 'similarity': w_sim})
                print({'w1': w1_border['word'], 'w2': w2_border['word'], 'similarity': w_sim})
    save_state(similarities, 'similarity_calculation')

else:
    print('similarity_calculation: using previous state')

for s in similarities:
    print(s)
