class Entity:
    name: str
    attributes = []

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes