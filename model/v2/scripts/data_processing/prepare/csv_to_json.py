import csv
import json as json_processor
import os

file_dir = os.path.dirname(os.path.realpath(__file__))

def resolve_path(relative_path):
     return os.path.join(file_dir, relative_path)

def readcsv(filename, delimiter):
    with open(resolve_path(filename), 'r', encoding='utf-8') as rfile:
        return list(csv.reader(rfile, delimiter=delimiter, dialect=csv.excel))
    
def writejson(filename, json):
    with open(resolve_path(filename), 'w', encoding='utf-8') as wfile:
        for item in json:
            wfile.write(json_processor.dumps(item) + "\n")
    
def main():
    csv_data = readcsv('../../../data/data_to_annotate.csv', ';')
    json = []
    for text in csv_data[1:]:
        json.append({'text': text[0], 'label': ''})
    writejson('../../../data/data_to_annotate.jsonl', json)

if __name__ == "__main__":
    main()