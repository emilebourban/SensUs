#!/usr/bin/env python3

import log_setup


def is_raspi():
    try:
        from socket import gethostname
        if 'raspi' in gethostname():
            return True
    except BaseException:
        return False


def main(log):
    try:
        from application import Application
        app = Application(is_raspi=is_raspi(), debug=False)
        rtn_msg = app.run()
        if rtn_msg:
            log.debug(f'Quitting: app returned {rtn_msg}')
            return True
    except KeyboardInterrupt:
            log.debug('Quitting: KeyboardInterrupt')
            return True
    except BaseException as e:
            log.exception(f'app crashed: {e}')


if __name__ == '__main__':
    # If the log seems to crash use: log = log_setup.init(safe_mode=True))
    log = log_setup.init()
    while not main(log):
        pass
