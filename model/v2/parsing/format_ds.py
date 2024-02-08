import csv
import os

file_dir = os.path.dirname(os.path.realpath(__file__))

def resolve_path(relative_path):
     return os.path.join(file_dir, relative_path)

def data_for_ner(dataset):
    lst = []
    for row in dataset[1:]:
        lst.append(row[0] + '---')
    return lst

def readsome(filename, delimiter):
    with open(resolve_path(filename), 'r', encoding='utf-8') as rfile:
        return list(csv.reader(rfile, delimiter=delimiter, dialect=csv.excel))
    
def writetxt(list, filename):
    with open(resolve_path(filename), 'w', encoding='utf-8') as wfile:
            wfile.writelines(list)


print(file_dir)
ds = readsome('../data/raw_data.csv', ';')
writetxt(data_for_ner(ds), '../data/dataset_ner.txt')