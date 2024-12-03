import time

class Date:

    @staticmethod
    def timestring() -> str:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))