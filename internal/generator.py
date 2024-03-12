# SPDX-License-Identifier: MIT

'''
@File     :  generator.py
@Desc     :  Generator class, to write the HTML report to disk
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/11/2023
@Version  :  1.0
'''

import json

from internal.collector import Asset
from internal.logger import Logger
from internal.parser import Tests


class Generator:
    class Error(Exception):
        def __init__(self):
            super().__init__("Method is abstract")

    styles: list[Asset]
    scripts: list[Asset]
    logger: Logger

    def __init__(self, styles: list[Asset], scripts: list[Asset], logger: Logger) -> None:
        self.styles = styles
        self.scripts = scripts
        self.logger = logger

    def test_data(self, tests: Tests) -> str:
        data = {}

        for test in tests.tests.values():
            executions = {}

            for execution in test.executions:
                steps = {}

                for step in execution.steps:
                    steps[step.id] = {
                        'description': step.description,
                        'outcome': step.outcome
                    }

                executions[execution.id] = {
                    'device': execution.device,
                    'outcome': execution.outcome,
                    'duration': execution.duration,
                    'steps': steps
                }

            data[test.name] = {
                'node_id': test.node_id,
                'name': test.name,
                'description': test.description,
                'self_test': test.self_test,
                'executions': executions
            }

        tests = {}  # type: ignore
        tests['tests'] = data  # type: ignore

        return json.dumps(tests, indent=4)

    def report(self, html: str, file_path: str) -> bool:
        raise Generator.Error()  # Abstract method

    def _write_report(self, html: str, file_path: str) -> bool:
        try:
            output = open(file_path, 'w')
            output.write(html)
            output.close()
        except IOError as e:
            self.logger.error(f'failed to write report to disk: {e}')
            return False

        return True
