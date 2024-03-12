# SPDX-License-Identifier: MIT

'''
@File     :  internal_types.py
@Desc     :  Files with custom types
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/12/2023
@Version  :  1.0
'''

from enum import Enum


class ReportMode(Enum):
    STATIC = 0
    DYNAMIC = 1
