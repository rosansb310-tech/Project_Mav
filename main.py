from core.router import Router

from indexer.scanner import FileScanner
from indexer.database import FileDatabase


def main():

    router = Router()

    scanner = FileScanner()
    database = FileDatabase()

    print("=" * 40)
    print("           Mav Core")
    print("=" * 40)

    while True:

        command = input("\nMav > ").strip()

        if not command:
            continue

        cmd = command.lower()

        if cmd in ["exit", "quit"]:

            print("Goodbye.")
            break

        elif cmd == "scan":

            database.clear()
            scanner.scan(".")

        elif cmd == "files":

            database.show_files()

        elif cmd == "projects":

            database.show_projects()

        elif cmd == "clear":

            database.clear()

        else:

            router.route(command)


if __name__ == "__main__":
    main()