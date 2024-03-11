#!/usr/bin/python3

'''
@File     :  generate.py
@Desc     :  Script, to generate QA test reports from JSON files
@Authors  :  Bram Vlerick <bram.vlerick@openpixelsystems.org>, Nick Vissers <nick.vissers@openpixelsystems.org>
@Date     :  23/11/2023
@Version  :  1.0
@License  :  Copyright (C) 2023 Open Pixel Systems. All rights reserved.
          :  Confidential and for internal use only. The content of this document constitutes proprietary
          :  information of the Open Pixel Systems company. Any disclosure, copying, distribution or use
          :  of any part of the content of this document by unauthorized parties is strictly prohibited.
'''

import argparse
import os
import sys

from enum import Enum

from internal.builder import Builder
from internal.collector import Collector
from internal.factories.builder import BuilderFactory
from internal.factories.generator import GeneratorFactory
from internal.logger import Logger
from internal.parser import Parser
from internal.types import ReportMode


class Error(Enum):
    NONE = 0
    INPUT_EMPTY = 1
    OUTPUT_EMPTY = 2
    PARSE = 3
    GENERATE_JSON = 4
    GENERATE_REPORT = 5


def validArguments(args: any, logger: Logger) -> Error:
    if args.input == '':
        logger.error('input parameter is empty')
        return Error.INPUT_EMPTY

    if args.output == '':
        logger.error('output parameter is empty')
        return Error.OUTPUT_EMPTY

    return Error.NONE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='path to JSON input files (e.g., "json1,json2")', required=True)
    parser.add_argument('-o', '--output', help='path to HTML output file', required=True)
    parser.add_argument('-t', '--title', help='title of the report', required=True)
    parser.add_argument('-d', '--dynamic', help='generate dynamic report', action='store_true', required=False)
    parser.add_argument('-s', '--self-test', help='include self tests', action='store_true', required=False)
    parser.add_argument('-v', '--verbose', help='verbose output', action='store_true', required=False)

    args = parser.parse_args()

    logger = Logger(args.verbose)

    ret = validArguments(args, logger)
    if ret != Error.NONE:
        parser.print_help()
        sys.exit(ret.value)

    mode = ReportMode.STATIC

    if (args.dynamic):
        mode = ReportMode.DYNAMIC

    assets = os.path.dirname(os.path.abspath(__file__)) + '/' + 'assets'

    collector = Collector(assets, logger)

    styles = collector.css_filenames(mode)
    scripts = collector.js_filenames(mode)

    parser = Parser(args.input, args.self_test, logger)
    builder = BuilderFactory.create(mode, styles, scripts, logger)
    generator = GeneratorFactory.create(mode, styles, scripts, logger)

    tests = parser.parse()
    if tests is None:
        sys.exit(Error.PARSE.value)

    test_data = generator.test_data(tests)
    if test_data == '':
        sys.exit(Error.GENERATE_JSON.value)

    data = Builder.Data(tests, test_data)
    html = builder.build(args.title, data)

    if not generator.report(html, args.output):
        sys.exit(Error.GENERATE_REPORT.value)

    logger.success(f'report generated: {os.path.abspath(args.output)}')


if __name__ == '__main__':
    main()
