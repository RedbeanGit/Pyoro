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
Provide methods to play and manage sounds
and musics

Created on 27/08/2018
"""

import os
import pyaudio
import audioop
import threading

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from audio.sound import Sound
from audio.music import Music
from game.config import LOW_AUDIO
from game.util import getResourcePaths


class Audio_player:
	"""
	Play sounds and musics with a defined volume and speed.

	Actually, only sound files with 2 channels, a 44100Hz framerate
	and an audio format defined on 32bit can be played correctly! It will
	be updated in the future.
	"""

	defaultFramerate = 44100 # CD quality (22050 samples per second)

	def __init__(self, nbChannels=2, samplesWidth=2, chunkSize=1024):
		"""
		Initialize the Audio_player object.

		:type nbChannels: int
		:param nbChannels: Number of output channels (1=mono, 2=stereo).

		:type samplesWidth: int
		:param samplesWidth: Number of bytes per sample
			(1 = 8bits, 2 = 16bits, ...).

		:type chunkSize: int
		:param chunkSize: Number of samples per chunk.
		"""

		print("[INFO] [Audio_player.__init__] Opening audio stream")
		self.nbChannels = nbChannels
		self.samplesWidth = samplesWidth
		self.chunkSize = chunkSize
		self.framerate = Audio_player.defaultFramerate

		self.pyaudioInstance = pyaudio.PyAudio()
		self.stream = self.pyaudioInstance.open(
				format = self.pyaudioInstance.get_format_from_width(
					self.samplesWidth),
				rate = Audio_player.defaultFramerate,
				channels = self.nbChannels,
				output = True
			)

		self.sounds = {}
		self.musics = {}
		self.mixer = []

		self.soundVolume = 1
		self.musicVolume = 1

		self.active = False
		self.thread = None
		self.lock = threading.RLock()

	def loadAudio(self):
		"""
		Load the sounds and musics in the default audio data location.
		"""

		print("[INFO] [Audio_player.loadAudio] Loading sounds and musics")
		for soundPath in getResourcePaths("sounds"):
			self.loadSound(os.path.join("data", *soundPath))
		for musicPath in getResourcePaths("musics"):
			self.loadMusic(os.path.join("data", *musicPath))

	def loadSound(self, soundPath):
		"""
		Load a specific wav file as a Sound in a defined path.

		:type soundPath: str
		:param soundPath: The file path of the sound to load.
		"""

		snd = Sound(self)
		snd.load(soundPath)
		self.sounds[soundPath] = snd

	def loadMusic(self, musicPath):
		"""
		Load a specific wav file as a Music in a defined path.

		:type musicPath: str
		:param musicPath: The file path of the music to load.
		"""

		msc = Music(self)
		msc.load(musicPath)
		self.musics[musicPath] = msc

	def getSound(self, soundPath):
		"""
		Get a loaded sound. If the sound file at the given
		path is not loaded, return an empty sound.

		:type soundPath: str
		:param soundPath: The path of the sound file.

		:rtype: audio.sound.Sound
		:returns: A loaded sound.
		"""

		if soundPath in self.sounds:
			snd = self.sounds[soundPath].copy()
		else:
			print('[WARNING] [Audio_player.getSound] Unable to get ' \
				+ '"%s" ! Creating empty sound' % soundPath)
			snd = Sound(self)
			snd.filePath = soundPath
		self.sounds[soundPath, "copy", snd] = snd
		return snd

	def getMusic(self, musicPath):
		"""
		Get a loaded music. If the music file at the given
		path is not loaded, return an empty sound.

		:type musicPath: str
		:param musicPath: The path of the music file.

		:rtype: audio.music.Music
		:returns: A loaded music or empty sound.
		"""

		if musicPath in self.musics:
			return self.musics[musicPath]
		print('[WARNING] [Audio_player.getMusic] Unable to get ' \
			+ '"%s" ! Creating empty sound' % musicPath)
		snd = Sound(self)
		snd.filePath = musicPath
		return snd

	def removeSound(self, sound):
		"""
		Remove a sound from the sound list.

		:type sound: audio.sound.Sound
		:param sound: The sound to remove.
		"""

		if (sound.filePath, "copy", sound) in self.sounds:
			self.sounds.pop((sound.filePath, "copy", sound))

	def removeMusic(self, music):
		"""
		Remove a music from the music list.

		:type music: audio.music.Music
		:param music: The music to remove.
		"""

		if music.filePath in self.musics:
			self.musics.pop(music.filePath)

	def isPlayable(self, sound):
		"""
		Check if the sound can be played by this Audio_player.

		:type sound: audio.sound.Sound
		:param sound: The sound to check.

		:rtype: bool
		:returns: True if the sound is playable, otherwise False.
		"""

		return sound.samplesWidth == self.samplesWidth \
			and sound.nbChannels == self.nbChannels

	def start(self):
		"""
		Start the audio player in a new thread.
		"""

		def loop():
			while self.active:
				if LOW_AUDIO:
					self.updateLow()
				else:
					self.update()

		self.active = True
		self.thread = threading.Thread(target = loop)
		self.thread.start()
		print("[INFO] [Audio_player.start] Player started in a new thread")

	def stop(self):
		"""
		Stop the audio player if started.
		"""

		if self.active:
			print("[INFO] [Audio_player.stop] Stopping player")
			self.active = False
			self.thread.join()
		else:
			print("[WARNING] [Audio_player.stop] Audio_player already stopped")

	def isMusic(self, sound):
		"""
		Return True if the given sound is a Music instance.

		:type sound: audio.sound.Sound
		:param sound: The sound to check.

		:rtype: bool
		:returns: True if the sound is a music, otherwise False.
		"""
		return isinstance(sound, Music)

	def update(self):
		"""
		Update sounds and music and play a new audio sample.
		"""

		with self.lock:
			framerate = int(self.framerate)
			chunks = bytes()
			for sound in self.mixer:
				if sound.isPlaying and self.isPlayable(sound):
					if self.isMusic(sound):
						volume = self.musicVolume
					else:
						volume = self.soundVolume

					chunk = sound.setChunkFramerate(
						sound.setChunkVolume(
							sound.update(),
							volume * sound.volume),
						framerate)
					if chunks:
						chunks = audioop.add(chunks, chunk, self.samplesWidth)
					else:
						chunks = chunk
			if chunks:
				self.stream.write(chunks)

	def updateLow(self):
		"""
		Update sounds and music and play a new audio samples but use less
		resources than Audio_player.update() method.
		"""

		with self.lock:
			framerate = int(self.framerate)
			chunks = bytes(self.chunkSize * self.samplesWidth * self.nbChannels // 2)

			for sound in self.mixer:
				if sound.isPlaying and self.isPlayable(sound):
					if self.isMusic(sound):
						volume = self.musicVolume
					else:
						volume = self.soundVolume

					chunk = sound.setChunkVolume(sound.update(), volume \
						* sound.volume)
					chunks = audioop.add(chunks, chunk, self.samplesWidth)
			chunks = audioop.ratecv(chunks, self.samplesWidth, self.nbChannels, \
				Audio_player.defaultFramerate, framerate * 2, None)[0]
			self.stream.write(chunks)


	def getMusicInMixer(self):
		"""
		Get all musics in the mixer.

		:rtype: list
		:returns: A list of audio.music.Music.
		"""

		return [music for music in self.mixer if isinstance(music, Music)]

	def getSoundInMixer(self):
		"""
		Get all sounds in the mixer.

		:rtype: list
		:returns: A list of audio.sound.Sound.
		"""

		return [sound for sound in self.mixer if not isinstance(sound, Music)]

	def stopAudio(self):
		"""
		Stop all sounds and musics in the mixer.
		"""

		for sound in self.mixer:
			sound.stop()
		self.mixer.clear()

	def pauseAudio(self):
		"""
		Pause all sounds and musics in the mixer.
		"""

		for sound in self.mixer:
			sound.pause()

	def unpauseAudio(self):
		"""
		Unpause sounds and musics in the mixer.
		"""

		for sound in self.mixer:
			sound.play()

	def setSpeed(self, speed):
		"""
		Set the reading speed of the audio player.

		:type speed: float
		:param speed: The speed of the audio player (default is 1)
		"""
		self.framerate = Audio_player.defaultFramerate / speed

	def getSpeed(self):
		"""
		Get the current reading speed of the audio player.

		:rtype: float
		:returns: The current speed of the audio player (-1 if the default
			framerate is 0).
		"""

		if Audio_player.defaultFramerate != 0:
			return Audio_player.defaultFramerate / self.framerate
		return -1
