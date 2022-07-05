from sklearn.datasets import fetch_20newsgroups
import sklearn.datasets
from nltk.tokenize import word_tokenize
import nltk
import util
import json
from window import getWindowJaccard
#import threading
from multiprocessing import Process

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

    def _handle_similarity_calculation(index:int, word:str):
        for j, w2_border in enumerate(word_borders[index + 1:]):
            w_sim = util.calculateBorderSimilarity(word, w2_border)

            if w_sim != 0 and w_sim > 0.1:
                similarities.append({'w1': w1_border['word'], 'w2': w2_border['word'], 'similarity': w_sim})

            #if index % 20 == 0:
                #print('processed', index, 'items', {'w1': w1_border['word'], 'w2': w2_border['word'], 'similarity': w_sim})

    th_list = list()
    if similarities == None:
        similarities = []
        total_len = len(word_borders)
        for i, w1_border in enumerate(word_borders):
            if i % 64 != 0:
                #th_list.append(threading.Thread(target=_handle_similarity_calculation, args=(i,w1_border)))
                p = Process(target=_handle_similarity_calculation, args=(i,w1_border))
                th_list.append(p)
            else:
                for th in th_list:
                    th.start()
                for th in th_list:
                    th.join()
                print('processed', i, '/', total_len, 'words')
                th_list = []


        save_state(similarities, 'similarity_calculation')

    else:
        print('similarity_calculation: using previous state')

    for s in similarities:
        print(s)
