# database/database.py
import sqlite3
from pathlib import Path
from typing import Iterable, Optional, Sequence


class Database:
    def __init__(self, db_path: Optional[str] = None):
        path = Path(db_path) if db_path else Path("database") / "mav.db"
        path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                extension TEXT,
                path TEXT UNIQUE NOT NULL,
                modified REAL
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                path TEXT UNIQUE NOT NULL,
                language TEXT,
                git_repo INTEGER DEFAULT 0,
                entry_file TEXT,
                metadata TEXT,
                last_modified REAL
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS apps(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT UNIQUE NOT NULL,
                source TEXT,
                modified REAL,
                favorite INTEGER DEFAULT 0
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS preferences(
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )

        self.connection.commit()

    def insert_file(self, name, extension, path, modified):
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO files
            (
                name,
                extension,
                path,
                modified
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (name, extension, path, modified),
        )
        self.connection.commit()

    def insert_project(self, name, path, language, modified, git_repo=0, entry_file=None, metadata=None):
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO projects
            (
                name,
                path,
                language,
                git_repo,
                entry_file,
                metadata,
                last_modified
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (name, path, language, int(bool(git_repo)), entry_file, metadata, modified),
        )
        self.connection.commit()

    def insert_app(self, name, path, source=None, modified=None, favorite=0):
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO apps
            (
                name,
                path,
                source,
                modified,
                favorite
            )
            VALUES
            (
                ?, ?, ?, ?, ?
            )
            """,
            (name, path, source, modified, int(bool(favorite))),
        )
        self.connection.commit()

    def get_files(self):
        self.cursor.execute(
            """
            SELECT
                name,
                extension,
                path,
                modified
            FROM files
            ORDER BY name
            """
        )
        return self.cursor.fetchall()

    def get_projects(self):
        self.cursor.execute(
            """
            SELECT
                name,
                path,
                language,
                git_repo,
                entry_file,
                metadata,
                last_modified
            FROM projects
            ORDER BY name
            """
        )
        return self.cursor.fetchall()

    def get_apps(self):
        self.cursor.execute(
            """
            SELECT
                name,
                path,
                source,
                modified,
                favorite
            FROM apps
            ORDER BY favorite DESC, name
            """
        )
        return self.cursor.fetchall()

    def clear_files(self):
        self.cursor.execute("DELETE FROM files")
        self.connection.commit()

    def clear_projects(self):
        self.cursor.execute("DELETE FROM projects")
        self.connection.commit()

    def clear_apps(self):
        self.cursor.execute("DELETE FROM apps")
        self.connection.commit()

    def clear_all(self):
        self.clear_files()
        self.clear_projects()
        self.clear_apps()

    def set_preference(self, key: str, value: str):
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO preferences(key, value)
            VALUES(?, ?)
            """,
            (key, value),
        )
        self.connection.commit()

    def get_preference(self, key: str):
        self.cursor.execute(
            """
            SELECT value
            FROM preferences
            WHERE key = ?
            """,
            (key,),
        )
        row = self.cursor.fetchone()
        return row["value"] if row else None

    def close(self):
        self.connection.close()