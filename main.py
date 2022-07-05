from sklearn.datasets import fetch_20newsgroups
import sklearn.datasets
from nltk.tokenize import word_tokenize
import nltk
from window import getWindowJaccard

newsgroups_train = fetch_20newsgroups(subset='train')

data_tokens = []
documents = []
for d in newsgroups_train.data:
  # data_tokens.append(word_tokenize(d))
  sentences = nltk.sent_tokenize(d)
  documents.append(sentences)


sims = {}
for i in range(200):#range(len(documents)):
    d = documents[i]
    #if i % 100 == 0:
    print('processed ', i, '/', len(documents),' documents')

    jacs = getWindowJaccard(d)
    for jac in jacs:
        if jac['jaccard'] > 0.5:
            if jac['w1'] in sims:
                if jac['w1'] != jac['w2']:
                    sims[jac['w1']].append(jac['w2'])
            else:
                sims[jac['w1']] = [jac['w2'],]

print(sims)
#
# for i in range(len(data_tokens)):
#     data_tokens[i] = list(filter(lambda l:len(l) >= 3 , list(map(lambda x:x.lower(), data_tokens[i]))))

# uniques = {}
# for i in range(len(data_tokens)):
#     for word in data_tokens[i]:
#         if (not uniques.get(word)):
#             uniques[word] = 1
#         else:
#             uniques[word] += 1



# print(uniques)
#
# uniques = dict(sorted(uniques.items(), key=lambda item: item[1]))
# print(uniques)
