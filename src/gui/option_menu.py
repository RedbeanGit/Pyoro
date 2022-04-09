# -*- coding: utf-8 -*-

#	This file is part of Pyoro (A Python fan game).
#
#	Metawars is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	Metawars is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide a menu to manage game options.

Created on 21/08/2018
"""

import os
from pygame.locals import KEYDOWN, JOYBUTTONDOWN, JOYAXISMOTION, JOYHATMOTION

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import GUI_IMAGE_PATH, NAME, VERSION
from game.util import getKeyName, getJoyKeyName, resetGame, Game

from gui.button import Button
from gui.setting_bar import Setting_bar
from gui.text import Text
from gui.menu_widget import Menu_widget


class Option_menu(Menu_widget):
	"""
	Create a menu allowing the player to change some game settings.
	"""

	DEFAULT_KWARGS = {
		"font": os.path.join(GUI_IMAGE_PATH, "font.ttf"),
		"fontSize": 20
	}

	def __init__(self, activity, pos, quitFct, **kwargs):
		"""
		Initialize a new Option_menu widget.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The default position of this widget in a (x, y) tuple where
			x and y are integers.

		:type quitFct: callable
		:param quitFct: A function, method or class which can be called when the
			player leave this menu.
		"""

		Option_menu.updateDefaultKwargs(kwargs)
		Menu_widget.__init__(self, activity, pos, **kwargs)

		self.quitFct = quitFct
		self.waitingInput = ()

	def initWidgets(self):
		"""
		Create subwidgets which will be display in this menu.
		"""

		rp = self.getRealPos()
		f = self.kwargs["font"]
		w, h = self.kwargs["size"]
		ko = Game.options.get("keyboard", {})
		jo = Game.options.get("joystick", {})
		mv = Game.options.get("music volume", 1)
		sv = Game.options.get("sound volume", 1)
		ts = self.kwargs["fontSize"]; ms = ts - 3; ls = ms - 3

		px = int(w * 0.05)
		py = int(h * 0.15)
		self.addSubWidget("volumeMusicText", Text, (px, py), \
			"Volume de la musique", anchor = (-1, 0), fontSize = ms, font = f)
		py = int(h * 0.25)
		self.addSubWidget("volumeSoundText", Text, (px, py), \
			"Volume des sons", anchor = (-1, 0), fontSize = ms, font = f)
		py = int(h * 0.35)
		self.addSubWidget("commandTitleText", Text, (px, py), "Commandes :", \
			anchor = (-1, 0), fontSize = ms, font = f)

		px = int(w * 0.15)
		py = int(h * 0.45)
		self.addSubWidget("rightCommandText", Text, (px, py), "Aller a droite", \
			anchor = (-1, 0), fontSize = ms, font = f)
		py = int(h * 0.55)
		self.addSubWidget("leftCommandText", Text, (px, py), "Aller a gauche", \
			anchor = (-1, 0), fontSize = ms, font = f)
		py = int(h * 0.65)
		self.addSubWidget("actionCommandText", Text, (px, py), \
			"Tirer (la langue)", anchor = (-1, 0), fontSize = ms, font = f)
		py = int(h * 0.75)
		self.addSubWidget("pauseCommandText", Text, (px, py), "Pause / retour", \
			anchor = (-1, 0), fontSize = ms, font = f)

		px = int(w * 0.25)
		py = int(h * 0.95)
		self.addSubWidget("resetButton", Button, (px, py), \
			text = "Réinitialiser", anchor = (0, 0), textKwargs = {\
			"fontSize": ms, "font": f}, size = (int(w * 0.4), \
			int(h * 0.06)), onClickFct = resetGame)

		px = int(w * 0.5)
		py = int(h * 0.05)
		self.addSubWidget("titleText", Text, (px, py), "Options", \
			anchor = (0, -1), fontSize = ts, font = f)

		px = int(w * 0.66)
		py = int(h * 0.35)
		self.addSubWidget("keyboardCommandText", Text, (px, py), "Clavier", \
			anchor = (0, 0), fontSize = ms, font = f)
		py = int(h * 0.45)
		self.addSubWidget(("commandButton", "keyboard", "right"), Button, \
			(px, py), text = getKeyName(ko["right"]), size = (int(w * 0.18), \
			int(h * 0.08)), onClickFct = self.inputCommand, \
			onClickArgs = ("keyboard", "right"), anchor = (0, 0), textKwargs = { \
			"fontSize": ls, "font": f})
		py = int(h * 0.55)
		self.addSubWidget(("commandButton", "keyboard", "left"), Button, \
			(px, py), text = getKeyName(ko["left"]), size = (int(w * 0.18), \
			int(h * 0.08)), onClickFct = self.inputCommand, \
			onClickArgs = ("keyboard", "left"), anchor = (0, 0), textKwargs = { \
			"fontSize": ls, "font": f})
		py = int(h * 0.65)
		self.addSubWidget(("commandButton", "keyboard", "action"), Button, \
			(px, py), text = getKeyName(ko["action"]), size = (int(w * 0.18), \
			int(h * 0.08)), onClickFct = self.inputCommand, \
			onClickArgs = ("keyboard", "action"), anchor = (0, 0), textKwargs = { \
			"fontSize": ls, "font": f})
		py = int(h * 0.75)
		self.addSubWidget(("commandButton", "keyboard", "pause"), Button, \
			(px, py), text = getKeyName(ko["pause"]), size = (int(w * 0.18), \
			int(h * 0.08)), onClickFct = self.inputCommand, \
			onClickArgs = ("keyboard", "pause"), anchor = (0, 0), textKwargs = { \
			"fontSize": ls, "font": f})

		px = int(w * 0.75)
		py = int(h * 0.95)
		self.addSubWidget("backButton", Button, (px, py), text = "Retour", \
			anchor = (0, 0), textKwargs = {"fontSize": ms, "font": f}, \
			size = (int(w * 0.4), int(h * 0.06)), onClickFct = self.destroy)

		px = int(w * 0.86)
		py = int(h * 0.35)
		self.addSubWidget("joystickCommandText", Text, (px, py), "Manette", \
			anchor = (0, 0), fontSize = ms, font = f)
		py = int(h * 0.45)
		self.addSubWidget(("commandButton", "joystick", "right"), Button, \
			(px, py), text = getJoyKeyName(**jo["right"]), \
			size = (int(w * 0.18), int(h * 0.08)), \
			onClickFct = self.inputCommand, \
			onClickArgs = ("joystick", "right"), anchor = (0, 0), textKwargs = { \
			"fontSize": ls, "font": f})
		py = int(h * 0.55)
		self.addSubWidget(("commandButton", "joystick", "left"), Button, \
			(px, py), text = getJoyKeyName(**jo["left"]), \
			size = (int(w * 0.18), int(h * 0.08)), \
			onClickFct = self.inputCommand, onClickArgs = ("joystick", "left"), \
			anchor = (0, 0), textKwargs = {"fontSize": ls, "font": f})
		py = int(h * 0.65)
		self.addSubWidget(("commandButton", "joystick", "action"), Button, \
			(px, py), text = getJoyKeyName(**jo["action"]), \
			size = (int(w * 0.18), int(h * 0.08)), \
			onClickFct = self.inputCommand, \
			onClickArgs = ("joystick", "action"), anchor = (0, 0), textKwargs = { \
			"fontSize": ls, "font": f})
		py = int(h * 0.75)
		self.addSubWidget(("commandButton", "joystick", "pause"), Button, \
			(px, py), text = getJoyKeyName(**jo["pause"]), \
			size = (int(w * 0.18), int(h * 0.08)), \
			onClickFct = self.inputCommand, onClickArgs = ("joystick", "pause"), \
			anchor = (0, 0), textKwargs = {"fontSize": ls, "font": f})

		px = int(w * 0.95)
		py = int(h * 0.15)
		self.addSubWidget(("volumeSettingBar", "music"), Setting_bar, (px, py), \
			anchor = (1, 0), size = (int(w * 0.45), int(h * 0.05)), \
			cursorWidth = int(w * 0.03), lineThickness = int(h * 0.02), \
			value = mv)
		py = int(h * 0.25)
		self.addSubWidget(("volumeSettingBar", "sound"), Setting_bar, (px, py), \
			anchor = (1, 0), size = (int(w * 0.45), int(h * 0.05)), \
			cursorWidth = int(w * 0.03), lineThickness = int(h * 0.02), \
			value = sv)
		py = int(h * 0.85)
		self.addSubWidget("versionText", Text, (px, py), \
			"%s v%s" % (NAME, VERSION), font = f, fontSize = ls, anchor = (1, 0))

	def onEvent(self, event):
		"""
		Update subwidgets of this menu by passing to the given event.

		:type event: pygame.event.Event
		:param event: The pygame event to give to all subwidgets.
		"""

		Menu_widget.onEvent(self, event)
		if self.waitingInput:
			if self.waitingInput[0] == "keyboard":
				if event.type == KEYDOWN:
					self.configSubWidget(("commandButton", *self.waitingInput), \
						text=getKeyName(event.key), enable=True)
					self.setKeyboardOption(self.waitingInput[1], event.key)
					self.waitingInput = ()
			
			elif self.waitingInput[0] == "joystick":
				
				if event.type == JOYBUTTONDOWN:
					self.configSubWidget(("commandButton", *self.waitingInput), \
						text=getJoyKeyName(JOYBUTTONDOWN, \
						buttonId=event.button), enable=True)
					self.setJoystickOption(self.waitingInput[1], \
						inputType = JOYBUTTONDOWN, buttonId = event.button)
					self.waitingInput = ()
				
				elif event.type == JOYHATMOTION:
					self.configSubWidget(("commandButton", *self.waitingInput), \
						text=getJoyKeyName(JOYHATMOTION, hatId=event.hat, \
						value=round(event.value)), enable=True)
					self.setJoystickOption(self.waitingInput[1], \
						inputType=JOYHATMOTION, hatId=event.hat, \
						value = round(event.value))
					self.waitingInput = ()
				
				elif event.type == JOYAXISMOTION:
					self.configSubWidget(("commandButton", *self.waitingInput), \
						text = getJoyKeyName(JOYAXISMOTION, axisId=event.axis, \
						value=round(event.value)), enable=True)
					self.setJoystickOption(self.waitingInput[1], \
						inputType=JOYAXISMOTION, axisId=event.axis, \
						value=round(event.value))
					self.waitingInput = ()
				
				elif event.type == KEYDOWN:
					self.configSubWidget(("commandButton", *self.waitingInput), \
					enable=True)
					self.waitingInput = ()

	def setKeyboardOption(self, actionName, keyCode):
		"""
		Define a new key for a given action.

		:type actionName: str
		:param actionName: The name used to identify the associated action.

		:type keyCode: int
		:param keyCode: A key id.
		"""

		if "keyboard" not in Game.options:
			Game.options["keyboard"] = {}
		Game.options["keyboard"][actionName] = keyCode

	def setJoystickOption(self, actionName, **inputKwargs):
		"""
		Define a new controller button for a given action.

		:type actionName: str
		:param actionName: The name used to identify the associated action.

		Keyword arguments depend of the event type.
		"""

		if "joystick" not in Game.options:
			Game.options["joystick"] = {}
		Game.options["joystick"][actionName] = inputKwargs

	def update(self, deltaTime):
		"""
		Update the menu, its subwidgets and the sound volume.

		:type deltaTime: float
		:param deltaTime: Time elapsed since the last call of this method (in
			seconds).
		"""

		Menu_widget.update(self, deltaTime)

		if ("volumeSettingBar", "music") in self.subWidgets:
			Game.audioPlayer.musicVolume = \
				self.subWidgets["volumeSettingBar", "music"].getValue()
		if ("volumeSettingBar", "sound") in self.subWidgets:
			Game.audioPlayer.soundVolume = \
				self.subWidgets["volumeSettingBar", "sound"].getValue()

	def destroy(self):
		"""
		Destroy the menu and its subwidgets.
		"""

		if ("volumeSettingBar", "music") in self.subWidgets:
			Game.options["music volume"] = \
				self.subWidgets["volumeSettingBar", "music"].getValue()
		if ("volumeSettingBar", "sound") in self.subWidgets:
			Game.options["sound volume"] = \
				self.subWidgets["volumeSettingBar", "sound"].getValue()
		Menu_widget.destroy(self)
		self.quitFct()

	def inputCommand(self, inputTypeName, actionName):
		"""
		Start to record user event to configure the keyboard or a joystick.

		:type inputTypeName: str
		:param inputTypeName: It can be "keyboard" or "joystick".

		:type actionName: str
		:param actionName: The name used to identify the associated action.
		"""

		if not self.waitingInput:
			self.configSubWidget(("commandButton", inputTypeName, \
				actionName), enable=False)
			self.waitingInput = (inputTypeName, actionName)
