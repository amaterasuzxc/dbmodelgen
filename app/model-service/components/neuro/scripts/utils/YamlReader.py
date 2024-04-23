import yaml


class DotDict(dict):
    # dot-notation access to dictionary attributes
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def read(path: str) -> DotDict:
        with open(path) as file:
            yaml_dict = yaml.full_load(file)
        return DotDict(yaml_dict)