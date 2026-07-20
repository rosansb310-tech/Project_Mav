from core.registry import SkillRegistry
from core.executor import Executor


class Router:
    def __init__(self):
        self.registry = SkillRegistry()
        self.executor = Executor()

    def route(self, command):
        parts = command.strip().split()

        if not parts:
            return

        action = parts[0].lower()
        skill = self.registry.get(action)

        if skill is None:
            print("Unknown command.")
            return

        kwargs = skill.parse(parts[1:])
        self.executor.execute(skill, **kwargs)