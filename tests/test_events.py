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
from ga.pyga.requests import GIFRequest
from tests import logging_disabled
from mock import patch


@patch.object(GIFRequest, 'fire')
class Test_events(unittest.TestCase):

    def setUp(self):
        with logging_disabled():
            from b3.fake import FakeConsole, FakeClient
            self.console = FakeConsole('@b3/conf/b3.distribution.xml')
        self.conf = CfgConfigParser()
        self.p = GaPlugin(self.console, self.conf)

        self.conf.loadFromString(dedent("""
            [google analytics]
            tracking ID: UA-000000-0
        """))
        self.p.onLoadConfig()
        self.p.onStartup()
        self.assertIsNotNone(self.p._ga_tracking_id)

        self.joe = FakeClient(self.console, name="Joe", guid="GUID_joe", ip="12.12.12.12")
        self.jack = FakeClient(self.console, name="Jack", guid="GUID_jack", ip="45.45.45.45")

    def test_auth(self, fire_mock):
        self.joe.connects("1")
        # THEN
        self.assertEqual(1, len(fire_mock.mock_calls))

    def test_disconnect(self, fire_mock):
        self.joe.connects("1")
        self.joe.disconnects()
        # THEN
        self.assertEqual(2, len(fire_mock.mock_calls))

    def test_new_round(self, fire_mock):
        # GIVEN
        self.joe.connects("1")
        self.jack.connects("2")
        # WHEN
        self.console.game.gameType = "The game type"
        self.console.game.mapName = "The map name"
        self.console.queueEvent(self.console.getEvent('EVT_GAME_ROUND_START', data=self.console.game))
        # THEN
        self.assertEqual(4, len(fire_mock.mock_calls))