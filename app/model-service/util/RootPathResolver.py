import os

from definitions import ROOT

def resolve_project_path(path: str) -> str:
     return os.path.join(ROOT, path)