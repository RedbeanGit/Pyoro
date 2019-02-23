# -*- coding: utf-8 -*-

"""
Provide high level widgets based on lemapi widgets for Pyoro.

Created on 19/01/2019
"""

from game.config import GUI_IMAGE_PATH, NAME, VERSION
from game.util import reset

__author__ = "Julien Dubois"
__version__ = "2.0.0"

from os.path import join
from lemapi.event_manager import Event
from lemapi.widget import Button, Menu_widget, Text, Setting_bar, Clickable_text


class Play_button(Button):

	DEFAULT_KWARGS = {
		"textAnchor": (0, -0.05),
		"backgroundImage": join(GUI_IMAGE_PATH, "play button {}", \
			"play_button.png"),
		"onHoverBackgroundImage": join(GUI_IMAGE_PATH, "play button {}", \
			"play_button_hover.png"),
		"onClickBackgroundImage": join(GUI_IMAGE_PATH, "play button {}", \
			"play_button_click.png"),
		"onMiddleClickBackgroundImage": join(GUI_IMAGE_PATH, "play button {}", \
			"play_button_middle_click.png"),
		"onRightClickBackgroundImage": join(GUI_IMAGE_PATH, "play button {}", \
			"play_button_right_click.png"),
		"disableBackgroundImage": join(GUI_IMAGE_PATH, "play button {}", \
			"play_button_disable.png")
	}

	def __init__(self, gui, pos, gameId, **kwargs):
		Play_button.updateDefaultKwargs(kwargs)
		self.gameId = gameId
		super().__init__(gui, pos, **kwargs)

	def loadBackgroundImages(self):
		backNames = ("backgroundImage", "onHoverBackgroundImage", \
			"onClickBackgroundImage", "onMiddleClickBackgroundImage", \
			"onRightClickBackgroundImage", "disableBackgroundImage")
		for backName in backNames:
			if self.kwargs[backName]:
				if "{}" in self.kwargs[backName]:
					self.kwargs[backName] = self.kwargs[backName].format( \
					self.gameId + 1)
		super().loadBackgroundImages()


class Option_menu(Menu_widget):

	DEFAULT_KWARGS = {
		"font": join(GUI_IMAGE_PATH, "font.ttf"),
		"fontSize": 20,
		"backgroundBorderSize": 5
	}

	def __init__(self, gui, pos, destroyFct, soundFct, soundVolumes, **kwargs):
		Option_menu.updateDefaultKwargs(kwargs)
		self.destroyFct = destroyFct
		self.soundFct = soundFct
		self.soundVolumes = soundVolumes
		super().__init__(gui, pos, **kwargs)
		self.initEvents()

	def initWidgets(self):
		rp = self.getRealPos()
		sv, mv = self.soundVolumes
		f = self.kwargs["font"]
		w, h = self.kwargs["size"]
		ts = self.kwargs["fontSize"]; ms = ts - 3; ls = ms - 3

		px = int(w * 0.05)
		py = int(h * 0.15)
		self.addSubWidget("music_volume_text", Text, (px, py), \
			"Volume de la musique", anchor=(-1, 0), fontSize=ms, font=f)
		py = int(h * 0.25)
		self.addSubWidget("sound_volume_text", Text, (px, py), \
			"Volume des sons", anchor=(-1, 0), fontSize=ms, font=f)

		px = int(w * 0.25)
		py = int(h * 0.95)
		self.addSubWidget("reset_button", Button, (px, py), \
			text="Réinitialiser", anchor=(0, 0), textKwargs={"fontSize": ms, \
			"font": f}, size=(int(w * 0.4), int(h * 0.06)))

		px = int(w * 0.5)
		py = int(h * 0.05)
		self.addSubWidget("title_text", Text, (px, py), "Options", \
			anchor=(0, -1), fontSize=ts, font=f)

		px = int(w * 0.75)
		py = int(h * 0.95)
		self.addSubWidget("back_button", Button, (px, py), text="Retour", \
			anchor=(0, 0), textKwargs={"fontSize": ms, "font": f}, \
			size=(int(w * 0.4), int(h * 0.06)))

		px = int(w * 0.95)
		py = int(h * 0.15)
		self.addSubWidget("music_volume_setting_bar", Setting_bar, (px, py), \
			anchor=(1, 0), size=(int(w * 0.45), int(h * 0.05)), \
			cursorWidth=int(w * 0.03), lineThickness=int(h * 0.02), value=mv)
		py = int(h * 0.25)
		self.addSubWidget("sound_volume_setting_bar", Setting_bar, (px, py), \
			anchor=(1, 0), size=(int(w * 0.45), int(h * 0.05)), \
			cursorWidth=int(w * 0.03), lineThickness=int(h * 0.02), value=sv)
		py = int(h * 0.85)
		self.addSubWidget("version_text", Text, (px, py), \
			"%s v%s" % (NAME, VERSION), font=f, fontSize=ls, anchor=(1, 0))

	def initEvents(self):
		event = Event(reset)
		self.subWidgets["reset_button"].endClickEvents.append(event)
		event = Event(self.destroyFct)
		self.subWidgets["back_button"].endClickEvents.append(event)

	def update(self):
		mv = self.subWidgets["music_volume_setting_bar"].getValue()
		sv = self.subWidgets["sound_volume_setting_bar"].getValue()
		self.soundFct(sv, mv)
		super().update()


class Pause_menu(Menu_widget):
	"""
	A menu to display when the game is paused.
	"""

	DEFAULT_KWARGS = {
		"fontSize": 20,
		"font": join(GUI_IMAGE_PATH, "font.ttf"),
		"backgroundBorderSize": 5
	}

	def __init__(self, gui, pos, resumeFct, quitFct, optionFct, **kwargs):
		"""
		Initialize a new Pause_menu object.

		:type activity: gui.activity.Activity
		:param activity: The parent activity of this widget.

		:type pos: tuple
		:param pos: The position of the widget in a (x, y) tuple where x and y
			are integers.

		:type resumeFct: callable
		:param resumeFct: A function, class or method which can be called on click
			on the "resume" button.

		:type quitFct: callable
		:param quitFct: A function, class or method which can be called on click
			on the "quit" button.
		"""

		Pause_menu.updateDefaultKwargs(kwargs)
		self.resumeFct = resumeFct
		self.quitFct = quitFct
		self.optionFct = optionFct
		super().__init__(gui, pos, **kwargs)
		self.initEvents()

	def initWidgets(self):
		"""
		Create widgets displayed in this dialog.
		"""

		realPos = self.getRealPos()
		w, h = self.kwargs["size"]
		f = self.kwargs["font"]
		ts = self.kwargs["fontSize"]; ms = ts - 3

		px = int(w * 0.5)
		py = int(h * 0.2)
		self.addSubWidget("title_text", Text, (px, py), "Pause", anchor=(0, 0), \
			font=f, fontSize=ts)
		py = int(h * 0.4)
		self.addSubWidget("resume_clickable_text", Clickable_text, (px, py), \
			"continuer", anchor=(0, 0), font=f, fontSize=ms)
		py = int(h * 0.6)
		self.addSubWidget("option_clickable_text", Clickable_text, (px, py), \
			"options", anchor=(0, 0), font=f, fontSize=ms)
		py = int(h * 0.8)
		self.addSubWidget("quit_clickable_text", Clickable_text, (px, py), \
			"quitter", anchor=(0, 0), font=f, fontSize=ms)

	def initEvents(self):
		event = Event(self.resumeFct)
		self.subWidgets["resume_clickable_text"].endClickEvents.append(event)
		event = Event(self.optionFct)
		self.subWidgets["option_clickable_text"].endClickEvents.append(event)
		event = Event(self.quitFct)
		self.subWidgets["quit_clickable_text"].endClickEvents.append(event)


class Game_over_menu(Menu_widget):

	DEFAULT_KWARGS = {
		"fontSize": 20,
		"font": join(GUI_IMAGE_PATH, "font.ttf"),
		"backgroundBorderSize": 5
	}

	def __init__(self, gui, pos, quitFct, score, **kwargs):
		Game_over_menu.updateDefaultKwargs(kwargs)
		self.quitFct = quitFct
		self.score = score
		super().__init__(gui, pos, **kwargs)
		self.initEvents()

	def initWidgets(self):
		realPos = self.getRealPos()
		w, h = self.kwargs["size"]
		f = self.kwargs["font"]
		ts = self.kwargs["fontSize"]; ms = ts - 3

		px = int(w * 0.5)
		py = int(h * 0.25)
		self.addSubWidget("title_text", Text, (px, py), "Game Over", \
			anchor=(0, 0), font=f, fontSize=ts)
		py = int(h * 0.50)
		self.addSubWidget("score_text", Text, (px, py), \
			"score : %s" % self.score, anchor=(0, 0), font=f, fontSize=ms)
		py = int(h * 0.75)
		self.addSubWidget("quit_clickable_text", Clickable_text, (px, py), \
			"quitter", anchor=(0, 0), font=f, fontSize=ms)

	def initEvents(self):
		event = Event(self.quitFct)
		self.subWidgets["quit_clickable_text"].endClickEvents.append(event)
