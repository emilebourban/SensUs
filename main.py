#!/usr/bin/env python3

from application import Application
import log_setup
import logging

# set to False if the app should never exit even if interupted or crashed
CAN_EXIT = True


def main(log):
    app = Application()
    try:
        return app.run()
    except BaseException as e:
        if type(e) is KeyboardInterrupt and CAN_EXIT:
            return True
        log.exception(f'app crashed: {e}')


if __name__ == '__main__':
    # If the log seems to crash use: log = log_setup.init(safe_mode=True))
    log = log_setup.init()
    while not main(log):
        pass
