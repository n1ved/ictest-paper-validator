from app.configs.config import CONFIG_LOGGER_ENABLED
from app.utils.span_finder import find_span_location


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

class LogLevel:
    DEBUG = 1
    INFO = 2

# Default log level
current_log_level = LogLevel.DEBUG

def set_log_level(level):
    global current_log_level
    current_log_level = level

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
    error_spans = []
    formatted_text = None

    @classmethod
    def set_formatted_text(cls, formatted_text):
        cls.formatted_text = formatted_text

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
    def add_log(cls, provider, message, msg_type='INFO', data=None):
        """Add a generic log message (non-error)."""
        log_entry = {
            'provider': provider,
            'error': message, # Reusing 'error' field for compatibility with report generator
            'msg_type': msg_type,
            'data': data,
            'span': None,
            'page': -1
        }
        cls.logs.append(log_entry)

    @classmethod
    def get_logs(cls):
        return cls.logs

    @classmethod
    def clear_logs(cls):
        cls.error_spans = []
        cls.logs = []

    @classmethod
    def set_error_span(cls, span):
        span_check_res = find_span_location(cls.formatted_text,span)
        for spans in span_check_res:
                cls.error_spans.append(spans)

    @classmethod
    def get_error_spans(cls):
        return cls.error_spans



def logger():
    return Logger

log_enabled = CONFIG_LOGGER_ENABLED

def printwarn(provider,content):
    if not log_enabled or current_log_level > LogLevel.INFO:
        return
    print(bcolors.WARNING + "[" + provider + "] "+ bcolors.ENDC + content)

def printinfo(provider,content):
    if not log_enabled or current_log_level > LogLevel.DEBUG:
        return
    print(bcolors.OKBLUE + "[" + provider + "] "+ bcolors.ENDC + content)

def printsuccess(provider,content):
    if not log_enabled or current_log_level > LogLevel.INFO:
        return
    print(bcolors.OKGREEN + "[" + provider + "] "+ bcolors.ENDC + content)

def printfail(provider,content):
    if not log_enabled or current_log_level > LogLevel.INFO:
        return
    print(bcolors.FAIL + "[" + provider + "] "+ bcolors.ENDC + content)

def errorlogger(provider, error, span=None):
    t_spans = []
    if isinstance(span, list):
        t_spans = span
    else:
        t_spans.append(span)
    Logger.add_fail(provider, error, t_spans)
    Logger.set_error_span(t_spans)
    
    if log_enabled and current_log_level <= LogLevel.INFO:
        print(bcolors.FAIL + "[" + provider + "] " + bcolors.ENDC + error)
        if span:
            print(bcolors.FAIL + "Span: " + str(span) + bcolors.ENDC)


def infologger(provider, message, msg_type='INFO', data=None):
    """Logs info to both stdout (if enabled) and Logger storage."""
    Logger.add_log(provider, message, msg_type=msg_type, data=data)
    printinfo(provider, message)

