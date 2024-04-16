import json
import copy
import typer
import re
from pathlib import Path
from spacy.lang.ru import Russian
from typing import List

def main(main_json:Path, custom_json:Path, out_file:Path):
    outfile = []
    nlp = Russian()
    main_file = assemble_new_json(main_json, nlp)
    custom_file = assemble_new_json(format_custom_json(custom_json), nlp)
    all_lines = enumerate(zip(main_file, custom_file))
    for line_nr, (main_line, custom_line) in all_lines:
        newline = copy.deepcopy(main_line)
        for main_span in newline["spans"]:
            for custom_span in custom_line["spans"]:
                if (main_span["start"] == custom_span["start"]):
                    main_span["category"] = custom_span["label"]
        outfile.append(newline)
        
    with out_file.open("w+", encoding="utf8") as newfile:
        for item in outfile:
            newfile.write(json.dumps(item, ensure_ascii=False) + "\n")

def format_custom_json(json_loc:Path) -> Path:
    path = json_loc.parent.joinpath("temp_mapped.jsonl")
    outfile = []
    with json_loc.open("r", encoding="utf8") as jsonfile:
        for line in jsonfile:
            entry = json.loads(line)
            newline = copy.deepcopy(entry)
            newline["entities"] = []
            old_spans = newline.pop("label")
            for old_span in old_spans:
                new_span = {}
                new_span["start_offset"] = old_span[0]
                new_span["end_offset"] = old_span[1]
                new_span["label"] = old_span[2]
                newline["entities"].append(new_span)
            outfile.append(newline)

    with path.open("w+", encoding="utf8") as newfile:
        for item in outfile:
            newfile.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    return path
        

def assemble_new_json(json_loc:Path, nlp:Russian) -> List:
    outfile = []
    with json_loc.open("r", encoding="utf8") as jsonfile:
        for line in jsonfile:
            entry = json.loads(line)
            newline = copy.deepcopy(entry)
            if newline.get("entities") is not None:
                newline["spans"] = newline.pop("entities")
                tokenizer = nlp.tokenizer
                tokens = tokenizer(newline["text"])
                tokens = tokens.to_json()["tokens"]
                newline["tokens"] = tokens
                for token in newline["tokens"]:
                    token["text"] = newline["text"][token["start"]:token["end"]]
                for span in newline["spans"]:
                    span["start"] = span.pop("start_offset")
                    span["end"] = span.pop("end_offset")
                    span["type"] = "span"
                    text = newline["text"][span["start"]:span["end"]]
                    span["text"] = text
                    tail_match = re.match(r"(.+\S)(\s+$)", text)
                    head_match = re.match(r"(^\s+)(\S.+)", text)
                    if tail_match != None:
                        tail = tail_match.group(2)
                        trim_count = len(tail)
                        text = text[0:len(text) - trim_count]
                        span["end"] = span["end"] - trim_count
                    if head_match != None:
                        head = head_match.group(1)
                        trim_count = len(head)
                        text = text[trim_count:len(text)]
                        span["start"] = span["start"] + trim_count
                    span["text"] = text
                    for token in tokens:
                        if token["start"] == span["start"] - 1:
                            span["token_start"] = token["id"]
                            span["start"] = token["start"]
                            span["text"] = newline["text"][span["start"]:span["end"]]
                        if token["start"] == span["start"]:
                            span["token_start"] = token["id"]
                        if token["end"] == span["end"]:
                            span["token_end"] = token["id"]
                        if len(newline["text"]) - 1 < token["end"] + 1:
                            token["ws"] = False
                        else:
                            token["ws"] = True if newline["text"][token["end"]] == ' ' else False
            if newline.get("relations") is not None:
                for relation in newline["relations"]:
                    relation["label"] = relation.pop("type")
                    for span in newline["spans"]:
                        if span["id"] == relation["from_id"]:
                            relation["head"] = span["token_end"]
                        if span["id"] == relation["to_id"]:
                            relation["child"] = span["token_end"]
            outfile.append(newline)
    return outfile
        
if __name__ == "__main__":
    typer.run(main)