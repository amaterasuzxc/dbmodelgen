import spacy
from spacy.tokens.doc import Doc

import scripts.utils.yaml_to_dict_reader as yaml_reader
from scripts.utils.path_resolver import resolve_project_path as resolve_path
from scripts.data_processing.postprocessing.doc_cleaner import Cleaner
from scripts.data_processing.postprocessing.span_merger import SpanMerger
from scripts.data_processing.postprocessing.json_assembler import JsonAssembler
from model.components import component_registry

class PipelineModel:
    def __init__(self, config_path: str) -> None:
        self._pipeline_config = yaml_reader.read(config_path)
        self._rel_threshold = float(self._pipeline_config.rel_threshold)
        self._ecat_threshold = float(self._pipeline_config.ecat_threshold)
        self._model = spacy.load(resolve_path(self._pipeline_config.ner))
        self._rel = spacy.load(resolve_path(self._pipeline_config.rel))
        self._ecat = spacy.load(resolve_path(self._pipeline_config.ecat))
        self._pretrained_ru_pipe = spacy.load("ru_core_news_sm")
        self._model.add_pipe(self._rel.component_names[0], name=f"rel_{self._rel.component_names[0]}", source=self._rel)
        self._model.add_pipe("relation_extractor", source=self._rel, last=True)
        self._model.add_pipe(self._ecat.component_names[0], name=f"ecat_{self._ecat.component_names[0]}", source=self._ecat)
        self._model.add_pipe("entity_categorizer", source=self._ecat, last=True)
        self._model.add_pipe("lemmatizer", source=self._pretrained_ru_pipe, last=True)
        self._cleaner = Cleaner(config_path=resolve_path(self._pipeline_config.cleaner_config))
        self._merger = SpanMerger(config_path=resolve_path(self._pipeline_config.merger_config))
        self._json_assembler = JsonAssembler(rel_threshold=self._rel_threshold, ecat_threshold=self._ecat_threshold)

    
    def _get_predictions(self, text: str) -> Doc:
        return self._model(text)
    

    def _postprocess(self, doc: Doc) -> Doc:
        doc = self._cleaner.clean(doc)
        doc = self._merger.merge(doc)

        return doc
    

    def _assemble_json(self, doc: Doc) -> str:
        return self._json_assembler.assemble(doc)
    

    def apply(self, text: str) -> str:
        model_out = self._get_predictions(text)
        processed_out = self._postprocess(model_out)

        return self._assemble_json(processed_out)