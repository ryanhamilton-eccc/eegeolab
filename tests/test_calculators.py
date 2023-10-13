#!/usr/bin/env python

"""Tests for `eegeolab` package."""


import unittest
import ee

from eegeolab.bandmath.ndvi import NDVI


class TestNDVICalculator(unittest.TestCase):
    """Tests for `eegeolab` package."""

    def setUp(self):
        ee.Initialize()
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""
