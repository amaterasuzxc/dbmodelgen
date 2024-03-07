import spacy
from model.Entity import Entity
from model.Attribute import Attribute

nlp = None

def init():
    global nlp
    nlp = spacy.load("ru_core_news_lg")


def parse_text(text):
    return nlp(text)

def parse_text_for_ner(ner: spacy.tokens.Doc, text):
    if nlp == None:
        init()
    result = []
    dp = parse_text(text)
    ner_idxs = [entity.start_char for entity in ner.ents]
    dp_tokens = list(filter(lambda _:_.idx in ner_idxs, [dp_token for dp_token in dp]))
    for entity in ner.ents:
        for dp_token in dp_tokens:
            if entity.start_char == dp_token.idx:
                result.append(Entity(entity.text, [Attribute(child.orth_, child.tag_) for child in dp_token.children if child.tag_ == "NOUN"]))
    return result
    

