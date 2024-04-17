from typing import Dict, List
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span

from scripts.data_processing.postprocessing.composition_finder import CompositionFinder


class SpanMerger: # TODO
    def __init__(self) -> None:
        self._composition_finder = CompositionFinder()

    def merge(self, doc: Doc) -> Doc:
        compositions = self._composition_finder.find(doc)
        
        return doc