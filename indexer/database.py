# indexer/database.py
from database.database import Database


class FileDatabase:
    def __init__(self):
        self.database = Database()

    def show_files(self):
        files = self.database.get_files()

        if not files:
            print("\nNo indexed files.\n")
            return

        print("\n========== FILE INDEX ==========\n")

        for file in files:
            print(f"Name      : {file['name']}")
            print(f"Extension : {file['extension']}")
            print(f"Path      : {file['path']}")
            print(f"Modified  : {file['modified']}")
            print("-" * 60)

    def show_projects(self):
        projects = self.database.get_projects()

        if not projects:
            print("\nNo projects detected.\n")
            return

        print("\n========= PROJECT INDEX =========\n")

        for project in projects:
            print(f"Project   : {project['name']}")
            print(f"Language  : {project['language']}")
            print(f"Git Repo  : {bool(project['git_repo'])}")
            print(f"Entry     : {project['entry_file']}")
            print(f"Path      : {project['path']}")
            print(f"Modified  : {project['last_modified']}")
            print("-" * 60)

    def show_apps(self):
        apps = self.database.get_apps()

        if not apps:
            print("\nNo indexed apps.\n")
            return

        print("\n========== APP INDEX ==========\n")

        for app in apps:
            print(f"Name      : {app['name']}")
            print(f"Path      : {app['path']}")
            print(f"Source    : {app['source']}")
            print(f"Favorite  : {bool(app['favorite'])}")
            print(f"Modified  : {app['modified']}")
            print("-" * 60)

    def clear(self):
        self.database.clear_all()
        print("Database cleared.")