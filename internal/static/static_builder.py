# SPDX-License-Identifier: MIT

'''
@File     :  static_builder.py
@Desc     :  Static builder class, to generate HTML content for the static reports
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  24/12/2023
@Version  :  1.0
'''

from internal.builder import Element, Builder
from internal.parser import Tests, Test, Execution


class StaticBuilder(Builder):
    def build(self, title: str, data: Builder.Data) -> str:
        html = Element('html')
        head = self._head(title)
        body = self._body(title, data.tests)

        html.add(head)
        html.add(body)

        return self._build(html)

    def _head(self, title: str) -> Element:
        head = Element('head')

        head.add(Element('title', title))
        head.add(Element('link', '',
                         {'rel': 'stylesheet',
                          'href': 'https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap'
                          }))

        head.add(self._style())

        return head

    def _style(self) -> Element:
        styles: list[str] = []

        for style in self.styles:
            try:
                with open(style.source, 'r') as file:
                    styles.append(f'\n{file.read()}\n')
            except IOError as e:
                self.logger.warning(f'style file {style.source} not found: {e}')

        return Element('style', '\n'.join(styles), {'type': 'text/css'})

    def _body(self, title: str, tests: Tests) -> Element:
        body = Element('body')

        body.add(self._title(title))
        body.add(self._overview(tests.tests))

        for test in tests.tests.values():
            body.add(self._individual_test(test))

        return body

    # Title

    def _title(self, title: str) -> Element:
        return Element('h1', title)

    # Overview

    def _overview(self, tests: dict[str, Test]) -> Element:
        div = Element('div', '')

        div.add(Element('h2', 'Test overview'))
        div.add(self._overview_action_bar(tests))
        div.add(self._overview_table_container(tests))

        return div

    def _overview_action_bar(self, tests: dict[str, Test]) -> Element:
        div = Element('div', '', {'class': 'action-bar'})

        passed = 0
        failed = 0
        skipped = 0

        for _, test in tests.items():
            outcome = test.get_outcome()

            if outcome == 'passed':
                passed += 1
            elif outcome == 'failed':
                failed += 1
            elif outcome == 'skipped':
                skipped += 1
            else:
                self.logger.warning(f'unknown outcome for test: {test.name}')

        total_tag = 'tests'

        if len(tests) == 1:
            total_tag = 'test'

        summary = Element('span', '', {'class': 'summary'})

        summary.add(Element('span', f'{len(tests)} {total_tag}', {'class': 'tile total active'}))

        if passed > 0:
            summary.add(Element('span', f'{passed} passed', {'class': 'tile passed active'}))

        if failed > 0:
            summary.add(Element('span', f'{failed} failed', {'class': 'tile failed active'}))

        if skipped > 0:
            summary.add(Element('span', f'{skipped} skipped', {'class': 'tile skipped active'}))

        div.add(summary)

        return div

    def _overview_table_container(self, tests: dict[str, Test]) -> Element:
        div = Element('div', '', {'class': 'individual-test-execution-table-container'})

        if len(tests) > 0:
            table = Element('table', '', {'class': 'test-table'})

            thead = Element('thead', '')

            thead_tr = Element('tr', '')

            thead_tr.add(Element('th', 'ID'))
            thead_tr.add(Element('th', 'Status'))
            thead_tr.add(Element('th', 'Device', {'width': '50%'}))
            thead_tr.add(Element('th', 'Name', {'width': '50%'}))
            thead_tr.add(Element('th', 'Duration'))
            thead_tr.add(Element('th', 'Executions'))

            thead.add(thead_tr)

            tbody = Element('tbody', '')

            for test in tests.values():
                execution_count = len(test.executions)

                for execution in test.executions:
                    execution_outcome_class = {'class': f'{execution.outcome}'}
                    tr_classes = ''

                    if test.has_same_outcome():
                        tr_classes += f' {test.get_outcome()}'
                    else:
                        tr_classes += ' mixed'

                    if execution_count > 1 and execution.id != len(test.executions) - 1:
                        tr_classes += ' no-border'

                    tbody_tr = Element('tr', '', {'class': tr_classes})

                    if execution.id == 0:
                        rowspan = {'rowspan': f'{execution_count}'}

                        tbody_tr.add(Element('td', str(test.id), rowspan))
                        tbody_tr.add(Element('td', execution.outcome, execution_outcome_class))
                        tbody_tr.add(Element('td', execution.device, execution_outcome_class))
                        tbody_tr.add(Element('td', test.name, rowspan))
                        tbody_tr.add(Element('td', f'{execution.duration:.2f}s', execution_outcome_class))
                        tbody_tr.add(Element('td', str(len(test.executions)), {'align': 'center'} | rowspan))
                    else:
                        tbody_tr.add(Element('td', execution.outcome, execution_outcome_class))
                        tbody_tr.add(Element('td', execution.device, execution_outcome_class))
                        tbody_tr.add(Element('td', f'{execution.duration:.2f}s', execution_outcome_class))

                    tbody.add(tbody_tr)

            table.add(thead)
            table.add(tbody)

            div.add(table)
        else:
            div.add(self._overview_table_placeholder_no_tests())

        return div

    def _overview_table_placeholder_no_tests(self) -> Element:
        return Element('div', 'No tests found', {'class': 'no-tests'})

    # Individual tests

    def _individual_test(self, test: Test) -> Element:
        div = Element('div', '', {'class': 'individual-test'})

        div.add(Element('h2', f'Test: {test.name}'))
        div.add(self._individual_test_description(test))
        div.add(self._individual_test_ran_on(test))
        div.add(self._individual_test_executions(test))

        return div

    def _individual_test_description(self, test: Test) -> Element:
        div = Element('div', '', {'class': 'test-description'})

        div.add(Element('h3', 'Test description:'))
        div.add(Element('p', test.description.replace('\n', '', 1).replace('\n', '<br/>\n') + '<br/>'))

        return div

    def _individual_test_ran_on(self, test: Test) -> Element:
        div = Element('div', '', {'class': 'ran-on'})

        div.add(Element('span', 'ran on:', {'class': 'ran-on'}))

        if len(test.executions) >= 1:
            div.add(self._individual_test_devices(test))
        elif len(test.executions) < 1:
            self.logger.warning(f'no executions found for test: {test.name}')
            return div

        return div

    def _individual_test_devices(self, test: Test) -> Element:
        span = Element('span', '', {'class': 'devices'})

        devices: list[str] = []

        for execution in test.executions:
            devices.append(execution.device)

        span.add(Element('span', ', '.join(devices)))

        return span

    def _individual_test_executions(self, test: Test) -> Element:
        div = Element('div', '', {'class': 'individual-test-executions'})

        for execution in test.executions:
            classes = 'individual-test-execution'

            div_execution = Element('div', '', {'class': classes})

            div_execution.add(Element('h3', f'Device: {execution.device}'))
            div_execution.add(self._individual_test_action_bar(test, execution))
            div_execution.add(self._individual_test_table_container(test, execution))

            div.add(div_execution)

        return div

    def _individual_test_action_bar(self, test: Test, execution: Execution) -> Element:
        div = Element('div', '', {'class': 'action-bar'})

        passed = 0
        failed = 0
        skipped = 0

        for step in execution.steps:
            if step.outcome == 'passed':
                passed += 1
            elif step.outcome == 'failed':
                failed += 1
            elif step.outcome == 'skipped':
                skipped += 1

        total_tag = 'steps'

        if len(test.executions[0].steps) == 1:
            total_tag = 'step'

        summary = Element('span', '', {'class': 'summary'})

        summary.add(Element('span', f'{len(test.executions[0].steps)} {total_tag}', {'class': 'tile total active'}))

        if passed > 0:
            summary.add(Element('span', f'{passed} passed', {'class': 'tile passed active'}))
        if failed > 0:
            summary.add(Element('span', f'{failed} failed', {'class': 'tile failed active'}))
        if skipped > 0:
            summary.add(Element('span', f'{skipped} skipped', {'class': 'tile skipped active'}))

        div.add(summary)

        return div

    def _individual_test_table_container(self, test: Test, execution: Execution) -> Element:
        div = Element('div', '', {'class': 'individual-test-execution-table-container'})

        if len(execution.steps) > 0:
            table = Element('table', '', {'class': 'test-table individual-test-table'})
            thead = Element('thead', '')

            thead_tr = Element('tr', '')

            thead_tr.add(Element('th', 'Step'))
            thead_tr.add(Element('th', 'Description', {'width': '100%'}))
            thead_tr.add(Element('th', 'Status'))

            thead.add(thead_tr)

            tbody = Element('tbody', '')

            i = 1

            for step in execution.steps:
                tbody_tr = Element('tr', '', {'class': f'{step.outcome}'})
                tbody_tr.add(Element('td', f'{i}/{len(execution.steps)}'))
                tbody_tr.add(Element('td', step.description))
                tbody_tr.add(Element('td', step.outcome))
                tbody.add(tbody_tr)

                i += 1

            tfoot = Element('tfoot', '', {'class': execution.outcome})

            tfoot_tr = Element('tr', '')

            footer = f'Test on {execution.device} {execution.outcome} in {execution.duration:.2f}s'
            tfoot_tr.add(Element('td', footer, {'colspan': '3'}))

            tfoot.add(tfoot_tr)

            table.add(thead)
            table.add(tbody)
            table.add(tfoot)

            div.add(table)
        else:
            div.add(self._individual_test_table_placeholder_no_steps(test))

        return div

    def _individual_test_table_placeholder_no_steps(self, test: Test) -> Element:
        return Element('div', 'No individual steps found', {'class': 'no-steps'})
