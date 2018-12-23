# -*- coding: utf-8 -*-

"""
Provides a Music class for loading and managing musics.
Ideal for large audio files. For more reactivity, it's better
to use audio.sound.Sound.

Created on 27/08/2018
"""

from audio.sound import Sound

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import os
import wave


class Music(Sound):
	"""
	Made for loading and playing large audio files
	"""

	def __init__(self, audioPlayer):
		"""
		Initialize a Music object.

		:type audioPlayer: audio.audio_player.Audio_player
		:param audioPlayer: The player that will update this Music object.
		"""

		Sound.__init__(self, audioPlayer)
		self.waveFile = None

	def load(self, filePath):
		"""
		Open a wav file at the given path to load it during playback.

		:type filePath: str
		:param filePath: The path of the file to load
		"""

		if os.path.exists(filePath):
			try:
				# Openning new stream
				self.waveFile = wave.open(filePath, "rb")
				self.filePath = filePath,
				self.framerate = self.waveFile.getframerate()
				self.nbChannels = self.waveFile.getnchannels()
				self.samplesWidth = self.waveFile.getsampwidth()
				self.isLoaded = True
			except Exception:
				print('[WARNING] [Music.load] Unable to load "%s"' % filePath)
		else:
			print('[WARNING] [Music.load] Unable to find "%s"' % filePath)

	def unload(self):
		"""
		Clear the sound properties and audio data, and close the wave file.
		"""

		if self.isLoaded:
			self.waveFile.close()
			Sound.unload(self)
		else:
			print("[WARNING] [Music.unload] Music not loaded")

	def isFinished(self):
		"""
		Return True if the playhead has arrived at the end,
		otherwise False.
		"""
		return self.pos >= self.waveFile.getnframes()

	def setPos(self, pos):
		"""
		Set the playhead position.

		:type pos: int
		:param pos: The new position of the playback
		"""
		self.waveFile.setpos(pos)
		self.pos = pos

	def getFrames(self, nbFrames):
		"""
		Get a new audio chunk.

		:type nbFrames: int
		:param nbFrames: The size of the audio chunk to get

		:rtype: bytes
		:returns: A new raw audio chunk
		"""

		nbFrames = int(nbFrames)
		chunkSize = int(nbFrames / self.nbChannels / self.samplesWidth)
		chunk = self.waveFile.readframes(chunkSize)
		self.pos = self.waveFile.tell()
		return chunk + bytes(nbFrames - len(chunk))

	def reset(self):
		"""
		Set the playhead at the beginning.
		"""

		if self.isLoaded:
			self.waveFile.rewind()
		else:
			print("[WARNING] [Music.getFileInfo] Music not loaded")

	def copy(self):
		snd = Sound.copy(self)
		if self.isLoaded:
			snd.waveFile = self.waveFile
		return snd