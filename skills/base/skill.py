from abc import ABC, abstractmethod


class Skill(ABC):

    name = ""
    description = ""
    commands = []

    @abstractmethod
    def parse(self, parts):
        """Convert command parts into kwargs."""
        pass

    @abstractmethod
    def execute(self, **kwargs):
        pass