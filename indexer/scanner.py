from pathlib import Path
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
        ".mypy_cache"
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
        ".sqlite3"
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
        print(f"Skipped Files : {self.files_skipped}")
        print(f"Projects Found: {self.projects_found}")
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

        if self._is_project(folder):
            self.projects_found += 1

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
                modified=stat.st_mtime
            )

            self.files_indexed += 1

        except Exception:

            self.files_skipped += 1

    def _is_project(self, folder: Path):

        project_markers = [
            ".git",
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "Cargo.toml",
            "pom.xml",
            "CMakeLists.txt",
            ".sln"
        ]

        for marker in project_markers:

            if (folder / marker).exists():

                return True

        return False