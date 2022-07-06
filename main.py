from sklearn.datasets import fetch_20newsgroups
import sklearn.datasets
from nltk.tokenize import word_tokenize
import nltk
import util
import itertools
import json
from window import getWindowJaccard
import multiprocessing

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

def _handle_similarity_calculation(index:int, word:str, word_borders:list):
    if index % 100 == 0:
        print('calculating similarities ', index, '/', len(word_borders))
    similarities = []
    for j, w2_border in enumerate(word_borders[index + 1:]):
        w_sim = util.calculateBorderSimilarity(word, w2_border)

        if w_sim != 0 and w_sim > 0.1:
            similarities.append({'w1': word['word'], 'w2': w2_border['word'], 'similarity': w_sim})

    return similarities

if __name__ == "__main__":

    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
    data_tokens = []
    documents = []




    data = load_state('preprocess')
    if data == None:
        data = newsgroups_train.data
        for i, doc in enumerate(data):
            data[i] = util.preprocess_document(doc)

        save_state(data, 'preprocess')
    else:
        print('preprocess: using previous state')

    base_border = util.getCollectionVector(data)

    word_borders = load_state('border_generation')

    if word_borders == None:
        word_borders = []
        for i, word in enumerate(base_border):
            if i % 100 == 0:
                print('generating word border for \'' + word + '\':' , i, '/', len(base_border))

            w_border = util.getWordBorder(base_border, word, data)
            word_borders.append({'word': word, 'border': w_border})

        save_state(word_borders, 'border_generation')
    else:
        print('border_generation: using previous state')

    print('calculating similarities')

    similarities = load_state('similarity_calculation')



    p_list = list()
    if similarities == None:
        similarities = []
        total_len = len(word_borders)
        pool = multiprocessing.Pool()
        similarities = pool.starmap(_handle_similarity_calculation, [(i, word_borders[i], word_borders) for i in range(len(word_borders))])
        similarities = list(itertools.chain(*similarities))
        save_state(similarities, 'similarity_calculation')

    else:
        print('similarity_calculation: using previous state')


    for s in similarities:
        print(s)
