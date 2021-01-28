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
Provides a Music class for loading and managing musics.
Ideal for large audio files. For more reactivity, it's better
to use audio.sound.Sound.

Created on 27/08/2018
"""

import os
import wave

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from audio.sound import Sound


class Music(Sound):
	"""
	Made for loading and playing large audio files.
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
		"""
		Create a new music with the same properties and audio data as this
		music.

		:rtype: audio.music.Music
		:returns: A new independant music.
		"""

		msc = Music(self.ap)
		if self.isLoaded:
			msc.framerate = self.framerate
			msc.nbChannels = self.nbChannels
			msc.samplesWidth = self.samplesWidth
			msc.filePath = self.filePath
			msc.samples = self.samples
			msc.waveFile = self.waveFile
			msc.isLoaded = True

		return msc