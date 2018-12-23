# -*- coding: utf-8 -*-

"""
Provides a Sound class for loading and managing sounds.
Ideal for small audio files. For larger files, it's better
to use audio.music.Music.

Created on 23/08/2018
"""

__author__ = "Julien Dubois"
__version__ = "1.1.2"

import audioop
import os
import wave


class Sound:
	"""
	Made for loading and playing small audio files by loading
	them completly in the RAM.
	"""

	def __init__(self, audioPlayer):
		"""
		Initialize a Sound object.

		:type audioPlayer: audio.audio_player.Audio_player
		:param audioPlayer: The player that will update this Sound object.
		"""

		self.ap = audioPlayer
		self.samples = bytes()

		self.isLoaded = False
		self.isPlaying = False

		self.filePath = ""
		self.framerate = 0
		self.nbChannels = 0
		self.samplesWidth = 0

		self.pos = 0
		self.loop = 1
		self.volume = 1

	def load(self, filePath):
		"""
		Loads a sound from a wav file at the given path.

		:type filePath: str
		:param filePath: The path of the file to load.
		"""

		if os.path.exists(filePath):
			try:
				with wave.open(filePath, "rb") as wf:
					self.filePath = filePath
					self.framerate = wf.getframerate()
					self.nbChannels = wf.getnchannels()
					self.samplesWidth = wf.getsampwidth()
					
					# Loading sounds samples
					self.samples = wf.readframes(wf.getnframes() - 1)
					self.isLoaded = True

			except Exception:
				print('[WARNING] [Sound.load] Unable to load "%s"' % filePath)
		else:
			print('[WARNING] [Sound.load] Unable to find "%s"' % filePath)

	def unload(self):
		"""
		Clear the sound properties and audio data.
		"""

		if self.isLoaded:
			self.filePath = ""
			self.framerate = 0
			self.nbChannels = 0
			self.samplesWidth = 0
			self.samples = bytes()
			self.isLoaded = False
		else:
			print("[WARNING] [Sound.unload] Sound not loaded")

	def play(self, loop = None):
		"""
		Make the sound be playable by the audio player.

		:type loop: int
		:param loop: The number of times to play the sound.
		"""

		if self.isLoaded:
			self.loop = loop if loop else self.loop
			self.isPlaying = True
			if self not in self.ap.mixer:
				self.ap.mixer.append(self)
		else:
			print("[WARNING] [Sound.play] Sound not loaded")

	def pause(self):
		"""
		Prevent the audio player to continue to play this sound.
		"""

		if self.isLoaded:
			self.isPlaying = False
		else:
			print("[WARNING] [Sound.stop] Sound not loaded")

	def stop(self):
		"""
		Prevent the audio player to play this sound and reset it.
		"""

		if self.isLoaded:
			if self.isPlaying:
				self.isPlaying = False
				if self in self.ap.mixer:
					self.ap.mixer.remove(self)
				self.reset()
				self.loop = 1
			else:
				print('[WARNING] [Sound.stop] Sound "%s" ' % self.filePath \
					+ 'not currently playing')
		else:
			print("[WARNING] [Sound.stop] Sound not loaded")

	def update(self):
		"""
		Update the sound by playing a new audio chunk.

		:rtype: bytes
		:returns: Raw audio data.
		"""

		if self.isLoaded:
			if self.isPlaying:
				if self.isFinished():
					self.endLoop()
					if self.isPlaying:
						return self.getFrames(self.getChunkSize())
					return bytes(self.getChunkSize())

				chunk = self.getFrames(self.getChunkSize())
				return chunk
			else:
				print('[WARNING] [Sound.update] Sound "%s" ' % self.filePath \
					+ 'not currently playing')
		else:
			print("[WARNING] [Sound.update] Sound not loaded")

	def endLoop(self):
		"""
		Decrement the loop count and reset the sound if necessary.
		"""

		self.loop -= 1
		if self.loop == 0:
			self.stop()
		else:
			self.reset()

	def isFinished(self):
		"""
		Return True if the playhead has arrived at the end,
		otherwise False.

		:rtype: bool
		:returns: True if the playback has been arrived at the end,
			otherwise False.
		"""

		return self.pos >= len(self.samples)

	def setPos(self, pos):
		"""
		Set the playhead position.

		:type pos: int
		:param pos: The new position of the playback
		"""

		if pos >= 0 and pos < len(self.samples):
			self.pos = pos
		else:
			print("[WARNING] [Sound.setPos] Position (defined to " \
				+ "%s) must be between 0 and %s" % (pos, len(self.samples)))

	def getFrames(self, nbFrames):
		"""
		Get a new audio chunk.

		:type nbFrames: int
		:param nbFrames: The size of the audio chunk to get

		:rtype: bytes
		:returns: A new raw audio chunk
		"""

		dataLength = len(self.samples)
		if self.pos < dataLength:
			chunk = self.samples[self.pos : self.pos+nbFrames]

			# If playback head reached the end
			# add some empty bytes to get a chunk of nbFrames size
			if self.pos + nbFrames >= dataLength:
				self.pos = dataLength
				chunk += bytes(nbFrames - len(chunk))
			else:
				self.pos += nbFrames
			return chunk
		return bytes(nbFrames)

	def setChunkVolume(self, chunk, volume):
		"""
		Modify a raw data chunk to change the audio volume.

		:type chunk: bytes
		:param chunk: The chunk to modify.

		:type volume: float
		:param volume: A floating point value between 0 and 1.

		:rtype: bytes
		:returns: A modified audio chunk.
		"""

		if self.isLoaded:
			return audioop.mul(chunk, 
				self.samplesWidth,
				volume)
		else:
			print("[WARNING] [Sound.setChunkVolume] Sound not loaded")
			return chunk

	def setChunkFramerate(self, chunk, framerate):
		"""
		Modify the framerate of an audio chunk.

		:type chunk: bytes
		:param chunk: The chunk to modify.

		:type framerate: int
		:param framerate: The new framerate to set.

		:rtype: bytes
		:returns: A modified audio chunk.
		"""

		if self.isLoaded:
			return audioop.ratecv(
				chunk,
				self.samplesWidth,
				self.nbChannels,
				self.framerate,
				framerate,
				None
			)[0]
		else:
			print("[WARNING] [Sound.setChunkFramerate] Sound not loaded")
			return chunk

	def reset(self):
		"""
		Set the playhead at the beginning.
		"""
		self.pos = 0

	def getChunkSize(self):
		"""
		Get a the size of an audio chunk according to the number of channels,
		the width of each samples and the number of samples per chunk.

		:rtype: int
		:returns: The size of an audio chunk in bytes.
		"""

		if self.isLoaded:
			return int(self.ap.chunkSize \
				* self.nbChannels \
				* self.samplesWidth \
				* self.framerate \
				/ self.ap.defaultFramerate)
		else:
			print("[WARNING] [Sound.getChunkSize] Sound not loaded")
			return 0

	def copy(self):
		"""
		Create a new sound with the same properties and audio data as this
		sound.

		:rtype: audio.sound.Sound
		:returns: A new independant sound.
		"""

		snd = Sound(self.ap)
		if self.isLoaded:
			snd.framerate = self.framerate
			snd.nbChannels = self.nbChannels
			snd.samplesWidth = self.samplesWidth
			snd.filePath = self.filePath
			snd.samples = self.samples
			snd.isLoaded = True
		return snd