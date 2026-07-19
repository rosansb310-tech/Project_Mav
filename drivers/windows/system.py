import subprocess

from core.result import Result


class WindowsSystem:

    @staticmethod
    def open_app(app: str):

        try:

            subprocess.Popen(app)

            return Result(
                success=True,
                message=f"{app} launched successfully.",
                data={
                    "application": app
                }
            )

        except Exception as e:

            return Result(
                success=False,
                message=str(e)
            )