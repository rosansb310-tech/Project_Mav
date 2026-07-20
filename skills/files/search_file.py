from skills.base.skill import Skill
from core.services.search_service import SearchService


class SearchFileSkill(Skill):
    name = "search_file"

    description = "Search for an indexed file."

    commands = [
        "find",
        "search_file",
        "file"
    ]

    def __init__(self):
        self.search_service = SearchService()

    def parse(self, parts):
        return {
            "query": " ".join(parts)
        }

    def execute(self, **kwargs):
        query = kwargs["query"].strip()
        results = self.search_service.search_files(query, limit=5)

        if not results:
            return f"No file found for: {query}"

        lines = []
        for item in results:
            lines.append(f"{item['name']} -> {item['path']}")

        return "\n".join(lines)