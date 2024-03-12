# SPDX-License-Identifier: MIT

'''
@File     :  static_generator.py
@Desc     :  Static generator class, to write the static HTML report to disk
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  25/12/2023
@Version  :  1.0
'''

import os

from internal.generator import Generator


class StaticGenerator(Generator):
    def report(self, html: str, output_folder: str) -> bool:
        file_path = os.path.join(output_folder, 'report.html')
        return self._write_report(html, file_path)
