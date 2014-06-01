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
from ConfigParser import NoOptionError
from b3.plugin import Plugin
from .pyga.requests import Tracker
from .pyga.entities import Page, Session, Visitor

__version__ = '0.1'
__author__ = 'Courgette'


class GaPlugin(Plugin):

    def __init__(self, console, config=None):
        Plugin.__init__(self, console, config)

        self._ga_tracking_id = None
        """:type : str"""

        self.tracker = None
        """:type : Tracker"""

    ####################################################################################################################
    ##                                                                                                                ##
    ##   STARTUP                                                                                                      ##
    ##                                                                                                                ##
    ####################################################################################################################

    def onLoadConfig(self):
        """\
        Load plugin configuration
        """
        try:
            self._ga_tracking_id = self.config.get('google analytics', 'tracking ID')
            if not self._ga_tracking_id.startswith('UA-'):
                raise ValueError("Google Analytics tracking ID must start with 'UA-'")
            self.info('loaded "google analytics/tracking ID": %s' % self._ga_tracking_id)
        except (NoOptionError, ValueError), e:
            self.error('could not load "google analytics/tracking ID". %s' % e)
            self._ga_tracking_id = None

    def onStartup(self):
        if self._ga_tracking_id:
            # set up GA client
            self.tracker = Tracker(self._ga_tracking_id)

            # register events
            self.registerEvent(self.console.getEventID('EVT_CLIENT_AUTH'), self.on_auth)
            self.registerEvent(self.console.getEventID('EVT_CLIENT_DISCONNECT'), self.on_disconnect)
            self.registerEvent(self.console.getEventID('EVT_GAME_ROUND_START'), self.on_round_start)

    ####################################################################################################################
    ##                                                                                                                ##
    ##   EVENTS                                                                                                       ##
    ##                                                                                                                ##
    ####################################################################################################################

    def on_auth(self, event):
        """
        Event handler when a player connects to the game server.

        :param event: b3.event.Event
        """
        self.track(event.client)

    def on_disconnect(self, event):
        """
        Event handler when a player disconnects from the game server.

        :param event: b3.event.Event
        """
        self.track(event.client, '/end')

    def on_round_start(self, event):
        """
        Event handler when a new round starts on the game server.

        :param event: b3.event.Event
        """
        for client in self.console.clients.getList():
            self.track(client)

    ####################################################################################################################
    ##                                                                                                                ##
    ##   UTILS                                                                                                        ##
    ##                                                                                                                ##
    ####################################################################################################################

    def track(self, client, page=None):
        """
        Send a 'track pageview' event to google analytics for the given client and page.
        If page is None, then it is built based on current map and gametype.

        :param client: b3.client.Client
        :param page: str
        :return: None
        """
        if not client:
            return
        session = client.var(plugin=self, key="session", default=Session()).value
        visitor = client.var(plugin=self, key="visitor", default=None).value
        if visitor is None:
            visitor = Visitor()
            visitor.add_session(session)
            visitor.ip_address = client.ip or None
        if page is None:
            page = "/B3/%s/%s" % (self.console.game.gameType, self.console.game.mapName)
        self.tracker.track_pageview(Page(page), session, visitor)