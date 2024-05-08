from copy import deepcopy
from typing import Callable, List, Tuple
from spacy.tokens.doc import Doc
from spacy.tokens.token import Token
from spacy.tokens.span import Span

from ...utils.YamlReader import read as read_yaml


class Cleaner:
    def __init__(self, config_path: str) -> None:
        self._config = read_yaml(config_path)
        self._stopwords = self._config.stopwords
        self._punct = self._config.punct
        self._trims = self._config.trims
        self._processors = [self._process_stopwords, self._process_punct, self._process_trims]
        self._current_tokens: List[Token] = []


    def _process_generic(self, span: Span, invalids: List[str]) -> Span:
        if span is None:
            return span
        
        invalids_set = set(invalids)

        while True:
            start_token = self._current_tokens[span.start]
            end_token = self._current_tokens[span.end - 1]
            changed = False

            if invalids_set.intersection({start_token.text, end_token.text}):
                if start_token.text in invalids_set:
                    span.start += 1
                    changed = True
                if end_token.text in invalids_set:
                    span.end -= 1
                    changed = True

            if not changed:
                break
            elif span.start >= span.end:
                return None

        return span
    

    def _process_stopwords(self, span: Span) -> Span:
        return self._process_generic(span, self._stopwords)
    
        
    def _process_punct(self, span: Span) -> Span:
        return self._process_generic(span, self._punct)
    

    def _process_trims(self, span: Span) -> Span:
        return self._process_generic(span, self._trims)
    

    @staticmethod
    def _process_token(span: Span, processor: Callable[[Span], Span]) -> Span:
        return processor(span)
    
    
    @staticmethod
    def _apply_processing_pipeline(span: Span, pipeline: List[Callable[[Span], Span]]) -> Span:
        for processor in pipeline:
            span = processor(span)

        return span
    
    
    def _resolve_new_spans(self, doc: Doc, all_spans: List[Tuple[Span, Span]]) -> Doc:
        relations = doc._.rel
        categories = doc._.ecat
        new_spans = list(filter(lambda _:_ is not None, [new_span for (o, new_span) in all_spans]))
        
        for (old_span, new_span) in all_spans:
            rel_direct_keys = [key[1] for key in list(filter(lambda _:_[0] == old_span.start, relations.keys()))]
            rel_reverse_keys = [key [0] for key in list(filter(lambda _:_[1] == old_span.start, relations.keys()))]

            if old_span.start not in categories and not rel_direct_keys and not rel_reverse_keys:
                continue

            if new_span is None:
                if old_span.start in categories:
                    categories.pop(old_span.start)
                for dk in rel_direct_keys:
                    relations.pop((old_span.start, dk))
                for rk in rel_reverse_keys:
                    relations.pop((rk, old_span.start))
            elif new_span.start != old_span.start:
                if old_span.start in categories:
                    categories[new_span.start] = categories.pop(old_span.start)
                for dk in rel_direct_keys:
                    relations[(new_span.start, dk)] = relations.pop((old_span.start, dk))
                for rk in rel_reverse_keys:
                    relations[(rk, new_span.start)] = relations.pop((rk, old_span.start))

        doc.ents = new_spans

        return doc
                    

    def clean(self, doc: Doc) -> Doc:
        self._current_tokens = [tok for tok in doc]
        processing_pipeline = self._processors
        new_doc = deepcopy(doc)
        temp_doc = deepcopy(doc)
        old_spans = temp_doc.ents
        new_spans = temp_doc.ents

        for span in new_spans:
            span = self._apply_processing_pipeline(span, processing_pipeline)

        all_spans = list(zip(old_spans, new_spans))
        new_doc = self._resolve_new_spans(new_doc, all_spans)
        
        return new_doc 