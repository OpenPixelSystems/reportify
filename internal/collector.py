'''
@File     :  collector.py
@Desc     :  Collector class, to collect the assets
@Authors  :  Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/12/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

import glob

from internal.logger import Logger
from internal.internal_types import ReportMode


class Asset:
    source: str
    destination: str

    def __init__(self, source: str, destination: str) -> None:
        self.source = source
        self.destination = destination


class Collector:
    folder: str
    logger: Logger

    def __init__(self, folder: str, logger: Logger) -> None:
        self.folder = folder
        self.logger = logger

    def css_filenames(self, mode: ReportMode) -> list[Asset]:
        assets: list[Asset] = []

        filenames = self._css_shared_filenames()

        mode_folder = self.folder + '/' + self._mode_folder(mode)
        filenames += glob.glob(mode_folder + '/css/**/*.css', recursive=True)

        for filename in filenames:
            source = filename
            destination = filename.replace(mode_folder, '').replace(self._shared_folder(), '')
            assets.append(Asset(source, destination))

        return assets

    def _shared_folder(self) -> str:
        return self.folder + '/shared'

    def js_filenames(self, mode: ReportMode) -> list[Asset]:
        assets: list[Asset] = []

        filenames = self._js_shared_filenames()

        mode_folder = self.folder + '/' + self._mode_folder(mode)
        filenames += glob.glob(mode_folder + '/js/**/*.js', recursive=True)

        for filename in filenames:
            source = filename
            destination = filename.replace(mode_folder, '').replace(self._shared_folder(), '')
            assets.append(Asset(source, destination))

        return assets

    def _css_shared_filenames(self) -> list[str]:
        return glob.glob(self._shared_folder() + '/css/**/*.css', recursive=True)

    def _js_shared_filenames(self) -> list[str]:
        return glob.glob(self._shared_folder() + '/js/**/*.js', recursive=True)

    def _mode_folder(self, mode: ReportMode) -> str:
        if mode == ReportMode.STATIC:
            return 'static'
        elif mode == ReportMode.DYNAMIC:
            return 'dynamic'
