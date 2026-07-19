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
            print(f"Path      : {project['path']}")
            print(f"Modified  : {project['last_modified']}")
            print("-" * 60)

    def clear(self):

        self.database.clear_files()
        self.database.clear_projects()

        print("Database cleared.")