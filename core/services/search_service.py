# core/services/search_service.py
from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional

from database.database import Database


class SearchService:
    def __init__(self, database: Optional[Database] = None):
        self.database = database or Database()

    def search_files(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        rows = self.database.get_files()
        return self._rank_rows(
            rows=rows,
            query=query,
            limit=limit,
            name_key="name",
            path_key="path",
            type_label="file",
        )

    def search_projects(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        rows = self.database.get_projects()
        return self._rank_rows(
            rows=rows,
            query=query,
            limit=limit,
            name_key="name",
            path_key="path",
            type_label="project",
        )

    def search_apps(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        rows = self.database.get_apps()
        return self._rank_rows(
            rows=rows,
            query=query,
            limit=limit,
            name_key="name",
            path_key="path",
            type_label="app",
        )

    def best_file_match(self, query: str) -> Optional[Dict[str, Any]]:
        results = self.search_files(query, limit=1)
        return results[0] if results else None

    def best_project_match(self, query: str) -> Optional[Dict[str, Any]]:
        results = self.search_projects(query, limit=1)
        return results[0] if results else None

    def best_app_match(self, query: str) -> Optional[Dict[str, Any]]:
        results = self.search_apps(query, limit=1)
        return results[0] if results else None

    def _rank_rows(self, rows, query: str, limit: int, name_key: str, path_key: str, type_label: str):
        query = (query or "").strip().lower()
        if not query:
            return []

        tokens = [t for t in re.split(r"\s+", query) if t]
        ranked = []

        for row in rows:
            name = str(row[name_key] or "")
            path = str(row[path_key] or "")
            haystack = f"{name} {path}".lower()

            score = self._score(query, tokens, name.lower(), haystack, row)

            if score <= 0:
                continue

            ranked.append(
                {
                    "type": type_label,
                    "name": name,
                    "path": path,
                    "score": round(score, 4),
                    "row": dict(row),
                }
            )

        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[:limit]

    def _score(self, query: str, tokens: List[str], name: str, haystack: str, row) -> float:
        score = 0.0

        if query == name:
            score += 100.0

        if query in name:
            score += 60.0

        if query in haystack:
            score += 35.0

        for token in tokens:
            if token in name:
                score += 10.0
            elif token in haystack:
                score += 5.0

        ratio = SequenceMatcher(None, query, name).ratio()
        score += ratio * 30.0

        modified = row.get("modified") or row.get("last_modified") or 0
        favorite = row.get("favorite") or 0

        if favorite:
            score += 15.0

        if modified:
            score += min(float(modified) / 10_000_000_000, 5.0)

        return score