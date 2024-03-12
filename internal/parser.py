'''
@File     :  parser.py
@Desc     :  Parser class, to parse the test JSON files into objects
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/11/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

import json
import re

from internal.logger import Logger


class Step:
    id: int
    description: str
    outcome: str

    def __init__(self) -> None:
        self.id = 0
        self.description = ''
        self.outcome = ''


class Execution:
    id: int
    device: str
    outcome: str
    duration: float
    steps: list[Step]

    def __init__(self) -> None:
        self.id = 0
        self.device = ''
        self.outcome = ''
        self.duration = 0.0
        self.steps = []


class Test:
    id: int
    node_id: str
    name: str
    description: str
    self_test: bool
    executions: list[Execution]

    def __init__(self) -> None:
        self.id = 0
        self.name = ''
        self.node_id = ''
        self.description = ''
        self.self_test = False
        self.executions = []

    def get_devices(self) -> list[str]:
        devices: list[str] = []

        for execution in self.executions:
            if execution.device not in devices:
                devices.append(execution.device)

        return devices

    def get_outcome(self) -> str:
        outcomes: list[str] = []

        for execution in self.executions:
            outcomes.append(execution.outcome)

        if 'failed' in outcomes:
            return 'failed'
        elif 'passed' in outcomes:
            return 'passed'
        elif 'skipped' in outcomes:
            return 'skipped'

        return 'unknown'

    def has_same_outcome(self) -> bool:
        outcome = self.get_outcome()

        for execution in self.executions:
            if execution.outcome != outcome:
                return False

        return True

    def get_duration(self) -> float:
        duration = 0.0

        for execution in self.executions:
            duration += execution.duration

        return duration


class Tests:
    tests: dict[str, Test]

    def __init__(self) -> None:
        self.tests = {}

    def __str__(self):
        s = ''
        s = 'Tests:\n'

        i = 1

        for _, test in self.tests.items():
            description = test.description.replace('\n', '\\n').strip()

            if len(description) > 77:  # 80 - 3
                description = description[:77] + '...'

            s += '\n'
            s += f'- Test {test.id}:\n\n'
            s += f'  - Node ID      : {test.node_id}\n'
            s += f'  - Name         : {test.name}\n'
            s += f'  - Description  : {description}\n'
            s += f'  - Self test    : {test.self_test}\n'

            for execution in test.executions:
                s += '\n'
                s += f'  - Execution {execution.id}:\n\n'
                s += f'    - Device       : {execution.device}\n'
                s += f'    - Outcome      : {execution.outcome}\n'
                s += f'    - Duration     : {execution.duration}\n'

                if len(execution.steps) != 0:
                    s += '    - Steps: \n'

                    max_desc_length = 0
                    for step in execution.steps:
                        max_desc_length = max(max_desc_length, len(step.description))

                    for step in execution.steps:
                        desc_length = len(step.description)
                        s += f'      - {step.description}'

                        for _ in range(0, max_desc_length - desc_length):
                            s += ' '

                        s += f'      {step.outcome}\n'

            i += 1

        return s


class Parser:
    inputs: list[str]
    logger: Logger

    def __init__(self, input: str, include_self_tests: bool, logger: Logger) -> None:
        self.inputs = self._toList(input)
        self.include_self_tests = include_self_tests
        self.logger = logger

    def parse(self) -> Tests | None:
        all_tests = Tests()

        id = 0

        for input in self.inputs:
            try:
                with open(input, 'r') as file:
                    try:
                        json_data = json.load(file)
                    except json.JSONDecodeError as e:
                        self.logger.error(f'failed to parse input file: {e}')
                        return None
            except IOError as e:
                self.logger.error(f'failed to read input file: {e}')
                return None

            for test in json_data['tests']:
                tests, id = self._read_test(all_tests, test, id)
                if tests is None:
                    return None

                all_tests.tests = all_tests.tests | tests.tests

        self.logger.debug(all_tests)  # type: ignore

        return all_tests

    def _toList(self, files: str) -> list[str]:
        return files.split(',') if ',' in files else [files]

    def _read_test(self, tests: Tests, json_data: dict, id: int) -> [Tests, int]:  # type: ignore
        test = Test()

        test.id = id

        if not self._hasKey('metadata', json_data, test.node_id):
            self.logger.error(f'no metadata found for test: {test.node_id}')
            return None, -1

        test.name = self._readKey('active_test', json_data['metadata'], test.node_id)  # type: ignore
        if test.name is None:
            return None, -1

        test.node_id = self._readKey('nodeid', json_data)
        if test.node_id is None:
            return None, -1

        # Remove helper postfix from node id
        test.node_id = re.sub('\\[(.*)]', '', test.node_id)

        if test.name not in test.node_id:
            self.logger.error(f'name {test.name} not found in node id {test.node_id}')
            return None, -1

        test.description = self._readKey('description', json_data['metadata'], test.node_id)  # type: ignore
        if test.description is None:
            return None, -1

        if self._hasOptionalKey('self_test', json_data['metadata']):
            test.self_test = json_data['metadata']['self_test']

        # Skip self tests if not requested
        if test.self_test and not self.include_self_tests:
            return tests, id

        existing_test = self._get_test(test.name, tests)
        if existing_test is not None:
            if not self._verify_test(test, existing_test):
                return None, -1

            # Add the device to the existing test
            test = existing_test
        else:
            id += 1  # Only increment the id if the test is new

        execution = self._read_execution(json_data, len(test.executions), test.node_id)
        if execution is None:
            return None

        test.executions.append(execution)

        tests.tests[test.name] = test

        return tests, id

    def _read_execution(self, json_data: dict, id: int, node_id: str) -> Execution | None:
        execution = Execution()

        execution.id = id

        if not self._hasKey('call', json_data, node_id):
            self.logger.error(f'no call found for test: {node_id}')
            return None

        execution.device = self._readKey('device', json_data['metadata'], node_id)
        if execution.device is None:
            return None

        execution.outcome = self._readKey('outcome', json_data, node_id)
        if execution.outcome is None:
            return None

        execution.duration = self._readKey('duration', json_data['call'], node_id)  # type: ignore
        if execution.duration is None:
            return None

        steps = self._read_steps(json_data, node_id)
        if steps is None:
            return None

        execution.steps = steps

        return execution

    def _read_steps(self, json_data: dict, node_id: str) -> list[Step] | None:
        steps: list[Step] = []

        if not self._hasKey('steps', json_data['metadata'], node_id):
            self.logger.error(f'no steps found for test: {node_id}')
            return None

        step_count = int(json_data['metadata']['steps'])
        for step in range(0, step_count):
            step_key = f'step-{step}'

            if not self._hasKey(step_key, json_data['metadata'], node_id):
                self.logger.error(f'no {step_key} found for test: {node_id}')
                return None

            s = Step()

            s.id = len(steps)

            s.description = self._readKey('description', json_data['metadata'][step_key], node_id, step_key)
            if s.description is None:
                return None

            s.outcome = self._readKey('outcome', json_data['metadata'][step_key], node_id, step_key)
            if s.outcome is None:
                return None

            steps.append(s)

        return steps

    def _get_test(self, name: str, tests: Tests) -> Test | None:
        for key, value in tests.tests.items():
            if key == name:
                return value

        return None

    def _verify_test(self, test: Test, existing_test: Test) -> bool:
        if test.name != existing_test.name:
            self.logger.error(f'name mismatch for {test.name}: {test.name} != {existing_test.name}')
            return False

        if test.node_id != existing_test.node_id:
            self.logger.error(f'node id mismatch for {test.name}: {test.node_id} != {existing_test.node_id}')
            return False

        if test.description != existing_test.description:
            self.logger.error(
                f'description mismatch for {test.name}: {test.description} != {existing_test.description}')
            return False

        if test.self_test != existing_test.self_test:
            self.logger.error(f'self test mismatch for {test.name}: {test.self_test} != {existing_test.self_test}')
            return False

        return True

    def _readKey(self, key: str, data: dict, node_id: str = '', step_key: str = '') -> str:
        if not self._hasKey(key, data, node_id):
            return None  # type: ignore

        return data[key]

    def _hasKey(self, key: str, data: dict, node_id: str = '', step_key: str = '') -> bool:
        if key not in data:
            if node_id == '':
                self.logger.error(f'no {key} found for test')
            elif step_key == '':
                self.logger.error(f'no {key} found for test: {node_id}')
            else:
                self.logger.error(f'{key} not found for {step_key} in test: {node_id}')

            return False

        return True

    def _hasOptionalKey(self, key: str, data: dict) -> bool:
        return key in data
