# core/services/project_service.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from core.services.search_service import SearchService
from database.database import Database


class ProjectService:
    def __init__(self, database: Optional[Database] = None):
        self.database = database or Database()
        self.search = SearchService(self.database)

    def find_projects(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        return self.search.search_projects(query, limit=limit)

    def best_match(self, query: str) -> Optional[Dict[str, Any]]:
        return self.search.best_project_match(query)

    def get_entry_file(self, project_row: Dict[str, Any]) -> Optional[str]:
        entry = project_row.get("entry_file")
        if entry:
            return entry

        path = Path(project_row["path"])
        candidates = [
            "main.py",
            "app.py",
            "index.js",
            "index.ts",
            "index.tsx",
            "main.js",
            "main.ts",
        ]

        for candidate in candidates:
            if (path / candidate).exists():
                return candidate

        return None

    def project_summary(self, project_row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": project_row.get("name"),
            "path": project_row.get("path"),
            "language": project_row.get("language"),
            "git_repo": bool(project_row.get("git_repo")),
            "entry_file": self.get_entry_file(project_row),
            "metadata": project_row.get("metadata"),
            "last_modified": project_row.get("last_modified"),
        }