from loghelper import LogHelper
import numpy as np
from ctypes import *
# if c cypes do not work, use python version. But slower 1000 times
# from tracehelper.levenshtein import Levenshtein as lvst


LOG = LogHelper.AppLog().LOGGER


class Trace:

    def __init__(self, file_name: list):
        LOG.debug("start construction of Trace class")
        # define class attr
        LOG.debug('input parameter type is:' + str(type(file_name)))
        self.FileNames = file_name
        self.TraceLogList = []
        self.LogControllerDict = {}
        self.NormControllerLogDict = {}

        # define private attr
        self._dllObj = CDLL('./tracehelper/levenshtein.dll')
        self._dllObj.similarity.argtypes = (c_char_p, c_char_p)
        self._dllObj.similarity.restype = c_float
        self._similarity = self._dllObj.similarity

        # logic
        self.read_files()

    def read_files(self):
        """
        Read all files in the self.FileName list and parse each line to have a tuple stored in self.TraceLogList[]
        The tuple structure is (log_time: str, controller: str, code: str, log_msg: str)
        :return: NA
        """
        for each_file in self.FileNames:
            with open(each_file, mode='r') as current_file:
                for line in current_file:
                    self._parse_line(line, each_file)
        self._init_controller_dict()

    def normalize_controller_log_dict(self, controller_name: str, similarity: float = 0.7, suggestion: bool = False):
        _checked_name = self._check_controller_name(controller_name, suggestion)
        if _checked_name is None:
            LOG.error("controller name not found")
            return

        # logic
        _id = 0
        _result = []
        _log_list = []
        _compare_len = 30
        for index, log in enumerate(self.LogControllerDict[_checked_name]):
            print('\r {0}/{1}'.format(index, len(self.LogControllerDict[_checked_name])), end='')
            # handle the 1st log
            if len(_log_list) == 0:
                _log_list.append(log)
                _result.append(_id)
                _id += 1
                continue
            # handle the rest
            dp = np.zeros(len(_log_list))
            for index2, comp in enumerate(_log_list):
                # dp[index2] = lvst.similarity(comp[:_compare_len], log[:_compare_len])
                dp[index2] = self._similarity(comp[:_compare_len].encode('ascii'), log[:_compare_len].encode('ascii'))
            if np.max(dp) < similarity:
                # LOG.debug('compare id:\t{0}\t{1}...'
                # .format(_id, log[:_compare_len] if len(log) > _compare_len else log))
                _log_list.append(log)
                _result.append(_id)
                _id += 1
            else:
                # LOG.debug('compare id:\t{0}\t{1}...'
                # .format(np.argmax(dp), log[:_compare_len] if len(log) > _compare_len else log))
                _result.append(np.argmax(dp))
        return _result

    def _init_controller_dict(self):
        _time = 0
        _controller = 1
        _code = 2
        _msg = 3
        for index, log in enumerate(self.TraceLogList):
            print('\r processing controller dictionary init: {0}/{1}'.format(index+1, len(self.TraceLogList)), end='')
            if log[_controller] not in self.LogControllerDict:
                self.LogControllerDict[log[_controller]] = [log[_msg]]
            else:
                self.LogControllerDict[log[_controller]].append(log[_msg])
        print('\n controller dictionary init done\n')

    def _check_controller_name(self, controller_name: str, suggestion: bool):
        if controller_name in self.LogControllerDict.keys():
            return controller_name

        if suggestion:
            dp = np.zeros(len(self.LogControllerDict))
            for index, name in enumerate(self.LogControllerDict):
                # dp[index] = lvst.similarity(controller_name.upper(), name.upper())
                dp[index] = self._similarity(controller_name.upper().encode('ascii'),
                                             name.upper().encode('ascii'))
                LOG.debug("compare to strings: {0} vs {1} \t\t\t\t=> Similarity={2}"
                          .format(controller_name.upper(), name.upper(), dp[index]))
            _max_index = int(np.argmax(dp))
            LOG.debug("max index = {0}, type={1}".format(_max_index, type(_max_index)))
            LOG.debug('all controller names listed here: {0}'.format(self.LogControllerDict.keys()))
            _result_name = list(self.LogControllerDict.keys())[_max_index]
            LOG.warning("no controller named \"{0}\". do you mean \"{1}\""
                        .format(controller_name, _result_name))
            return _result_name
        else:
            return None

    def _parse_line(self, line: str, file_name: str):
        time = line[:35]
        splits = line[35:].split(':', maxsplit=2)
        spl_length = len(splits)
        if spl_length == 3:
            self.TraceLogList.append((time, splits[0].replace(' ', ''), splits[1], splits[2]))
        elif spl_length == 2:
            self.TraceLogList.append((time, splits[0].replace(' ', ''), splits[1], splits[1]))
            LOG.warning("Split line with only 2 parts in file " + file_name)
            LOG.warning('. Parsed as' + str(self.TraceLogList[-1]))
        elif spl_length == 1:
            self.TraceLogList.append((time, splits[0].replace(' ', ''), splits[0], splits[0]))
            LOG.warning("Split line with only 1 part in file " + file_name)
            LOG.warning('. Parsed as' + str(self.TraceLogList[-1]))


if __name__ == '__main__':
    LOG.warning("Please do call this script separately unless for testing")
