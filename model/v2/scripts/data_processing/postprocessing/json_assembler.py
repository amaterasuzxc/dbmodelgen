import json
from typing import List
from pydantic import BaseModel
from spacy.tokens.doc import Doc
from pydantic.json import pydantic_encoder

from scripts.data_processing.postprocessing.span_shapeshifter import ShapeShifter


class _LogicalAttribute(BaseModel):
    name: str
    type: str = None


class _LogicalEntity(BaseModel):
    name: str
    attributes: List[_LogicalAttribute] = []
    

class JsonAssembler:
    def __init__(self, rel_threshold: float = 0.8, ecat_threshold: float = 0.25) -> None:
        self._rel_threshold = rel_threshold
        self._ecat_threshold = ecat_threshold
        self._shapeshifter = ShapeShifter()


    def _shapeshift_entities(self, entities: List[_LogicalEntity]) -> List[_LogicalEntity]:
        for ent in entities:
            ent.name = self._shapeshifter.shapeshift(span=ent.name, single=False)

            for attr in ent.attributes:
                attr.name = self._shapeshifter.shapeshift(span=attr.name, single=True)
        
        return entities


    def _build_entities(self, doc: Doc) -> List[_LogicalEntity]:
        entities: List[_LogicalEntity] = []

        for ent in doc.ents:
            if ent.label_ != "LENTITY":
                continue
            entity = _LogicalEntity(name = ent.text)
            attributes: List[_LogicalAttribute] = []

            for relation in list(filter(lambda _:
                                        _[1]["ATTRIBUTE_OF"] 
                                        and _[1]["ATTRIBUTE_OF"] >= self._rel_threshold
                                        and _[0][1] == ent.start, doc._.rel.items())):
                attr = next(filter(lambda _:_.start == relation[0][0], doc.ents))
                if attr.label_ != "LATTRIBUTE":
                    continue
                attribute = _LogicalAttribute(name = attr.text)
                scores = next(filter(lambda _:_[0] == attr.start, doc._.ecat.items()))[1]
                max_scored = max(scores.items(), key=lambda scores:scores[1])
                attribute.type = max_scored[0] if max_scored[1] >= self._ecat_threshold else "string"
                attributes.append(attribute)
            
            entity.attributes = attributes
            entities.append(entity)

        return entities


    def assemble(self, doc: Doc) -> str:
        entities = self._build_entities(doc)
        entities = self._shapeshift_entities(entities)

        return json.dumps(entities, ensure_ascii=False, default=pydantic_encoder)