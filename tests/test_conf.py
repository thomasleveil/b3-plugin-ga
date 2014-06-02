#
# Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2014 Courgette
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
from textwrap import dedent
import unittest
from b3.config import CfgConfigParser
from ga import GaPlugin
from tests import logging_disabled


class Test_conf(unittest.TestCase):

    def setUp(self):
        with logging_disabled():
            from b3.fake import FakeConsole
            self.console = FakeConsole('@b3/conf/b3.distribution.xml')
        self.conf = CfgConfigParser()
        self.p = GaPlugin(self.console, self.conf)

    def test_empty_conf(self):
        self.conf.loadFromString("""""")
        self.p.onLoadConfig()
        self.p.onStartup()
        self.assertIsNone(self.p._ga_tracking_id)

    def test_missing_tracking_id(self):
        self.conf.loadFromString(dedent("""
            [google analytics]
        """))
        self.p.onLoadConfig()
        self.p.onStartup()
        self.assertIsNone(self.p._ga_tracking_id)

    def test_bad_tracking_id(self):
        self.conf.loadFromString(dedent("""
            [google analytics]
            tracking ID: xx-xxxxx-x
        """))
        self.p.onLoadConfig()
        self.p.onStartup()
        self.assertIsNone(self.p._ga_tracking_id)

    def test_bad_tracking_id2(self):
        self.conf.loadFromString(dedent("""
            [google analytics]
            tracking ID: UA-123456-x
        """))
        self.p.onLoadConfig()
        self.p.onStartup()
        self.assertIsNone(self.p._ga_tracking_id)

    def test_nominal(self):
        self.conf.loadFromString(dedent("""
            [google analytics]
            tracking ID: UA-1234567-8
        """))
        self.p.onLoadConfig()
        self.p.onStartup()
        self.assertEqual("UA-1234567-8", self.p._ga_tracking_id)
