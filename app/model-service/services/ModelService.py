import threading as thr

from exceptions.MsConflictError import MsConflictError
from exceptions.MsInternalError import MsInternalError
from components.neuro.model.PipelineModel import PipelineModel
from util.RootPathResolver import resolve_project_path as resolver


class ModelService:
    def __init__(self) -> None:
        self._model = PipelineModel("config/pipeline_config.yml", resolver)
        self._lock = thr.Lock()
        

    def get_model_response(self, text: str) -> str:
        if self._lock.acquire(blocking=False):
            try:
                return self._model.apply(text)
            except Exception:
                raise MsInternalError(message="Something went wrong")
            finally:
                self._lock.release()
        else:
            raise MsConflictError(message="Service is busy with processing another task at this moment")
            