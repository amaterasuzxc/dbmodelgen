import csv
import os

file_dir = os.path.dirname(os.path.realpath(__file__))

def resolve_path(relative_path):
     return os.path.join(file_dir, relative_path)

def readcsv(filename, delimiter):
    with open(resolve_path(filename), 'r', encoding='utf-8') as rfile:
        return list(csv.reader(rfile, delimiter=delimiter, dialect=csv.excel))
    
def writetxt(filename, text):
    with open(resolve_path(filename), 'w', encoding='utf-8') as wfile:
        wfile.writelines(text)
    
def main():
    csv_data = readcsv('../../../data/data_to_annotate.csv', ';')
    suffix = 0
    for text in csv_data[1:]:
        suffix += 1
        writetxt(f'../../../data/txt/task-{suffix}.txt', text[0])

if __name__ == "__main__":
    main()