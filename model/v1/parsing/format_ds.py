import csv
from operator import itemgetter
from itertools import groupby


def format_ds(dataset):
    for row in dataset[1:17]:
        rowlist = row[2].split(',')
        newrowlist = []
        for entry in rowlist:
            entry = entry.strip()
            newrowlist.append([entry, entry.split(':')[0]])
        newrowlist.sort(key=itemgetter(1))
        grpd = [[x for x, y in g] for k, g in groupby(newrowlist, key=itemgetter(1))]
        finalrowlist = []
        for entryset in grpd:
            finentry = entryset[0].split(':')[0] + ':['
            for entry in entryset:
                eset = entry.split(':')
                finentry += eset[1] + ':' + eset[2] + ','
            finentry = finentry.rstrip(',')
            finentry += ']'
            finentry = finentry.replace('_', ' ')
            finalrowlist.append(finentry)
        row[2] = '"' + ';'.join(finalrowlist) + '"'
    for row in dataset[17:]:
        rowlist = row[2].split(';')
        i = 0
        for e in rowlist:
            e = e.strip()
            rowlist[i] = e
            i += 1
        row[2] = '"' + ';'.join(rowlist) + '"'
    return dataset

def data_for_ner(dataset):
    lst = []
    for row in dataset[1:]:
        lst.append(row[0] + '---')
    return lst


def writenew(dataset):
    with open('formatted.csv', 'w', encoding='utf-8', newline='') as wfile:
        writer = csv.writer(wfile, delimiter=';', dialect=csv.excel)
        writer.writerows(dataset)


def readsome(name, delimiter):
    with open(name, 'r', encoding='utf-8') as rfile:
        return list(csv.reader(rfile, delimiter=delimiter, dialect=csv.excel))
    
def writetxt(list):
    with open('datalist.txt', 'w', encoding='utf-8') as wfile:
            wfile.writelines(list)


ds = readsome('zerodatasetcsv.csv', ';')
format_ds(ds)
writenew(ds)
nds = readsome('formatted.csv', ';')
writetxt(data_for_ner(nds))
# print(nds[1:][0][2])
