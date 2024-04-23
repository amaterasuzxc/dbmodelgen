from itertools import islice
from typing import Tuple, List, Iterable, Optional, Dict, Callable, Any

from spacy.scorer import PRFScore
from thinc.types import Floats2d
import numpy
from spacy.training.example import Example
from thinc.api import Model, Optimizer
from spacy.tokens.doc import Doc
from spacy.pipeline.trainable_pipe import TrainablePipe
from spacy.vocab import Vocab
from spacy import Language
from thinc.model import set_dropout_rate
from wasabi import Printer


Doc.set_extension("ecat", default={}, force=True)
msg = Printer()


@Language.factory(
    "entity_categorizer",
    requires=["doc.ents", "token.ent_iob", "token.ent_type"],
    assigns=["doc._.ecat"],
    default_score_weights={
        "ecat_micro_p": None,
        "ecat_micro_r": None,
        "ecat_micro_f": None,
    },
)
def make_entity_categorizer(
    nlp: Language, name: str, model: Model, *, threshold: float
):
    """Construct a EntityCategorizer component."""
    return EntityCategorizer(nlp.vocab, model, name, threshold=threshold)


class EntityCategorizer(TrainablePipe):
    def __init__(
        self,
        vocab: Vocab,
        model: Model,
        name: str = "ecat",
        *,
        threshold: float
    ) -> None:
        """Initialize an entity categorizer."""
        self.vocab = vocab
        self.model = model
        self.name = name
        self.cfg = {"labels": [], "threshold": threshold}

    @property
    def labels(self) -> Tuple[str]:
        """Returns the labels currently added to the component."""
        return tuple(self.cfg["labels"])

    @property
    def threshold(self) -> float:
        """Returns the threshold above which a prediction is seen as 'True'."""
        return self.cfg["threshold"]

    def add_label(self, label: str) -> int:
        """Add a new label to the pipe."""
        if not isinstance(label, str):
            raise ValueError("Only strings can be added as labels to the EntityCategorizer")
        if label in self.labels:
            return 0
        self.cfg["labels"] = list(self.labels) + [label]
        return 1

    def __call__(self, doc: Doc) -> Doc:
        """Apply the pipe to a Doc."""
        # check that there are actually any candidate entities in this batch of examples
        total_entities = len(self.model.attrs["get_entities"](doc))
        if total_entities == 0:
            msg.info("Could not determine any entities of defined types in doc - returning doc as is.")
            return doc

        predictions = self.predict([doc])
        self.set_annotations([doc], predictions)
        return doc

    def predict(self, docs: Iterable[Doc]) -> Floats2d:
        """Apply the pipeline's model to a batch of docs, without modifying them."""
        get_entities = self.model.attrs["get_entities"]
        total_entities = sum([len(get_entities(doc)) for doc in docs])
        if total_entities == 0:
            msg.info("Could not determine any entities of defined types in any docs - can not make any predictions.")
        scores = self.model.predict(docs)
        return self.model.ops.asarray(scores)

    def set_annotations(self, docs: Iterable[Doc], scores: Floats2d) -> None:
        """Modify a batch of `Doc` objects, using pre-computed scores."""
        c = 0
        get_entities = self.model.attrs["get_entities"]
        for doc in docs:
            for ent in get_entities(doc):
                offset = ent.start
                if offset not in doc._.ecat:
                    doc._.ecat[offset] = {}
                for j, label in enumerate(self.labels):
                    doc._.ecat[offset][label] = scores[c, j]
                c += 1

    def update(
        self,
        examples: Iterable[Example],
        *,
        drop: float = 0.0,
        set_annotations: bool = False,
        sgd: Optional[Optimizer] = None,
        losses: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """Learn from a batch of documents and gold-standard information,
        updating the pipe's model. Delegates to predict and get_loss."""
        if losses is None:
            losses = {}
        losses.setdefault(self.name, 0.0)
        set_dropout_rate(self.model, drop)

        # check that there are actually any candidate instances in this batch of examples
        total_entities = 0
        for eg in examples:
            total_entities += len(self.model.attrs["get_entities"](eg.predicted))
        if total_entities == 0:
            msg.info("Could not determine any entities of defined types in doc.")
            return losses

        # run the model
        docs = [eg.predicted for eg in examples]
        predictions, backprop = self.model.begin_update(docs)
        loss, gradient = self.get_loss(examples, predictions)
        backprop(gradient)
        if sgd is not None:
            self.model.finish_update(sgd)
        losses[self.name] += loss
        if set_annotations:
            self.set_annotations(docs, predictions)
        return losses

    def get_loss(self, examples: Iterable[Example], scores) -> Tuple[float, float]:
        """Find the loss and gradient of loss for the batch of documents and
        their predicted scores."""
        truths = self._examples_to_truth(examples)
        gradient = scores - truths
        mean_square_error = (gradient ** 2).sum(axis=1).mean()
        return float(mean_square_error), gradient

    def initialize(
        self,
        get_examples: Callable[[], Iterable[Example]],
        *,
        nlp: Language = None,
        labels: Optional[List[str]] = None,
    ):
        """Initialize the pipe for training, using a representative set
        of data examples.
        """
        if labels is not None:
            for label in labels:
                self.add_label(label)
        else:
            for example in get_examples():
                categories = example.reference._.ecat
                for indices, label_dict in categories.items():
                    for label in label_dict.keys():
                        self.add_label(label)
        self._require_labels()

        subbatch = list(islice(get_examples(), 10))
        doc_sample = [eg.reference for eg in subbatch]
        label_sample = self._examples_to_truth(subbatch, True)
        if label_sample is None:
            raise ValueError("Call begin_training with relevant entities and categories annotated in "
                             "at least a few reference examples!")
        self.model.initialize(X=doc_sample, Y=label_sample)

    def _examples_to_truth(self, examples: List[Example], init: bool = False) -> Optional[numpy.ndarray]:
        # check that there are actually any candidate instances in this batch of examples
        nr_instances = 0
        for eg in examples:
            nr_instances += len(self.model.attrs["get_entities"](eg.reference if init else eg.predicted))
        if nr_instances == 0:
            return None

        truths = numpy.zeros((nr_instances, len(self.labels)), dtype="f")
        c = 0
        for i, eg in enumerate(examples):
            for ent in self.model.attrs["get_entities"](eg.reference if init else eg.predicted):
                gold_label_dict = eg.reference._.ecat.get(ent.start, {})
                for j, label in enumerate(self.labels):
                    truths[c, j] = gold_label_dict.get(label, 0)
                c += 1

        truths = self.model.ops.asarray(truths)
        return truths

    def score(self, examples: Iterable[Example], **kwargs) -> Dict[str, Any]:
        """Score a batch of examples."""
        return score_categories(examples, self.threshold)


def score_categories(examples: Iterable[Example], threshold: float) -> Dict[str, Any]:
    """Score a batch of examples."""
    micro_prf = PRFScore()
    for example in examples:
        gold = example.reference._.ecat
        pred = example.predicted._.ecat
        for key, pred_dict in pred.items():
            if key not in gold.keys():
                for k, v in pred_dict.items():
                    if v >= threshold:
                        micro_prf.fp += 1
                continue
        for key, pred_dict in pred.items():
            gold_labels = [k for (k, v) in gold.get(key, {}).items() if v == 1.0]
            for k, v in pred_dict.items():
                if v >= threshold:
                    if k in gold_labels:
                        micro_prf.tp += 1
                    else:
                        micro_prf.fp += 1
                else:
                    if k in gold_labels:
                        micro_prf.fn += 1
    return {
        "ecat_micro_p": micro_prf.precision,
        "ecat_micro_r": micro_prf.recall,
        "ecat_micro_f": micro_prf.fscore,
    }