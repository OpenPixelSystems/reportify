# SPDX-License-Identifier: MIT

'''
@File     :  logger.py
@Desc     :  Logger class, to manage which messages are logged to the console
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/11/2023
@Version  :  1.0
'''


class Logger:
    verbose: bool

    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose

    def debug(self, message: str) -> None:
        if self.verbose:
            print(message)

    def info(self, message: str) -> None:
        print(message)

    def success(self, message: str) -> None:
        print(self._green(f'{message}'))

    def warning(self, message: str) -> None:
        print(self._yellow(f'warning: {message}'))

    def error(self, message: str) -> None:
        print(self._red(f'error: {message}'))

    def _green(self, message: str) -> str:
        return f'\033[92m{message}\033[0m'

    def _yellow(self, message: str) -> str:
        return f'\033[93m{message}\033[0m'

    def _red(self, message: str) -> str:
        return f'\033[91m{message}\033[0m'
