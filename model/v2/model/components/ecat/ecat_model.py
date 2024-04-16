from typing import List, Tuple, Callable

import spacy
from spacy.tokens import Doc, Span
from thinc.types import Floats2d, Ints1d, Ragged, cast
from thinc.api import Model, Linear, chain, Softmax_v2


@spacy.registry.architectures("ecat_model.v1")
def create_attribute_classification_model(
    create_entity_tensor: Model[List[Doc], Floats2d],
    classification_layer: Model[Floats2d, Floats2d],
) -> Model[List[Doc], Floats2d]:
    with Model.define_operators({">>": chain}):
        model = create_entity_tensor >> classification_layer
        model.attrs["get_entities"] = create_entity_tensor.attrs["get_entities"]
    return model


@spacy.registry.architectures("ecat_classification_layer.v1")
def create_classification_layer(
    nO: int = None, nI: int = None
) -> Model[Floats2d, Floats2d]:
    with Model.define_operators({">>": chain}):
        return Linear(nO=nO, nI=nI) >> Softmax_v2()


@spacy.registry.misc("ecat_entity_finder.v1")
def get_entities(target: Tuple[str]) -> Callable[[Doc], List[Span]]:
    target = [str.lower(label) for label in target]
    def find_entities(doc: Doc) -> List[Span]:
        entities = []
        for entity in doc.ents:
            if (str.lower(entity.label_) in target):
                entities.append(entity)

        return entities
    
    return find_entities


@spacy.registry.architectures("ecat_entity_tensor.v1")
def create_tensors(
    tok2vec: Model[List[Doc], List[Floats2d]],
    pooling: Model[Ragged, Floats2d],
    get_entities: Callable[[Doc], List[Span]],
) -> Model[List[Doc], Floats2d]:

    return Model(
        "entity_tensors",
        instance_forward,
        layers=[tok2vec, pooling],
        refs={"tok2vec": tok2vec, "pooling": pooling},
        attrs={"get_entities": get_entities},
        init=instance_init,
    )


def instance_forward(model: Model[List[Doc], Floats2d], docs: List[Doc], is_train: bool) -> Tuple[Floats2d, Callable]:
    pooling = model.get_ref("pooling")
    tok2vec = model.get_ref("tok2vec")
    get_entities = model.attrs["get_entities"]
    all_entities = [get_entities(doc) for doc in docs]
    tokvecs, bp_tokvecs = tok2vec(docs, is_train)

    ents = []
    lengths = []

    for doc_nr, (entities, tokvec) in enumerate(zip(all_entities, tokvecs)):
        token_indices = []
        for entity in entities:
            token_indices.extend([i for i in range(entity.start, entity.end)])
            lengths.append(entity.end - entity.start)
        ents.append(tokvec[token_indices])
    lengths = cast(Ints1d, model.ops.asarray(lengths, dtype="int32"))
    entities = Ragged(model.ops.flatten(ents), lengths)
    relations, bp_pooled = pooling(entities, is_train)

    def backprop(d_categories: Floats2d) -> List[Doc]:
        d_pooled = d_categories
        d_ents = bp_pooled(d_pooled).data
        d_tokvecs = []
        ent_index = 0
        for doc_nr, entities in enumerate(all_entities):
            shape = tokvecs[doc_nr].shape
            d_tokvec = model.ops.alloc2f(*shape)
            count_occ = model.ops.alloc2f(*shape)
            for entity in entities:
                d_tokvec[entity.start : entity.end] += d_ents[ent_index]
                count_occ[entity.start : entity.end] += 1
                ent_index += entity.end - entity.start
            d_tokvec /= count_occ + 0.00000000001
            d_tokvecs.append(d_tokvec)

        d_docs = bp_tokvecs(d_tokvecs)
        return d_docs

    return relations, backprop


def instance_init(model: Model, X: List[Doc] = None, Y: Floats2d = None) -> Model:
    tok2vec = model.get_ref("tok2vec")
    if X is not None:
        tok2vec.initialize(X)
    return model