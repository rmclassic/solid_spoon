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
    mode = input('Choose mode:\n1. Word window\n2. Sentence window\n3. Letter window\nmode: ')
    mode = int(mode)

    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
    data_tokens = []
    documents = []

    data = load_state('preprocess')
    if data == None:
        data = util.preprocess_data(newsgroups_train.data[:200], mode)

        save_state(data, 'preprocess')
    else:
        print('preprocess: using previous state')

    base_border = util.getCollectionVector(data)

    if mode != 3: #no letter window
        word_borders = load_state('border_generation')

        if word_borders == None:
            word_borders = []
            pool = multiprocessing.Pool()
            word_borders = pool.starmap(util.getWordBorder, [(base_border, word, data, mode) for _, word in enumerate(base_border)])

            save_state(word_borders, 'border_generation')
        else:
            print('border_generation: using previous state')

    print('calculating similarities')

    similarities = load_state('similarity_calculation')

    if similarities == None:
        similarities = []
        if mode != 3:
            total_len = len(word_borders)
            pool = multiprocessing.Pool()
            similarities = pool.starmap(_handle_similarity_calculation, [(i, word_borders[i], word_borders) for i in range(len(word_borders))])
            similarities = list(itertools.chain(*similarities))
        else:
            
        save_state(similarities, 'similarity_calculation')
    else:
        print('similarity_calculation: using previous state')


    for s in similarities:
        print(s)
