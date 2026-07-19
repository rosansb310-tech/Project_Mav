# core/services/app_service.py
from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.services.search_service import SearchService
from database.database import Database


class AppService:
    def __init__(self, database: Optional[Database] = None):
        self.database = database or Database()
        self.search = SearchService(self.database)

    def find_apps(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        return self.search.search_apps(query, limit=limit)

    def best_match(self, query: str) -> Optional[Dict[str, Any]]:
        return self.search.best_app_match(query)

    def favorite_app(self, app_name: str, favorite: bool = True):
        rows = self.database.get_apps()
        target = None

        for row in rows:
            if str(row["name"]).lower() == app_name.strip().lower():
                target = row
                break

        if not target:
            return False

        self.database.cursor.execute(
            """
            UPDATE apps
            SET favorite = ?
            WHERE path = ?
            """,
            (1 if favorite else 0, target["path"]),
        )
        self.database.connection.commit()
        return True