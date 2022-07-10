#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

from __future__ import annotations

import os
from io import StringIO
from coverage import Coverage, CoverageException
from typing import Sequence, Optional, Dict
from argparse import ArgumentParser
from requests import get


def coverage_color(rate: float, colors: str) -> str:
    """
    Return the badge color for a given rate and colors string\n
    :param coverage rate: in percentage
    :param colors: in format "color0 < % < color1 < % ... < color_n"
    :return color as string:
    """
    data = colors.split("<")
    colors = [x.strip() for i, x in enumerate(data) if i % 2 == 0]
    rates = [float(x.strip()) for i, x in enumerate(data) if i % 2 == 1]
    if len(rates) + 1 != len(colors):
        raise ValueError("Invalid colors array")
    for i, r in enumerate(rates):
        if rate < r:
            return colors[i]
    return colors[-1]


def make_dirs_if_needed(path: str) -> None:
    abs_path = os.path.abspath(path)
    dir_path = os.path.dirname(abs_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def format_args(options: Dict[str, str]) -> str:
    keys = ["style", "logo"]
    return "&".join([f"{k}={v.strip()}" for k, v in options.items() if k in keys])


def load_badge(rate: float, colors: str, badge: str, args: Optional[str] = None) -> None:
    make_dirs_if_needed(badge)
    color = coverage_color(rate, colors)
    url = f"https://img.shields.io/badge/coverage-{rate:.1f}%25-{color}"
    if args is not None:
        url += "?" + args
    with open(badge, "wb") as badge_output:
        r = get(url, allow_redirects=True)
        badge_output.write(r.content)


def make_badge(db: str, badge: str, colors: str, options: Dict[str, str]) -> int:
    try:
        cov = Coverage(db)
        cov.load()
        rate = cov.report(file=StringIO())
        args = format_args(options)
        load_badge(rate, colors, badge, args)
        return 0

    except CoverageException as e:
        print(str(e))
        return 1

    except ValueError as e:
        print(str(e))
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    parser = ArgumentParser()

    parser.add_argument("--input", type=str, default="./test.coverage", help="Coverage report file")

    parser.add_argument("--output", type=str, default="./coverage.svg", help="Coverage badge file")

    parser.add_argument(
        "--colors",
        type=str,
        default="red < 50.0 < orange < 75.0 < yellow < 95.0 < green",
        help='Badge color in format: "color1 < % < color2 < % ... << color_n"',
    )

    parser.add_argument(
        "--style",
        type=str,
        default=None,
        required=False,
        help="Badge style: plastic | flat | flat-square | for-the-badge | social",
    )

    parser.add_argument(
        "--logo",
        type=str,
        default=None,
        required=False,
        help="Badge logo: see https://simpleicons.org/ for names of icons",
    )

    args = parser.parse_args(argv)
    options = {}
    if args.style is not None:
        options["style"] = args.style
    if args.logo is not None:
        options["logo"] = args.logo

    return make_badge(
        db=args.input,
        badge=args.output,
        colors=args.colors,
        options=options,
    )


if __name__ == "__main__":
    raise SystemExit(main())
