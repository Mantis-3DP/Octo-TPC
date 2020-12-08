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
import numpy as np
import octoprint_tpc.cv as multi
import octoprint_tpc.offsetCalc as oC


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
		self.x = 0
		self.y = 0
		self.z = 0

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
			camerastep=dict(x=2, y=2),
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
			# xyr, success = multi.position()
			response = dict(success=True, x=self.offset[0], y=self.offset[1])
			return flask.jsonify(response)

	def on_api_command(self, command, data):

		self._logger.info(str(command))
		if command == "sendToPy":
			step = "{step}".format(**data)
			self._logger.info(step)
			self.calibration(step)

		# xy, r, success = multi.position()
		# datatype = "{state}".format(**data)
		# bOn = "{state}".format(**data)
		# lol = cv.double(bOn)
		# self._printer.commands(5)  # sendet ins terminal
		# self._logger.info("Hello World! (more: {}){}".format(success, datatype))
		# self._logger.info(self._settings.get(["feed_rate"]))
		# self._printer.commands("G1 " + "F" + self._settings.get(["feed_rate"]))
		# + self._settings.get("feed_rate")
		elif command == "nozzle_position":

			datatype = "{wert}".format(**data)
			self._logger.info("nozzle_position ausgeführt %s" % datatype)

	##~~ Softwareupdate hook
	# Use the on_event hook to extract XML data every time a new file has been loaded by the user
	def on_event(self, event, payload):
		# TODO: instead search for M114 in terminal output
		if event == "PositionUpdate":
			self.x: float = payload["x"]
			self.y: float = payload["y"]
			self.z: float = payload["z"]
			self._logger.info("X" + str(payload["x"]) + " Y" + str(payload["y"]) + " Z" + str(payload["z"]))

	# else:
	# 	self._logger.info(event, payload)

	def toolToOffset(self, choice):
		# self._logger.info(choice + ".x")
		choices = self._settings.get([str(choice)])
		offset = np.zeros([2])
		offset[0] = choices["x"]
		offset[1] = choices["y"]

		# offset[0] = self._settings.get([str(choice) + ".x"])
		# offset[1] = self._settings.get([str(choice) + ".y"])
		feed_rate = self._settings.get(["feed_rate"])

		# commands
		# self._printer.commands(self._settings.get(["takeTool".format(toolnumber)]))  # settings string
		self._printer.commands("G1 X{} Y{} F{}".format(offset[0], offset[1], feed_rate))
		self._printer.commands("G90")
		self._printer.commands("M400")
		return offset[0:2]

	def saveOffset(self):
		# SET_GCODE_OFFSET [X=<pos>] [Y=<pos>] [Z=<pos>] [MOVE=1 [MOVE_SPEED=<speed>]]
		self._printer.commands("SET_GCODE_OFFSET X{} Y{}".format(self.offset[0], self.offset[1]))
		self._printer.commands("SAVE_CONFIG")

	def calibration(self, step):

		if step == "0":
			self.xyr0 = np.zeros([2])
			self.xyr1 = np.zeros([2])
			self.offset = np.zeros([2])
			self.tempOffset = np.zeros([2])
			self.exOffset = np.zeros([2])
			self.stepsTaken = []
			np.append(self.stepsTaken, step)
			self.resolution = np.zeros([2])

			self.xyCamera = self._settings.get(["camera"])

			self._printer.commands("T2")

		elif step == "1":
			########################################
			#           TAKE TOOL                  #
			# position the nozzle above the camera #
			########################################
			# TODO: printer command aus settings

			self._printer.commands("G90")
			self._printer.commands("G1 X323 F1200")
			self._printer.commands("G1 Y191 F1200")
			self._printer.commands("M400")

			self._printer.commands("M114")

			self._logger.info(self.xyCamera["x"])
			self._logger.info(self.xyCamera["y"])

		# self.x = 265
		# self.y = 200
		# das Tool steht vor und etwas nach rechts

		# tempOffset[0] = 270 - 265 = 5
		# tempOffset[1] = 220 - 200 = 20
		# in x 5mm
		# in y 20mm
		# Von dieser Stelle will ich dann den Abstand zur unteren linken Ecke des Camerabildes

		elif step == "2":
			self.xyr0, success, width, height = multi.position()
			self.resolution = [width, height]

			# hier mit will ich die Distanz zwischen der Momentanen Position der Camera relativ zur Aufnahme und der neuen
			# Position des Tools

			self.tempOffset[0] = float(self.xyCamera["x"]) - self.x
			self.tempOffset[1] = float(self.xyCamera["y"]) - self.y
			self._logger.info(self.tempOffset)
			# Nun weiß ich, dass bei einem offset von x5 y20 die Nozzle an der Position xc300 yc150 auf Caera zu sehen
			# ist. Das ist die Translation vom 0 Punkt

			if success == False:
				self._logger.info("No Point recognized")
			np.append(self.stepsTaken, step)

		elif step == "3":
			self._printer.commands("G91")
			self.toolToOffset("camerastep")
			np.append(self.stepsTaken, step)
		# das Tool fährt nun +x2 +y2 und ist somit an der Stelle
		# self.x = 267
		# self.y = 202

		elif step == "4":
			self.xyr1, success, _, _ = multi.position()
			np.append(self.stepsTaken, step)
		# Dann wird wieder ein Bild aufgenommen
		# xc400 yc250
		# aus dem Vektor von xc300yc150 zu xc400 yc250 lässt sich die Rotation und pixel pro mm fahrt bestimmen


		elif step == "5":

			# TODO: das hier muss anders. so kann man das nicht prüfen

			self._logger.info(self.xyr0)
			self.xyr1 = self.xyr0 + [50, 50]
			self._logger.info(self.xyr1)

			self.exOffset = oC.calcOffset(self.xyr0, self.xyr1, self._settings.get(["camerastep"]), self.resolution)
			self.offset = self.tempOffset + self.exOffset
			self.offset = np.round(self.offset, 2)
			# aus xc400-xc300 => +xc = 100 damit bewegt sich die Nozzle im Bild mit 100px/mm

			# die Annahme die getroffen werden muss ist, dass die Aufnahme bei einem Offset von x0y0 sich genau in
			# der unteren linken Ekce der Camera befindet.
			# Also x270 y220 ist die koordinete der linken unteren Ecke
			# damit ist der Offset dann
			# tempOffset[0] = 270 - 265 = 5
			# tempOffset[1] = 220 - 200 = 20
			# tempOffset[0] + xc300/100px/mm = 3
			# tempOffset[1] + xc150/100px/mm = 1,5
			# offset[0] = 8
			# offset[1] = 21,5

			if len(self.exOffset) == 0:
				self._logger.info("no offset calculated")
			np.append(self.stepsTaken, step)


		elif step == "10":
			self.saveOffset()
			# self._settings.set(["tool0.x"], self.offset[0])
			# self._settings.set(["tool0.y"], self.offset[1])
			# self._settings.save()
			np.append(self.stepsTaken, step)

		else:
			self._logger.info("no available step was used")

		return

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
