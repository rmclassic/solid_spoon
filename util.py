import nltk
import math
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
sw = stopwords.words('english')

WINDOW_RADIUS = 2

def preprocess_document(doc):
    doc = nltk.word_tokenize(doc)
    processed = []
    processed = list(filter(lambda l:len(l) >= 3 and l.isalpha() and l not in sw, list(map(lambda x:x.lower(), doc))))
    return processed

def preprocess_document_sent(doc):
    toks = []
    doc = nltk.sent_tokenize(doc)

    for s in doc:
        toks.append(preprocess_document(s))

    return toks

def getCollectionVector(col):
    border = {}
    for index, doc in enumerate(col):
        if index % 100 == 0:
            print('processed', index, 'docs')

        for w in doc:
            if w not in border:
                border[w] = 0
    return border

def makeWindowAround(index, doc):
    start_index = index if index - WINDOW_RADIUS > 0 else 0
    end_index = index + WINDOW_RADIUS if index + WINDOW_RADIUS < len(doc) else len(doc) - 1
    return doc[start_index:end_index]

def getWordWindows(word, doc, mode):
    last_index = 0
    windows = []

    while last_index != -1 and last_index + 1 < len(doc):
        try:
            last_index = doc.index(word, last_index + 1)
        except:
            last_index = -1
            continue

        if mode == 1: # word window
            window = doc
            windows.append(window)
            break
        else: # sentence window
            window = makeWindowAround(last_index, doc)

        windows.append(window)
    return windows

def normalizeBorder(word, border):
    try:
        max_val = border[word]
    except:
        return {}
    border[word] = 0
    border.update((x, y/max_val) for x, y in border.items())
    return border

def getWordBorder(base_border, word, col, mode):
    border = {}
    print('generating word border for ', word)
    for doc in col:
        w_wins = getWordWindows(word, doc, mode)
        for window in w_wins:
            for neighbor in window:
                if border.get(neighbor):
                    border[neighbor] += 1
                else:
                    border[neighbor] = 1
    return {'word': word, 'border': normalizeBorder(word, border)}


def calculateBorderSimilarity(w1_border, w2_border):
    dot_sum = 0

    for neighbor in w1_border['border']:
        if not w2_border['border'].get(neighbor):
            continue

        dot_sum += w1_border['border'][neighbor] * w2_border['border'][neighbor] / math.sqrt(len(w1_border['border']) * len(w2_border['border']))

    return dot_sum


def preprocess_data(data, mode):

    if mode == 1: #Word window
        for i, doc in enumerate(data):
            data[i] = preprocess_document(doc)
    elif mode == 2: #Sentence window
        temp = []
        for i, doc in enumerate(data):
            temp.extend(preprocess_document_sent(doc))
            data = temp
    return data
