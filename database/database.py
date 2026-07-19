import sqlite3
from pathlib import Path


class Database:

    def __init__(self):

        db_path = Path("database") / "mav.db"

        db_path.parent.mkdir(exist_ok=True)

        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS files(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,
            extension TEXT,
            path TEXT UNIQUE NOT NULL,
            modified REAL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,
            path TEXT UNIQUE,
            language TEXT,
            last_modified REAL
        )
        """)

        self.connection.commit()

    def insert_file(self, name, extension, path, modified):

        self.cursor.execute("""
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
        """, (
            name,
            extension,
            path,
            modified
        ))

        self.connection.commit()

    def insert_project(self, name, path, language, modified):

        self.cursor.execute("""
        INSERT OR REPLACE INTO projects
        (
            name,
            path,
            language,
            last_modified
        )
        VALUES
        (
            ?, ?, ?, ?
        )
        """, (
            name,
            path,
            language,
            modified
        ))

        self.connection.commit()

    def get_files(self):

        self.cursor.execute("""
        SELECT
            name,
            extension,
            path,
            modified
        FROM files
        ORDER BY name
        """)

        return self.cursor.fetchall()

    def get_projects(self):

        self.cursor.execute("""
        SELECT
            name,
            path,
            language,
            last_modified
        FROM projects
        ORDER BY name
        """)

        return self.cursor.fetchall()

    def clear_files(self):

        self.cursor.execute("DELETE FROM files")
        self.connection.commit()

    def clear_projects(self):

        self.cursor.execute("DELETE FROM projects")
        self.connection.commit()

    def close(self):

        self.connection.close()