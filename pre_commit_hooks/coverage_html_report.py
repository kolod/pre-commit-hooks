#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from __future__ import annotations

from argparse import ArgumentParser
from typing import Sequence
from coverage import Coverage, CoverageException


def make_html_report(db: str, report: str) -> int:
    try:
        cov = Coverage(db)
        cov.load()
        cov.html_report(directory=report)
        return 0

    except CoverageException as e:
        print(str(e))
        return 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, default="./test.coverage", help="Coverage report file")
    parser.add_argument("--output", type=str, default="./htmlcov", help="Coverage html report path")
    args = parser.parse_args(argv)
    return make_html_report(
        db=args.input,
        report=args.output,
    )


if __name__ == "__main__":
    raise SystemExit(main())
