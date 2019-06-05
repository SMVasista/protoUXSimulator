from __future__ import division
import sys, os
import fileutils as fl
import numpy as np

def codify(strg, sep):
    if '?' in strg:
        strg = strg.strip().split('?')[0]
    n_strg = ''
    if len(strg) > 10:
        for i in range(10):
            n_strg = n_strg+str(list(strg)[i])
        return n_strg
    else:
        return '*'
        

def colorCode(weight):
    if weight <= 0.05:
        return '#527F9B'
    elif 0.05 <= weight <= 0.1:
        return '#6D95AE'
    elif 0.1 <= weight <= 0.15:
        return '#88AABF'
    elif 0.15 <= weight <= 0.2:
        return '#A7C2D3'
    elif 0.2 <= weight <= 0.25:
        return '#D8E5ED'
    elif 0.25 <= weight <= 0.3:
        return '#EDE0D8'
    elif 0.3 <= weight <= 0.35:
        return '#EECEBA'
    elif 0.35 <= weight <= 0.4:
        return '#EEB693'
    elif 0.4 <= weight <= 0.45:
        return '#F19B65'
    elif 0.45 <= weight:
        return '#F07629'
    else:
        return '#000000'

def createSiteMap(fileLoc):
    data = fl.readLinesAndSplit(fileLoc, '/')

    #Creating nXm matrix
    max_depth = max([len(x) for x in data])

    Rel = []
    for line in data:
        if len(line) > 2:
            for j in range(len(line)-1):
                if line[j] != '' and line[j+1] != '':
                    x = codify(str(line[j]), '-') if len(line[j]) > 15 else line[j]
                    y = codify(str(line[j+1]), '-') if len(line[j+1]) > 15 else line[j+1]
                    Rel.append(str(x)+'--'+str(y))

    with open('cluster','w') as f:
        for line in Rel:
            f.write(str(line)+'\n')
    return Rel

def createHeatMap(fileLoc):
    data = fl.readLinesAndSplit(fileLoc, ',')
    data.pop(0)
    types = list(set([v[0] for v in data]))
    connect = {}
    Rel = {}
    #Calculating page view stats
    pv_max = max([v[3] for v in data])
    pv_min = min([v[3] for v in data])
    pt_max = max([v[4] for v in data])
    pt_min = min([v[4] for v in data])
    for tp in types:
        Rel[tp] = {}
        for line in data:
            if line[0] == tp:
                x = codify(str(line[1]), '/') if len(line[1]) > 15 else line[1]
                y = codify(str(line[2]), '/') if len(line[2]) > 15 else line[2]
                w = (1+int(line[3]))*(1+int(line[4]))
                if x != y:
                    if str(x)+'--'+str(y) in Rel[tp]:
                        Rel[tp][str(x)+'->'+str(y)] += w
                    else:
                        Rel[tp][str(x)+'->'+str(y)] = w

    for tp in types:
        r_mean = np.mean(Rel[tp].values())
        r_std = np.std(Rel[tp].values())
        colored = []
        with open('hc_'+str(tp), 'w') as f:
            for elem in Rel[tp]:
                w = ((Rel[tp][elem] - r_mean)/r_std) + 0.4
                print w
                f.write(str(elem)+' {color:'+colorCode(w)+'}\n')
                if elem.split('->')[1] not in colored:
                    f.write(str(elem.split('->')[1])+' {color:'+colorCode(w)+'}\n')
                    colored.append(elem.split('->')[1])
                    
if __name__=="__main__":
    pass
