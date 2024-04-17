from typing import List, Dict, Any
from spacy.tokens.doc import Doc



class LogicalAttribute:
    def __init__(self, name: str) -> None:
        self.name = name

    @property
    def name(self) -> str:
        return self.name


class LogicalEntity:
    def __init__(self, name: str) -> None:
        self.name = name
        self.attributes: List[LogicalAttribute] = []

    @property
    def name(self) -> str:
        return self.name
    
    @property
    def attributes(self) -> List[LogicalAttribute]:
        return self.attributes
    

class JsonAssembler: # TODO
    def __init__(self) -> None:
        pass

    def assemble(self, doc: Doc) -> Dict[str, Any]:
        pass