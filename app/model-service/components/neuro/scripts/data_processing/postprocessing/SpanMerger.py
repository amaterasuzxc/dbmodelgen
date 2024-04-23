from typing import Dict, List, Tuple
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from copy import deepcopy

from ...utils.YamlReader import read as read_yaml
from components.neuro.scripts.data_processing.postprocessing.CompositionFinder import CompositionFinder


class SpanMerger:
    def __init__(self, config_path: str) -> None:
        self._config = read_yaml(config_path)
        self._composition_finder = CompositionFinder(config_path=config_path)
        self._labels = self._config.labels


    def _resolve_groups(self, doc: Doc) -> Dict[str, List[Span]]:
        spans = doc.ents
        groups = {}

        for label in self._labels:
            groups[label] = list(filter(lambda _:_.label_ == label, spans))

        return groups
    
    
    @staticmethod
    def _merge_group_full_matches(spans: List[Span]) -> Dict[Span, List[Span]]:
        merged = {}
        lists = []
        present = []

        for check_span in spans:
            if check_span in present:
                continue

            current_group = []

            for compare_span in spans:
                if check_span.lemma_ == compare_span.lemma_:
                    present.append(compare_span)
                    current_group.append(compare_span)

            lists.append(current_group)

        for lst in lists:
            first_span = sorted(lst, key=lambda _:_.start)[0]
            lst.remove(first_span)
            merged[first_span] = lst

        return merged
    
    
    def _process_dependencies(self, doc: Doc, span_groups: Dict[Span, List[Span]]) -> Doc:

        def _merge_relations(rel: Dict[Tuple[int, int], Dict[str, float]], span_keys: Tuple[int, int], coref_keys: Tuple[int, int], direct: bool = True) -> None:
            compare_idx = 1 if direct else 0
            not_processed = deepcopy(coref_keys)

            for span_key in span_keys:
                if span_key not in rel:
                    continue
                max_score = max(rel[span_key].values())
                for coref_key in coref_keys:
                    if coref_key not in rel:
                        continue
                    if coref_key[compare_idx] == span_key[compare_idx]:
                        curr_max = max(rel[coref_key].values())
                        if curr_max > max_score:
                            max_score = curr_max
                            not_processed.remove(coref_key)
                            rel[span_key] = rel.pop(coref_key)
            
            for key in not_processed:
                if key not in rel:
                    continue

                new_key = (span_keys[0][0], key[1]) if direct else (key[0], span_keys[0][1])
                rel[new_key] = rel.pop(key)
                    

        relations = doc._.rel
        categories = doc._.ecat
        new_spans = [span for span, g in span_groups.items()]

        for span, group in span_groups.items():
            if not group:
                continue

            ecat_max = 0
            span_rel_direct_keys = list(filter(lambda _:_[0] == span.start, relations.keys()))
            span_rel_reverse_keys = list(filter(lambda _:_[1] == span.start, relations.keys()))

            if span.start in categories:
                ecat_max = max(categories[span.start].values())

            for coref in group:
                coref_rel_direct_keys = list(filter(lambda _:_[0] == coref.start, relations.keys()))
                coref_rel_reverse_keys = list(filter(lambda _:_[1] == coref.start, relations.keys()))

                if coref.start not in categories and not coref_rel_direct_keys and not coref_rel_reverse_keys:
                    continue

                if coref.start in categories:
                    curr_ecat_max = max(categories[coref.start].values())

                    if curr_ecat_max > ecat_max:
                        ecat_max = curr_ecat_max
                        categories[span.start] = categories.pop(coref.start)

                if coref_rel_direct_keys:
                    _merge_relations(
                        rel=relations, 
                        span_keys=span_rel_direct_keys, 
                        coref_keys=coref_rel_direct_keys)
                    
                if coref_rel_reverse_keys:
                    _merge_relations(
                        rel=relations, 
                        span_keys=span_rel_reverse_keys, 
                        coref_keys=coref_rel_reverse_keys,
                        direct=False)

        doc.ents = new_spans

        return doc


    def _merge_full_matches(self, doc: Doc) -> Doc:
        groups = self._resolve_groups(doc)
        merged_entity_groups = {}

        for k, group in groups.items():
            merged_entity_groups = merged_entity_groups | self._merge_group_full_matches(group)

        doc = self._process_dependencies(doc, merged_entity_groups)

        return doc
    
            
    def merge(self, doc: Doc) -> Doc:
        new_doc = deepcopy(doc)
        new_doc = self._merge_full_matches(doc)
        compositions = self._composition_finder.find(new_doc)
        new_doc = self._process_dependencies(new_doc, compositions)
        
        return new_doc