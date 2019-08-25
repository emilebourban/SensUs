#!/usr/bin/env python3

from application import Application
import log_setup

# set to False if the app should never exit even if interupted or crashed
CAN_EXIT = True


def is_raspi():
    try:
        from socket import gethostname
        if 'raspi' in gethostname():
            return True
    except BaseException:
        return False


def main(log):
    app = Application(is_raspi=is_raspi(), debug=True)
    try:
        rtn_msg = app.run()
        if rtn_msg:
            log.debug(f'Quitting: app returned {rtn_msg}')
            return True
    except BaseException as e:
        if type(e) is KeyboardInterrupt and CAN_EXIT:
            log.debug('Quitting: KeyboardInterrupt')
            return True
        log.exception(f'app crashed: {e}')


if __name__ == '__main__':
    # If the log seems to crash use: log = log_setup.init(safe_mode=True))
    log = log_setup.init()
    while not main(log):
        pass
