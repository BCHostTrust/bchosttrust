# bchosttrust/tests/analysis_horizontal.py
# test bchosttrust.analysis.horizontal

# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from bchosttrust.analysis import horizontal


class BCHTHorizontalTestCase(unittest.TestCase):
    def test_get_simular_names_no_self(self):
        from_name = "www.example.com"
        list_names = ("www.example.com", "www.example.net",
                      "www.example.org", "www.google.com")
        simular = horizontal.get_simular_names(from_name, list_names)

        self.assertFalse(from_name in simular)
