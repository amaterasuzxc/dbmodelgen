import os
import sys

def resolve_project_path(path: str) -> str:
     root = min(list(filter(lambda __:__ not in ["", " "], sys.path)))
     return os.path.join(root, path)