from skills.base.skill import Skill
from core.services.project_service import ProjectService
from drivers.windows.system import WindowsSystem


class OpenProjectSkill(Skill):
    name = "open_project"

    description = "Open a project folder or workspace."

    commands = [
        "project",
        "open_project"
    ]

    def __init__(self):
        self.project_service = ProjectService()

    def parse(self, parts):
        return {
            "query": " ".join(parts)
        }

    def execute(self, **kwargs):
        query = kwargs["query"].strip()
        match = self.project_service.best_match(query)

        if not match:
            return f"No project found for: {query}"

        project_path = match["path"]
        entry_file = self.project_service.get_entry_file(match)

        if entry_file:
            WindowsSystem.open_folder(project_path)
            return f"Opened project: {match['name']} ({entry_file})"

        return WindowsSystem.open_folder(project_path)