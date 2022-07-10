#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import io
import unittest
from os.path import dirname, realpath

from pre_commit_hooks.coverage_badge import coverage_color, load_badge, make_badge, main


class TestCoverageBadge(unittest.TestCase):
    def test_coverage_color_red(self):
        expected = "red"
        actual = coverage_color(10.0, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green")
        self.assertEqual(expected, actual)

    def test_coverage_color_orange(self):
        expected = "orange"
        actual = coverage_color(66.1, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green")
        self.assertEqual(expected, actual)

    def test_coverage_color_yellow(self):
        expected = "yellow"
        actual = coverage_color(86.5, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green")
        self.assertEqual(expected, actual)

    def test_coverage_color_green(self):
        expected = "green"
        actual = coverage_color(96.0, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green")
        self.assertEqual(expected, actual)

    def test_coverage_color_00ff00(self):
        expected = "00ff00"
        actual = coverage_color(96.0, "red < 50.0 < orange < 75.0 < yellow < 95.0 < 00ff00")
        self.assertEqual(expected, actual)

    def test_coverage_color_expected_1(self):
        with self.assertRaises(Exception) as context:
            coverage_color(96.0, "red < 50.0 < orange < 75.0 < yellow < 95.0")
        self.assertEqual("Invalid colors array", str(context.exception))

    def test_coverage_color_expected_2(self):
        with self.assertRaises(Exception) as context:
            coverage_color(96.0, "red < 50.0 < orange < 75.0 < yellow < five < green")
        self.assertEqual("could not convert string to float: 'five'", str(context.exception))

    def test_load_badge_default(self):
        path = dirname(realpath(__file__))
        actual = path + "/actual_badge.svg"
        expected = path + "/expected_badge.svg"
        try:
            load_badge(96.0, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green", actual)
            self.assertListEqual(list(io.open(expected)), list(io.open(actual)))
        except Exception as e:
            self.fail(str(e))

    def test_load_badge_flat(self):
        path = dirname(realpath(__file__))
        actual = path + "/actual_badge_flat.svg"
        expected = path + "/expected_badge_flat.svg"
        try:
            load_badge(80.42226487523992, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green", actual, "style=flat")
            self.assertListEqual(list(io.open(expected)), list(io.open(actual)))
        except Exception as e:
            self.fail(str(e))

    def test_make_badge(self):
        path = dirname(realpath(__file__))
        data = path + "/.coverage"
        actual = path + "/actual_badge_flat.svg"
        expected = path + "/expected_badge_flat.svg"
        try:
            make_badge(data, actual, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green", {"style": "flat"})
            self.assertListEqual(list(io.open(expected)), list(io.open(actual)))
        except Exception as e:
            self.fail(str(e))

    def test_main(self):
        path = dirname(realpath(__file__))
        data = path + "/.coverage"
        actual = path + "/actual_badge_flat.svg"
        expected = path + "/expected_badge_flat.svg"
        try:
            main(
                (
                    "--input",
                    data,
                    "--output",
                    actual,
                    "--colors",
                    "red < 50.0 < orange < 75.0 < yellow < 95.0 < green",
                    "--style",
                    "flat",
                )
            )
            self.assertListEqual(list(io.open(expected)), list(io.open(actual)))
        except Exception as e:
            self.fail(str(e))


if __name__ == "__main__":
    pass
