# -*- coding: utf-8 -*-

"""
=========================
	@name: Pyoro
	@author: Ptijuju22
	@date: 10/05/2018
	@version: 1.1
=========================
"""

from cx_Freeze import setup, Executable
import os, json, sys

def getResourcePaths():
	print("[INFO] [getResourcePaths] Detecting resources")
	resources = []
	resourcePath = os.path.join("data", "resources.json")

	if os.path.exists(resourcePath):
		with open(resourcePath, "r") as file:
			res = json.load(file)
			for resType in ("musics", "sounds", "images", "external"):
				for fp in res[resType]:
					resPath = os.path.join("data", *fp)
					print("[INFO] [getResourcePaths] \"{}\" added".format(resPath))
					resources.append((resPath, resPath))
	else:
		print("[WARNING] [getResourcePaths] Unable to find \"{}\"".format(resourcePath))
	return resources

def main():
	print("[INFO] [main] Starting setup")
	resources = getResourcePaths()
	
	base = None
	if sys.platform == "win32":
		print("[INFO] [main] Platform detected : Windows")
		base = "Win32GUI"

	executable = Executable(
		"main.py",
		targetName = "Pyoro.exe",
		icon = os.path.join("data", "images", "gui", "pyoro_icon.ico"),
		base = base,
		shortcutName = "Pyoro"
	)

	print("[INFO] [main] Building game\n===========================")
	setup(
		name = "Pyoro",
		version = "1.1",
		author = "Julien Dubois",
		description = "Python Pyoro for Windows",
		options = 
		{
			"build_exe":
			{
				"include_files": resources
			}
		},
		executables = [executable],
	)
	print("===========================")
	print("[INFO] [main] Ending setup")

if __name__ == "__main__":
	main()
	os.system("pause")