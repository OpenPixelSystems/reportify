'''
@File     :  generator.py
@Desc     :  Static generator class, to write the static HTML report to disk
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  25/12/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

import os

from internal.generator import Generator


class StaticGenerator(Generator):
    def report(self, html: str, output_folder: str) -> bool:
        file_path = os.path.join(output_folder, 'report.html')
        return self._write_report(html, file_path)
