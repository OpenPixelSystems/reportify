# SPDX-License-Identifier: MIT

'''
@File     :  generator_factory.py
@Desc     :  Generator factory, to create the correct generator based on the report mode
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  25/12/2023
@Version  :  1.0
'''

from internal.collector import Asset
from internal.dynamic.dynamic_generator import DynamicGenerator
from internal.generator import Generator
from internal.logger import Logger
from internal.static.static_generator import StaticGenerator

from internal.internal_types import ReportMode


class GeneratorFactory:
    class Error(Exception):
        def __init__(self):
            super().__init__("Unknown report mode")

    @staticmethod
    def create(mode: ReportMode, styles: list[Asset], scripts: list[Asset], logger: Logger) -> Generator:
        if mode == ReportMode.STATIC:
            return StaticGenerator(styles, scripts, logger)
        elif mode == ReportMode.DYNAMIC:
            return DynamicGenerator(styles, scripts, logger)

        raise GeneratorFactory.Error()
