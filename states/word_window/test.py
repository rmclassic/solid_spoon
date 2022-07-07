import json

f = open('similarity_calculation.state', 'r').read()
a = json.loads(f)
s = {}
for sim in a:
    if sim['similarity'] > 0.5:
        if sim['w1'] not in s:
                s[sim['w1']] = [sim['w2']]
        else:
                s[sim['w1']].append(sim['w2'])
        # if sim['w2'] not in s:
        #         s[sim['w2']] = [sim['w1']]
        # else:
        #         s[sim['w2']].append(sim['w1'])


for x in s:
    print(x, s[x])
