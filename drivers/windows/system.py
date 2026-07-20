import os
import subprocess
from pathlib import Path

from core.result import Result


class WindowsSystem:

    @staticmethod
    def open_app(app: str):

        aliases = {
            "vscode": "code",
            "vs code": "code",
            "visual studio code": "code",
            "chrome": "chrome",
            "google chrome": "chrome",
            "edge": "msedge",
            "notepad": "notepad",
            "cmd": "cmd",
            "powershell": "powershell",
            "explorer": "explorer"
        }

        executable = aliases.get(app.lower(), app)

        try:

            subprocess.Popen(executable)

            return Result(
                success=True,
                message=f"{app} launched successfully.",
                data={
                    "application": executable
                }
            )

        except Exception as e:

            return Result(
                success=False,
                message=str(e)
            )

    @staticmethod
    def open_folder(path: str):

        try:

            path = str(Path(path).resolve())

            if not os.path.exists(path):

                return Result(
                    success=False,
                    message="Folder does not exist."
                )

            os.startfile(path)

            return Result(
                success=True,
                message="Folder opened.",
                data={
                    "path": path
                }
            )

        except Exception as e:

            return Result(
                success=False,
                message=str(e)
            )

    @staticmethod
    def open_file(path: str):

        try:

            path = str(Path(path).resolve())

            if not os.path.exists(path):

                return Result(
                    success=False,
                    message="File does not exist."
                )

            os.startfile(path)

            return Result(
                success=True,
                message="File opened.",
                data={
                    "path": path
                }
            )

        except Exception as e:

            return Result(
                success=False,
                message=str(e)
            )