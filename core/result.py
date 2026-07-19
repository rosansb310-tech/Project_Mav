from dataclasses import dataclass, field


@dataclass
class Result:

    success: bool
    message: str = ""
    data: dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }

    def __str__(self):

        return str(self.to_dict())