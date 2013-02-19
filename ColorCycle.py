import sublime, sublime_plugin
import fnmatch
import os
from collections import deque

class ColorSchemeCycle(sublime_plugin.ApplicationCommand):
	themes = []

	def cache_themes(self):
		themes = []
		package_path = sublime.packages_path()
		for root, dirnames, filenames in os.walk(package_path):
			for filename in fnmatch.filter(filenames, '*.tmTheme'):
				themes.append(os.path.join(root, filename))
		self.themes = deque(themes)
		
	def run(self, **args):
		if not self.themes and args['direction'] != 'cache':
			self.cache_themes()
		settingsFile = "Preferences.sublime-settings"
		settings = sublime.load_settings(settingsFile)

		direction = args['direction']
		if direction == 'left':
			self.themes.rotate(1)
		elif direction == 'right':
			self.themes.rotate(-1)
		sublime.status_message("Theme: " + os.path.basename(self.themes[0])[:-8])
		settings.set("color_scheme",self.themes[0])
		sublime.save_settings(settingsFile)
