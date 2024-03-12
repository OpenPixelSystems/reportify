# SPDX-License-Identifier: MIT

'''
@File     :  builder_factory.py
@Desc     :  Builder factory, to create the correct builder based on the report mode
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  24/12/2023
@Version  :  1.0
'''

from internal.builder import Builder
from internal.collector import Asset
from internal.dynamic.dynamic_builder import DynamicBuilder
from internal.logger import Logger
from internal.static.static_builder import StaticBuilder
from internal.internal_types import ReportMode


class BuilderFactory:
    class Error(Exception):
        def __init__(self):
            super().__init__("Unknown report mode")

    @staticmethod
    def create(mode: ReportMode, styles: list[Asset], scripts: list[Asset], logger: Logger) -> Builder:
        if mode == ReportMode.STATIC:
            return StaticBuilder(styles, scripts, logger)
        elif mode == ReportMode.DYNAMIC:
            return DynamicBuilder(styles, scripts, logger)

        raise BuilderFactory.Error()
