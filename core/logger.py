import datetime


class Logger:

    @staticmethod
    def log(skill_name, result):

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] {skill_name}")

        print(result)