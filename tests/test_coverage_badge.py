#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021-... Oleksandr Kolodkin <alexandr.kolodkin@gmail.com>.
# This program is distributed under the MIT license.
# Glory to Ukraine!

import io
import unittest
from os.path import dirname, realpath, join
from os import listdir, remove
from pre_commit_hooks.coverage_badge import coverage_color, load_badge, make_badge, main


class TestCoverageBadge(unittest.TestCase):
    def assertFileEqual(self, expected: str, actual: str):
        try:
            with open(expected, "r") as expected_file:
                with open(actual, "r") as actual_file:
                    expected_text = expected_file.read()
                    actual_text = actual_file.read()
                    self.assertEqual(expected_text, actual_text)
        except Exception as e:
            self.fail(str(e))

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
        path = dirname(realpath(__file__)) + "/files"
        actual = path + "/actual_badge.svg"
        expected = path + "/expected_badge.svg"
        try:
            load_badge(96.0, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green", actual)
            self.assertFileEqual(expected, actual)
        except Exception as e:
            self.fail(str(e))

    def test_load_badge_flat(self):
        path = dirname(realpath(__file__)) + "/files"
        actual = path + "/actual_badge_flat.svg"
        expected = path + "/expected_badge_flat.svg"
        try:
            load_badge(80.42226487523992, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green", actual, "style=flat")
            self.assertFileEqual(expected, actual)
        except Exception as e:
            self.fail(str(e))

    def test_make_badge(self):
        path = dirname(realpath(__file__)) + "/files"
        data = path + "/test.coverage"
        actual = path + "/actual_badge_flat.svg"
        expected = path + "/expected_badge_flat.svg"
        try:
            make_badge(data, actual, "red < 50.0 < orange < 75.0 < yellow < 95.0 < green", {"style": "flat"})
            self.assertFileEqual(expected, actual)
        except Exception as e:
            self.fail(str(e))

    def test_main(self):
        path = dirname(realpath(__file__)) + "/files"
        data = path + "/test.coverage"
        actual = path + "/actual_badge_flat.svg"
        expected = path + "/expected_badge_flat.svg"
        try:
            options = [
                "--input",
                data,
                "--output",
                actual,
                "--colors",
                "red < 50.0 < orange < 75.0 < yellow < 95.0 < green",
                "--style",
                "flat",
            ]
            main(options)
            self.assertFileEqual(expected, actual)
        except Exception as e:
            self.fail(str(e))

    @staticmethod
    def stopTestRun():
        path = dirname(realpath(__file__)) + "/files"
        for file in listdir(path):
            if file.startswith("actual_"):
                remove(join(path, file))


if __name__ == "__main__":
    unittest.main()
