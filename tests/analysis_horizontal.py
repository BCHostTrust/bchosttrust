# bchosttrust/tests/analysis_horizontal.py
# test bchosttrust.analysis.horizontal

# Copyright (C) 2023  Marco Pui, Cato Yiu, Lewis Chen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# The legal text of GPLv3 and LGPLv3 can be found at
# bchosttrust/gpl-3.0.txt and bchosttrust/lgpl-3.0.txt respectively.

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
