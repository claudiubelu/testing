#!/usr/bin/env python

"""Tests for `fib` package."""


import unittest

from sobolanism.compute import fib


class TestFibGenerator(unittest.TestCase):
    """Tests for `fib` package."""

    def setUp(self):
        super().setUp()
        self._gen = fib.FibGenerator()

    def test_fib_zero(self):
        result = self._gen.fibonate(0)
        self.assertEqual(0, result)

    def test_fib_one(self):
        result = self._gen.fibonate(1)
        self.assertEqual(1, result)

    def test_fib(self):
        result = self._gen.fibonate(5)
        self.assertEqual(5, result)
