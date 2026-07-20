from skills.base.skill import Skill
from drivers.windows.system import WindowsSystem


class OpenAppSkill(Skill):
    name = "open_app"

    description = "Launch an application."

    commands = [
        "open",
        "launch",
        "start",
        "run"
    ]

    def parse(self, parts):
        return {
            "app": " ".join(parts)
        }

    def execute(self, **kwargs):
        return WindowsSystem.open_app(kwargs["app"])