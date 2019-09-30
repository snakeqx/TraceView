from loghelper import LogHelper
from tracehelper.tracehelper import Trace
from matplotlib import pyplot as plt


if __name__ == '__main__':
    # Initial log
    LOG = LogHelper.AppLog().LOGGER
    LOG.debug("init successful")
    trace = Trace([r'./test_data/a.log', r'./test_data/b.log', r'./test_data/c.log'])
    # trace = Trace([r'./test_data/c.log'])

    ###############################
    # develop
    _select = 'actimas/dmc'

    list = trace.normalize_controller_log_dict(_select, suggestion=True)
    plt.plot(list)
    plt.show()