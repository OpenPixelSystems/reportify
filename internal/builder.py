'''
@File     :  builder.py
@Desc     :  Builder class, to generate HTML content for the reports
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/11/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

from typing import Any

from internal.collector import Asset
from internal.logger import Logger
from internal.parser import Tests


class Element:
    name: str
    value: str
    args = dict[str, str]
    elements: []  # type: ignore

    def __init__(self, name: str, value: str = '', args: dict = {}) -> None:
        self.name = name
        self.value = value
        self.args = args  # type: ignore
        self.elements = []

    def add(self, element: Any) -> None:
        self.elements.append(element)

    def get(self) -> []:  # type: ignore
        return self.elements


class Builder:
    class Error(Exception):
        def __init__(self):
            super().__init__("Method is abstract")

    class Data:
        tests: Tests
        test_data: str

        def __init__(self, tests: Tests, test_data: str) -> None:
            self.tests = tests
            self.test_data = test_data

    styles: list[Asset]
    scripts: list[Asset]
    logger: Logger

    def __init__(self, styles: list[Asset], scripts: list[Asset], logger: Logger) -> None:
        self.styles = styles
        self.scripts = scripts
        self.logger = logger

    def build(self, title: str, data: Data) -> str:
        raise Builder.Error()  # Abstract method

    def _build(self, element: Element) -> str:
        content = f'<{element.name}'

        for arg in element.args:  # type: ignore
            content += f' {arg}="{element.args[arg]}"'  # type: ignore

        if element.value == '':
            if len(element.elements) == 0:
                content += '/>\n'
                return content

            content += '>\n'

            for e in element.elements:
                content += self._build(e)
        else:
            content += f'>{element.value}'

        content += f'</{element.name}>\n'

        return content
