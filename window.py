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


def getWindowJaccard(data):
    dd = []
    for s in data:
        f = s.split(' ')
        dd.append(f)

    w = generateWindows(2, dd)
    all_windows = []
    for s in w:
        all_windows.append(s)

    jaccards = []
    for i in range(len(all_windows)):
        for j in range(i, len(all_windows)):
            temp = {}
            temp['w1'] = all_windows[i][int(len(all_windows[i])/2) + 1]
            temp['w2'] = all_windows[j][int(len(all_windows[j])/2) + 1]
            temp['isc'] = intersection(all_windows[i], all_windows[j])
            try:
                temp['jaccard'] = len(temp['isc']) / (len(sanitize(all_windows[i])) + len(sanitize(all_windows[j])) - len(temp['isc']))
            except:
                continue
            jaccards.append(temp)

    return jaccards
