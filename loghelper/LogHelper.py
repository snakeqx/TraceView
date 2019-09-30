import logging


# A decorator function to make a class as a singleton
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

# Singleton class
@singleton
class AppLog:
    """
    usage: a = AppLog() ==> a.LOGGER.error("msg")
    """

    def __init__(self):
        # public attr
        self.IsConsoleOutput = True
        self.IsLogFileOutput = True
        self.IsLogEnable = True
        self.LOGGER = logging.getLogger()
        # private attr
        self._log_formatter = logging.Formatter('%(asctime)s | %(filename)s | [line:%(lineno)d] | '
                                                '%(levelname)s | %(message)s')
        self._log_level = logging.DEBUG
        self._console_handler = logging.StreamHandler()
        self._file_handler = logging.FileHandler(r'./log.txt', mode='w')
        self._enable_handler()

    def _enable_handler(self):
        self.LOGGER.setLevel(self._log_level)
        if self.IsLogFileOutput is True:        
            self._file_handler.setLevel(self._log_level)
            self._file_handler.setFormatter(self._log_formatter)
            self.LOGGER.addHandler(self._file_handler)

        if self.IsConsoleOutput is True:        
            self._console_handler.setLevel(self._log_level)
            self._console_handler.setFormatter(self._log_formatter)
            self.LOGGER.addHandler(self._console_handler)

    def disable_log(self):
        self.IsLogEnable = False

    def enable_log(self):
        self.IsLogEnable = True
