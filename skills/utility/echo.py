from skills.base.skill import Skill
from core.result import Result


class EchoSkill(Skill):

    name = "echo"
    description = "Prints text."

    commands = [
        "echo",
        "say",
        "print"
    ]

    def parse(self, parts):

        return {
            "message": " ".join(parts)
        }

    def execute(self, **kwargs):

        message = kwargs.get("message", "")

        print(message)

        return Result(
            success=True,
            message=message
        )