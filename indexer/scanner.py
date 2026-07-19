# indexer/scanner.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from database.database import Database


class FileScanner:
    # Folders to ignore completely
    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        "node_modules",
        "venv",
        ".venv",
        ".idea",
        ".vscode",
        "dist",
        "build",
        "bin",
        "obj",
        ".pytest_cache",
        ".mypy_cache",
        ".next",
        ".git",
    }

    # File extensions worth indexing
    INDEX_EXTENSIONS = {
        ".py",
        ".txt",
        ".md",
        ".pdf",
        ".doc",
        ".docx",
        ".ppt",
        ".pptx",
        ".xls",
        ".xlsx",
        ".json",
        ".yaml",
        ".yml",
        ".xml",
        ".csv",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".java",
        ".js",
        ".ts",
        ".tsx",
        ".html",
        ".css",
        ".sql",
        ".db",
        ".sqlite",
        ".sqlite3",
        ".rs",
        ".go",
        ".kt",
        ".swift",
        ".dart",
        ".sh",
        ".bat",
        ".ps1",
    }

    PROJECT_MARKERS = (
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "pom.xml",
        "CMakeLists.txt",
        "*.sln",
        "go.mod",
        "pubspec.yaml",
        "composer.json",
    )

    LANGUAGE_MAP = {
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "package.json": "JavaScript/TypeScript",
        "Cargo.toml": "Rust",
        "pom.xml": "Java",
        "CMakeLists.txt": "C/C++",
        "go.mod": "Go",
        "pubspec.yaml": "Dart",
        "composer.json": "PHP",
    }

    def __init__(self):
        self.database = Database()
        self.files_indexed = 0
        self.files_skipped = 0
        self.projects_found = 0

    def scan(self, root):
        root = Path(root)

        if not root.exists():
            print("Directory does not exist.")
            return

        self.files_indexed = 0
        self.files_skipped = 0
        self.projects_found = 0

        self._scan_directory(root)

        print()
        print("=" * 40)
        print("SCAN COMPLETE")
        print("=" * 40)
        print(f"Indexed Files : {self.files_indexed}")
        print(f"Skipped Files  : {self.files_skipped}")
        print(f"Projects Found : {self.projects_found}")
        print("=" * 40)

    def _scan_directory(self, folder: Path):
        if folder.name in self.IGNORE_DIRS:
            return

        if folder.name.startswith(".") and folder.name != ".":
            return

        try:
            items = list(folder.iterdir())
        except Exception:
            return

        project_info = self._detect_project(folder)
        if project_info is not None:
            self.projects_found += 1
            self.database.insert_project(
                name=project_info["name"],
                path=str(folder.resolve()),
                language=project_info["language"],
                modified=project_info["modified"],
                git_repo=project_info["git_repo"],
                entry_file=project_info["entry_file"],
                metadata=project_info["metadata"],
            )

        for item in items:
            if item.is_dir():
                self._scan_directory(item)
                continue

            self._index_file(item)

    def _index_file(self, file: Path):
        extension = file.suffix.lower()

        if extension not in self.INDEX_EXTENSIONS:
            self.files_skipped += 1
            return

        try:
            stat = file.stat()
            self.database.insert_file(
                name=file.stem,
                extension=extension,
                path=str(file.resolve()),
                modified=stat.st_mtime,
            )
            self.files_indexed += 1
        except Exception:
            self.files_skipped += 1

    def _detect_project(self, folder: Path) -> Optional[dict]:
        git_repo = (folder / ".git").exists()
        language = self._detect_language(folder)
        entry_file = self._detect_entry_file(folder)
        metadata = self._collect_metadata(folder)

        if not git_repo and language is None and entry_file is None and metadata is None:
            return None

        try:
            modified = folder.stat().st_mtime
        except Exception:
            modified = None

        return {
            "name": folder.name,
            "language": language or "Unknown",
            "git_repo": 1 if git_repo else 0,
            "entry_file": entry_file,
            "metadata": metadata,
            "modified": modified,
        }

    def _detect_language(self, folder: Path) -> Optional[str]:
        for marker, language in self.LANGUAGE_MAP.items():
            if (folder / marker).exists():
                return language

        extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript/React",
            ".jsx": "JavaScript/React",
            ".java": "Java",
            ".cpp": "C++",
            ".c": "C",
            ".cs": "C#",
            ".go": "Go",
            ".rs": "Rust",
            ".kt": "Kotlin",
            ".swift": "Swift",
            ".dart": "Dart",
            ".sh": "Shell",
            ".ps1": "PowerShell",
            ".html": "HTML",
            ".css": "CSS",
            ".sql": "SQL",
        }

        counts = {}
        try:
            for path in folder.rglob("*"):
                if path.is_file():
                    ext = path.suffix.lower()
                    if ext in extensions:
                        counts[ext] = counts.get(ext, 0) + 1
        except Exception:
            return None

        if not counts:
            return None

        ext = max(counts, key=counts.get)
        return extensions[ext]

    def _detect_entry_file(self, folder: Path) -> Optional[str]:
        candidates = [
            "main.py",
            "app.py",
            "index.js",
            "index.ts",
            "index.tsx",
            "main.js",
            "main.ts",
            "src/main.py",
            "src/index.js",
            "src/index.ts",
            "Program.cs",
            "main.cpp",
            "main.c",
            "src/main.cpp",
        ]

        for candidate in candidates:
            if (folder / candidate).exists():
                return candidate

        return None

    def _collect_metadata(self, folder: Path) -> Optional[str]:
        metadata = {}

        readme = None
        for name in ("README.md", "readme.md", "Readme.md"):
            if (folder / name).exists():
                readme = name
                break

        if readme:
            metadata["readme"] = readme

        deps = []
        for name in ("requirements.txt", "package.json", "pyproject.toml", "Cargo.toml", "go.mod"):
            if (folder / name).exists():
                deps.append(name)

        if deps:
            metadata["dependencies"] = deps

        if not metadata:
            return None

        return json.dumps(metadata, ensure_ascii=False)