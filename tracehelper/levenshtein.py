import numpy as np
from loghelper.LogHelper import AppLog

LOG = AppLog().LOGGER


class Levenshtein:
    @staticmethod
    def distance(str1: str, str2: str):
        dp = np.zeros((len(str1) + 1, len(str2) + 1))

        for i in range(len(str1) + 1):
            dp[i][0] = i
        for j in range(len(str2) + 1):
            dp[0][j] = j

        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i - 1][j - 1], min(dp[i][j - 1], dp[i - 1][j])) + 1
        return dp[len(str1)][len(str2)]

    @staticmethod
    def similarity(str1: str, str2: str):
        __distance = Levenshtein.distance(str1, str2)
        __max_len = len(str1) if len(str1) >= len(str2) else len(str2)
        __similarity = 1 - __distance / __max_len
        return __similarity

    @staticmethod
    def result(str1: str, str2: str):
        __distance = Levenshtein.distance(str1, str2)
        __max_len = len(str1) if len(str1) >= len(str2) else len(str2)
        __similarity = 1 - __distance / __max_len
        return __distance, __similarity
