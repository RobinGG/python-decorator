import signal

import time


class TimeoutError(Exception):
    def __init__(self, func_name):
        self.func_name = func_name

    def __str__(self):
        return repr(self.func_name)


def timeout(seconds_before_timeout):
    """Time out decorator from https://stackoverflow.com/a/35491756"""

    def decorate(f):
        def handler(signum, frame):
            raise TimeoutError(f.__name__)

        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            old_time_left = signal.alarm(seconds_before_timeout)
            if 0 < old_time_left < seconds_before_timeout:  # never lengthen existing timer
                signal.alarm(old_time_left)
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
            finally:
                if old_time_left > 0:  # deduct f's run time from the saved timer
                    old_time_left -= time.time() - start_time
                signal.signal(signal.SIGALRM, old)
                signal.alarm(old_time_left)
            return result

        new_f.func_name = f.func_name
        return new_f

    return decorate
