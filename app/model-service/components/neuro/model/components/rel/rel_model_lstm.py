from typing import List, Tuple, Callable

import spacy
from spacy.tokens import Doc, Span
from thinc.types import Floats2d, Ints1d, Ragged, cast, Padded
from thinc.api import Model, Linear, chain, Logistic, PyTorchLSTM, prefer_gpu, set_active_gpu, use_pytorch_for_gpu_memory

if prefer_gpu():
    set_active_gpu(0)
    use_pytorch_for_gpu_memory()


lstm_dim: int = 2  # FIXME
lin_layer = Linear(nO=None, nI=None)


@spacy.registry.architectures("rel_model.v1")
def create_relation_model(
    create_instance_tensor: Model[List[Doc], Floats2d],
    classification_layer: Model[Floats2d, Floats2d],
) -> Model[List[Doc], Floats2d]:
    with Model.define_operators({">>": chain}):
        model = create_instance_tensor >> classification_layer
        model.attrs["get_instances"] = create_instance_tensor.attrs["get_instances"]
    return model

@spacy.registry.misc("bilstm_layer_builder.v1")
def bilstm_layer_builder(nO:int = None, depth: int = 1) -> Callable[[int], Model[Padded, Padded]]:
    def create_layer(dim: int):
        return PyTorchLSTM(nO=nO or dim, nI=dim, bi=True, depth=depth)
    
    return create_layer
    


@spacy.registry.architectures("rel_classification_layer.v1")
def create_classification_layer(
    bilstm_builder: Callable[[int], Model[Padded, Padded]], nO: int = None
) -> Model[Floats2d, Floats2d]:
    with Model.define_operators({">>": chain}):
        lin_layer.set_dim("nO", nO, force=True)
        return lin_layer >> Logistic()


@spacy.registry.misc("rel_instance_generator.v1")
def create_instances(max_length: int) -> Callable[[Doc], List[Tuple[Span, Span]]]:
    def get_instances(doc: Doc) -> List[Tuple[Span, Span]]:
        instances = []
        for ent1 in doc.ents:
            for ent2 in doc.ents:
                if ent1 != ent2:
                    if max_length and abs(ent2.start - ent1.start) <= max_length:
                        instances.append((ent1, ent2))
        return instances
    
    return get_instances


@spacy.registry.architectures("rel_instance_tensor.v1")
def create_tensors(
    tok2vec: Model[List[Doc], List[Floats2d]],
    pooling: Model[Ragged, Floats2d],
    bilstm_builder: Callable[[int], Model[Padded, Padded]],
    get_instances: Callable[[Doc], List[Tuple[Span, Span]]],
) -> Model[List[Doc], Floats2d]:

    return Model(
        "instance_tensors",
        instance_forward,
        layers=[tok2vec, pooling],
        refs={"tok2vec": tok2vec, "pooling": pooling},
        attrs={"get_instances": get_instances, "bilstm_builder": bilstm_builder},
        init=instance_init,
    )


def instance_forward(model: Model[List[Doc], Floats2d], docs: List[Doc], is_train: bool) -> Tuple[Floats2d, Callable]:

    def convert_padded_to_floats2d(padded_tensor: Padded) -> Floats2d:
        data = padded_tensor.data
        lengths = padded_tensor.lengths
        mask = model.ops.asarray(greater(lengths, 0), dtype="float32")
        masked_data = data * mask
        return masked_data.astype("float32")
    
    def greater(list, compare) -> List[bool]:
        return [val > compare for val in list]

    pooling = model.get_ref("pooling")
    global lstm_dim, lin_layer
    tok2vec = model.get_ref("tok2vec")
    bilstm_builder = model.attrs["bilstm_builder"]
    get_instances = model.attrs["get_instances"]
    all_instances = [get_instances(doc) for doc in docs]
    tokvecs, bp_tokvecs = tok2vec(docs, is_train)

    ents = []
    lengths = []

    for doc_nr, (instances, tokvec) in enumerate(zip(all_instances, tokvecs)):
        token_indices = []
        for instance in instances:
            for ent in instance:
                token_indices.extend([i for i in range(ent.start, ent.end)])
                lengths.append(ent.end - ent.start)
        ents.append(tokvec[token_indices])
    lengths = cast(Ints1d, model.ops.asarray(lengths, dtype="int32"))
    entities = Ragged(model.ops.flatten(ents), lengths)
    # print("DIM: ", entities.data.shape)
    lstm_dim = entities.data.shape[1]
    # print("LSTM_DIM: ", lstm_dim)

    bilstm = bilstm_builder(lstm_dim)
    # print("FACT_DIM: ", bilstm.get_dim("nO"))
    bilstm_out, bp_bilstm_out = bilstm(entities, is_train)
    # converted_out = convert_padded_to_floats2d(bilstm_out)
    # bp_converted_out: Floats2d

    lin_layer = Linear(nO=lin_layer._dims["nO"], nI=bilstm.get_dim("nO"))
    pooled, bp_pooled = pooling(bilstm_out, is_train)
    

    # Reshape so that pairs of rows are concatenated
    relations = model.ops.reshape2f(pooled, -1, pooled.shape[1] * 2)

    def backprop(d_relations: Floats2d) -> List[Doc]:
        d_bilstm_out = model.ops.reshape2f(d_relations, d_relations.shape[0] * 2, -1)
        d_ents = bp_pooled(d_bilstm_out).data
        d_tokvecs = []
        ent_index = 0
        for doc_nr, instances in enumerate(all_instances):
            shape = tokvecs[doc_nr].shape
            d_tokvec = model.ops.alloc2f(*shape)
            count_occ = model.ops.alloc2f(*shape)
            for instance in instances:
                for ent in instance:
                    d_tokvec[ent.start : ent.end] += d_ents[ent_index]
                    count_occ[ent.start : ent.end] += 1
                    ent_index += ent.end - ent.start
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