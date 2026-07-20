# core/registry.py

import importlib
import inspect
import pkgutil
import traceback

import skills
from skills.base.skill import Skill


class SkillRegistry:

    def __init__(self):
        self.skills = {}
        self.load_skills()

    def load_skills(self):

        print("\n========== Loading Skills ==========\n")

        for _, module_name, _ in pkgutil.walk_packages(
            skills.__path__,
            skills.__name__ + "."
        ):

            try:

                module = importlib.import_module(module_name)

                for _, obj in inspect.getmembers(module):

                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, Skill)
                        and obj is not Skill
                    ):

                        skill = obj()

                        self.register(skill)

                        print(f"[OK] {module_name}")

            except Exception as e:

                print(f"\n[FAILED] {module_name}")
                traceback.print_exc()

        print("\n====================================")
        print(f"Loaded {len(self.skills)} commands.")
        print("====================================\n")

    def register(self, skill):

        for command in skill.commands:
            self.skills[command] = skill

    def get(self, command):

        return self.skills.get(command)