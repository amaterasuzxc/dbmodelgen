import json
from typing import List, Dict, Any
from spacy.tokens.doc import Doc

from components.neuro.scripts.data_processing.postprocessing.SpanShapeshifter import ShapeShifter


class _LogicalAttribute:
    def __init__(self, name: str) -> None:
        self.name = name
        self.type = ""


    @property
    def name(self) -> str:
        return self._name
    
    
    @name.setter
    def name(self, value):
        self._name = value
    

    @property
    def type(self) -> str:
        return self._type
    

    @type.setter
    def type(self, value):
        self._type = value


class _LogicalEntity:
    def __init__(self, name: str) -> None:
        self.name = name
        self.attributes: List[_LogicalAttribute] = []


    @property
    def name(self) -> str:
        return self._name
    

    @name.setter
    def name(self, value):
        self._name = value
    

    @property
    def attributes(self) -> List[_LogicalAttribute]:
        return self._attributes
    

    @attributes.setter
    def attributes(self, value):
        self._attributes = value
    

class JsonAssembler:
    def __init__(self, rel_threshold: float) -> None:
        self._rel_threshold = rel_threshold
        self._shapeshifter = ShapeShifter()


    def _shapeshift_entities(self, entities: List[_LogicalEntity]) -> List[_LogicalEntity]:
        return entities # TODO


    def _build_entities(self, doc: Doc) -> List[_LogicalEntity]:
        entities: List[_LogicalEntity] = []

        for ent in doc.ents:
            if ent.label_ != "LENTITY":
                continue
            entity = _LogicalEntity(ent.text)
            attributes: List[_LogicalAttribute] = []

            for relation in list(filter(lambda _:
                                        _[1]["ATTRIBUTE_OF"] 
                                        and _[1]["ATTRIBUTE_OF"] >= self._rel_threshold
                                        and _[0][1] == ent.start, doc._.rel.items())):
                attr = next(filter(lambda _:_.start == relation[0][0], doc.ents))
                if attr.label_ != "LATTRIBUTE":
                    continue
                attribute = _LogicalAttribute(attr.text)
                scores = next(filter(lambda _:_[0] == attr.start, doc._.ecat.items()))[1]
                attribute.type = max(scores.items(), key=lambda scores:scores[1])[0]
                attributes.append(attribute)
            
            entity.attributes = attributes
            entities.append(entity)

        return entities


    def assemble(self, doc: Doc) -> str:
        entities = self._build_entities(doc)
        entities = self._shapeshift_entities(entities)

        return json.dumps(entities, default=lambda _:_.__dict__, ensure_ascii=False) # FIXME: field names