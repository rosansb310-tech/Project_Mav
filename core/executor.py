import time

from core.logger import Logger


class Executor:

    def execute(self, skill, **kwargs):

        start = time.time()

        result = skill.execute(**kwargs)

        duration = round(time.time() - start, 4)

        Logger.log(skill.name, result)

        print(f"Execution Time: {duration}s")

        return result