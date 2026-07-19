import importlib
import inspect
import pkgutil

from skills.base.skill import Skill
import skills


class SkillRegistry:

    def __init__(self):

        self.skills = {}

        self.load_skills()

    def load_skills(self):

        for _, module_name, _ in pkgutil.walk_packages(
            skills.__path__,
            skills.__name__ + "."
        ):

            try:

                module = importlib.import_module(module_name)

            except Exception:
                continue

            for _, obj in inspect.getmembers(module):

                if (
                    inspect.isclass(obj)
                    and issubclass(obj, Skill)
                    and obj is not Skill
                ):

                    skill = obj()

                    self.register(skill)

        print(f"Loaded {len(self.skills)} commands.")

    def register(self, skill):

        for command in skill.commands:

            self.skills[command] = skill

    def get(self, command):

        return self.skills.get(command)