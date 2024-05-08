from typing import Dict, List
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from spacy.tokens.token import Token
from copy import deepcopy
import re

from ...utils.YamlReader import read as read_yaml


class CompositionFinder:
    def __init__(self, config_path: str) -> None:
        self._config = read_yaml(config_path)
        self._labels = self._config.labels


    def _resolve_groups(self, doc: Doc) -> Dict[str, List[Span]]:
        spans = doc.ents
        groups = {}

        for label in self._labels:
            groups[label] = list(filter(lambda _:_.label_ == label, spans))

        return groups
    

    @staticmethod
    def _process_group(group: List[Span]) -> Dict[Span, List[Span]]:
        processed = {}
        not_roots = []
        lists = []

        for check_span in sorted(group, key=lambda _:len(_.text)):
            if check_span in not_roots:
                continue

            compositions = []

            for compare_span in sorted(group, key=lambda _:len(_.text)):
                pattern = r"^" + re.escape(check_span.lemma_) + r"(\s.*)?$"
                if re.fullmatch(pattern, compare_span.lemma_):
                    not_roots.append(compare_span)
                    compositions.append(compare_span)

            lists.append(compositions)
        
        for lst in lists:
            first_span = sorted(lst, key=lambda _:_.start)[0]
            lst.remove(first_span)
            processed[first_span] = lst

        return processed
    

    def find(self, doc: Doc) -> Dict[Span, List[Span]]:
        new_doc = deepcopy(doc)
        groups = self._resolve_groups(new_doc)
        found_compositions = {}
        
        for k, group in groups.items():
            found_compositions = found_compositions | self._process_group(group)

        return found_compositions