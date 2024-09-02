

class Image:
    def __init__(self, registry, name, tag):
        self.registry = registry
        self.name = name
        self.tag = tag

    def to_link(self) -> str:
        return f'{self.registry}/{self.name}:{self.tag}'