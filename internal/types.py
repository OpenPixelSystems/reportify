'''
@File     :  types.py
@Desc     :  Files with custom types
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/12/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

from enum import Enum


class ReportMode(Enum):
    STATIC = 0
    DYNAMIC = 1
