# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class FloctoPlugin(octoprint.plugin.ProgressPlugin,
				   octoprint.plugin.StartupPlugin):
	
	def __init__(self):
		self._initialized = False

	# internal initialize
	# we do it this weird way because __init__ gets called before the injected
	# properties but on_after_startup can be too late in the case of auto
	# connect on startup in which case the serial_factory is called first
	def _initialize(self):
		if self._initialized:
			return
		self._initialized = True
	
	# StartupPlugin
	def on_after_startup(self, *args, **kwargs):
		self._initialize()
	
	# main serial connection hook
	def serial_factory(self, comm, port, baudrate, timeout, *args, **kwargs):
		return None

def __plugin_load__():
	plugin = FloctoPlugin()

	global __plugin_implementation__
	__plugin_implementation__ = plugin

	global __plugin_hooks__
	__plugin_hooks__ = {
			"octoprint.comm.transport.serial.factory": plugin.serial_factory
		}

__plugin_name__ = "Flocto"
__plugin_version__ = "0.0.1"
__plugin_description__ = "Support for Flashforge Printers in Octoprint"
