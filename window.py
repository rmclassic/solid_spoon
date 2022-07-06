import pprint

def intersection(l1, l2):
    isc = [value for value in l1 if value in l2 if value != ''];
    return isc

def ejtema(l1, l2):
    isc = []
    isc.extend([value for value in l1 if value != ''])
    isc.extend([value for value in l2 if value not in l1 and value != ''])
    return isc

def sanitize(l):
    return [value for value in l if value != '']

def generateWindows(winlen, data):
    windows = []

    for s in data:
        words = s
        for i in range(len(words)):
            lwindow = []
            for j in range(winlen - 1, 0, -1):
                if i - j >= 0:
                    lwindow.append(words[i - j])
                else:
                    lwindow.append('')

            lwindow.append(words[i])

            for j in range(1, winlen):
                if i + j < len(words):
                    lwindow.append(words[i + j])
                else:
                    lwindow.append('')

            windows.append(lwindow)

    return windows


def getJaccard(w1, w2):
    if w1 == w2:
        return 0
    isc = intersection(w1, w2)
    try:
        jacc = len(temp['isc']) / (len(w2) + len(w1) - len(isc))
        return jacc
    except:
        return 0
