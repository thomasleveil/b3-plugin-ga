Google Analytics plugin for Big Brother Bot
===========================================

http://www.bigbrotherbot.net


Description
-----------

This plugin sends tracking events to Google Analytics.

You need to create a Google Analytics profile and set the GA profile ID accordingly in this plugin config file.



Installation
------------

- copy the `extplugins/ga` directory into `b3/extplugins`
- copy `extplugins/conf/plugin_ga.ini` in the directory where `b3.xml` is in
- edit `plugin_ga.ini` and set your Google Analytics profile id (UA-xxxxxx-x)
- add to the `plugins` section of your main b3 config file:

  `<plugin name="ga" config="@conf/plugin_ga.ini" />`


