from app.configs.config import CONFIG_LOGGER_ENABLED


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    """
    Logger class to handle logging of failures during validation checks.
    logs follow the format:
    [
        {
            provider: from which the log is coming,
            error: error message
            span: span where the error occurred (optional)
        }
    ]
    """

    logs = []

    @classmethod
    def add_fail(cls, provider, error , span=None , page=-1):
        message = {
            'provider': provider,
            'error': error,
            'span':span,
            'page' : page
        }
        cls.logs.append(message)

    @classmethod
    def get_logs(cls):
        return cls.logs

    @classmethod
    def clear_logs(cls):
        cls.logs = []


def logger():
    return Logger

log_enabled = CONFIG_LOGGER_ENABLED

def printwarn(provider,content):
    if not log_enabled:
        return
    print(bcolors.WARNING + "[" + provider + "] "+ bcolors.ENDC + content)

def printinfo(provider,content):
    if not log_enabled:
        return
    print(bcolors.OKBLUE + "[" + provider + "] "+ bcolors.ENDC + content)

def printsuccess(provider,content):
    if not log_enabled:
        return
    print(bcolors.OKGREEN + "[" + provider + "] "+ bcolors.ENDC + content)

def printfail(provider,content):
    if not log_enabled:
        return
    print(bcolors.FAIL + "[" + provider + "] "+ bcolors.ENDC + content)

def errorlogger(provider, error, span=None):
    Logger.add_fail(provider, error, span)
    print(bcolors.FAIL + "[" + provider + "] " + bcolors.ENDC + error)
    if span:
        print(bcolors.FAIL + "Span: " + str(span) + bcolors.ENDC)
