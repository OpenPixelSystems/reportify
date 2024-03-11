'''
@File     :  dynamic_generator.py
@Desc     :  Dynamic generator class, to write the dynamic HTML report and copy the assets to disk
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  25/12/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

import os
import shutil

from internal.generator import Generator


class DynamicGenerator(Generator):
    def report(self, html: str, output_folder: str) -> bool:
        report_folder = os.path.join(output_folder, 'report')

        if not os.path.isdir(report_folder):
            os.mkdir(report_folder)

        css_folder = os.path.join(report_folder, 'css')

        if not os.path.isdir(css_folder):
            os.mkdir(css_folder)

        js_folder = os.path.join(report_folder, 'js')

        if not os.path.isdir(js_folder):
            os.mkdir(js_folder)

        report_file_path = os.path.join(report_folder, 'report.html')

        return self._write_report(html, report_file_path) and self._copy_assets(report_folder)

    def _copy_assets(self, report_folder: str) -> bool:
        for style in self.styles:
            os.makedirs(os.path.dirname(report_folder + style.destination), exist_ok=True)
            shutil.copy(style.source, report_folder + style.destination)

        for script in self.scripts:
            os.makedirs(os.path.dirname(report_folder + script.destination), exist_ok=True)
            shutil.copy(script.source, report_folder + script.destination)

        return True
