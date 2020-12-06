# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import flask
import time
import octoprint_tpc.cv as multi


class TpcPlugin(octoprint.plugin.SettingsPlugin,
				octoprint.plugin.AssetPlugin,
				octoprint.plugin.StartupPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.SimpleApiPlugin,
				octoprint.plugin.EventHandlerPlugin):

	# import octoprint_tpc.cv as multiple importiert meine neue file die dann wie gewohnt mit multiple.function
	# aufgerufen werden kann

	##~~ SettingsPlugin mixi
	def on_after_startup(self):
		####### test
		# self.lol = cv.double(5)
		# self._logger.info(self.lol)

		self._logger.info("Tpc started! %s" % self._settings.get(["nozzle_temp"]))
		self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
			url="https://en.wikipedia.org/wiki/Hello_world",
			nozzle_temp=180,
			feed_rate=1200,
			# camera position
			camera=dict(x=100, y=160, z=20),
			# Offsets in mm
			tool0=dict(x=1, y=6, z=-0.3),
			tool1=dict(x=6, y=3, z=-0.8),
			tool2=dict(x=3, y=2, z=-0.2),
			tool3=dict(x=2, y=1, z=-0.5),
			# take tool
			takeTool="T{}"
		)

	def get_template_configs(self):
		return [dict(type="settings", custom_bindings=False),
				dict(type="navbar", custom_bindings=False)]

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/tpc.js"],
			css=["css/tpc.css"],
			less=["less/tpc.less"]
		)

	##~~ SimpleApiPlugin

	# wenn der command ausgeführt wird, wird in on api command etwas ausgeführt.
	#
	def get_api_commands(self):
		return dict(sendToPy=["step"],
					nozzle_position=["wert"]  # was muss für Wert rein? da ist ein String drin
					)

	def on_api_get(self, request):
		if request.args.get("getPosition"):
			self._logger.debug(request.args)

			xyr, success = multi.position()
			response = dict(success=success, x=xyr[0], y=xyr[1])
			self._printer.commands("M114")

			return flask.jsonify(response)

	def on_api_command(self, command, data):
		self._logger.info(str(command))
		if command == "sendToPy":
			step = "{step}".format(**data)
			if step == "1":
				self._logger.info(step)
			else:
				self._logger.info("anotior step " + step)
			# xy, r, success = multi.position()
			# datatype = "{state}".format(**data)
			# bOn = "{state}".format(**data)
			# lol = cv.double(bOn)
			# self._printer.commands(5)  # sendet ins terminal
			# self._logger.info("Hello World! (more: {}){}".format(success, datatype))
			self._logger.info(self._settings.get(["feed_rate"]))
			self._printer.commands("G1 " + "F" + self._settings.get(["feed_rate"]))
		# + self._settings.get("feed_rate")
		elif command == "nozzle_position":

			datatype = "{wert}".format(**data)
			self._logger.info("nozzle_position ausgeführt %s" % datatype)

	##~~ Softwareupdate hook
	# Use the on_event hook to extract XML data every time a new file has been loaded by the user
	def on_event(self, event, payload):
		if event == "PositionUpdate":
			self.x = payload["x"]
			self.y = payload["y"]
			self.z = payload["z"]
			self._logger.info("X" + str(payload["x"]) + " Y" + str(payload["y"]) + " Z" + str(payload["z"]))
		else:
			self._logger.info(event, payload)

	def toolTocamera(self, toolnumber):
		camera = []
		camera[0] = self._settings.get(["camera.x"])
		camera[1] = self._settings.get(["camera.y"])
		feed_rate = self._settings.get(["feed_rate"])

		# commands
		self._printer.commands(self._settings.get(["takeTool".format(toolnumber)]))  # settings string
		self._printer.commands("G1 X{} Y{} F{}".format(camera[0], camera[1], feed_rate))

	def run_gcode(self):
		self._printer.commands("M114")

		self._printer.commands("G1 " + "F" + self._settings.get(["feed_rate"]))




	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			tpc=dict(
				displayName="Tpc Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="Mantis-3DP",
				repo="OctoPrint-Tpc",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/Mantis-3DP/OctoPrint-Tpc/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Tpc Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
__plugin_pythoncompat__ = ">=3,<4"  # only python 3


# __plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = TpcPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
