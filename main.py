from sklearn.datasets import fetch_20newsgroups
import sklearn.datasets
from nltk.tokenize import word_tokenize
import nltk
import util
import itertools
import json
from window import getJaccard
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

def loop_query_search(s_borders, base_border):
    while True:
        query = input('Enter query: ')
        raw_query = query
        query = util.preprocess_document(query)
        q_border = {'border': util.getDocumentBorder(base_border, query), 'query': raw_query}
        result = []

        for s_border in s_borders:
            sim = util.calculateBorderSimilarity(q_border, s_border)
            if sim > 0.1:
                result.append(s_border)

        print('Retrieved', len(result), 'documents')
        if (len(result) == 0):
            continue

        while True:
            print('Enter [0-' + str(len(result) - 1) + '] to get specific document(q to search another query): ')
            i = input()
            if i == 'q':
                break
            else:
                if int(i) >= len(result) or int(i) < 0:
                    print('Invalid index')
                else:
                    print(result[int(i)]['doc'])
                    print()

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
    mode = input('Choose mode:\n1. Word window\n2. Sentence window\n3. Letter window\n4. Search query\nmode: ')
    mode = int(mode)

    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
    data_tokens = []
    documents = []

    data = load_state('preprocess')
    if data == None:
        data = util.preprocess_data(newsgroups_train.data[:100], mode)

        save_state(data, 'preprocess')
    else:
        print('preprocess: using previous state')

    base_border = util.getCollectionVector(data)
    if mode == 4: #Search document
        s_borders = load_state('s_border_generation')
        if s_borders == None:
            s_borders = []
            for i, doc in enumerate(data):
                s_borders.append({'border': util.getDocumentBorder(base_border, doc), 'doc': newsgroups_train.data[i]})

            save_state(s_borders, 's_border_generation')

        loop_query_search(s_borders, base_border)
        quit()

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
            for i, w1 in enumerate(base_border):
                print('calculating similarities ' + str(i) + '/' + str(len(base_border)))
                pool = multiprocessing.Pool(3)
                similarities = pool.starmap(getJaccard, [(w1, w2) for w2 in base_border])
                pool.terminate()

        save_state(similarities, 'similarity_calculation')
    else:
        print('similarity_calculation: using previous state')
