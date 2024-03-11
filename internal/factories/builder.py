'''
@File     :  builder.py
@Desc     :  Builder factory, to create the correct builder based on the report mode
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  24/12/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

from internal.builder import Builder
from internal.collector import Asset
from internal.dynamic.builder import DynamicBuilder
from internal.logger import Logger
from internal.static.builder import StaticBuilder
from internal.types import ReportMode


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
