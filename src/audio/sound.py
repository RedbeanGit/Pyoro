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
Provides a Sound class for loading and managing sounds.
Ideal for small audio files. For larger files, it's better
to use audio.music.Music.

Created on 23/08/2018
"""

import audioop
import os
import wave

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


class Sound:
    """
    Made for loading and playing small audio files by loading
    them completly in memory.
    """

    def __init__(self, audio_player):
        """
        Initialize a Sound object.

        :type audio_player: audio.audio_player.Audio_player
        :param audio_player: The player that will update this Sound object.
        """

        self.audio_player = audio_player
        self.samples = bytes()

        self.is_loaded = False
        self.is_playing = False

        self.file_path = ""
        self.framerate = 0
        self.nb_channels = 0
        self.samples_width = 0

        self.pos = 0
        self.loop = 1
        self.volume = 1

    def load(self, file_path):
        """
        Loads a sound from a wav file at the given path.

        :type file_path: str
        :param file_path: The path of the file to load.
        """

        if os.path.exists(file_path):
            try:
                with wave.open(file_path, "rb") as wave_file:
                    self.file_path = file_path
                    self.framerate = wave_file.getframerate()
                    self.nb_channels = wave_file.getnchannels()
                    self.samples_width = wave_file.getsampwidth()

                    # Loading sounds samples
                    self.samples = wave_file.readframes(
                        wave_file.getnframes() - 1)
                    self.is_loaded = True

            except Exception:
                print(f'[WARNING] [Sound.load] Unable to load "{file_path}"')
        else:
            print(f'[WARNING] [Sound.load] Unable to find "{file_path}"')

    def unload(self):
        """
        Clear the sound properties and audio data.
        """

        if self.is_loaded:
            self.file_path = ""
            self.framerate = 0
            self.nb_channels = 0
            self.samples_width = 0
            self.samples = bytes()
            self.is_loaded = False
        else:
            print("[WARNING] [Sound.unload] Sound not loaded")

    def play(self, loop=None):
        """
        Make the sound be playable by the audio player.

        :type loop: int
        :param loop: The number of times to play the sound.
        """

        if self.is_loaded:
            self.loop = loop if loop else self.loop
            self.is_playing = True
            if self not in self.audio_player.mixer:
                self.audio_player.mixer.append(self)
        else:
            print("[WARNING] [Sound.play] Sound not loaded")

    def pause(self):
        """
        Prevent the audio player to continue to play this sound.
        """

        if self.is_loaded:
            self.is_playing = False
        else:
            print("[WARNING] [Sound.stop] Sound not loaded")

    def stop(self):
        """
        Prevent the audio player to play this sound and reset it.
        """

        if self.is_loaded:
            if self.is_playing:
                self.is_playing = False
                if self in self.audio_player.mixer:
                    self.audio_player.mixer.remove(self)
                self.reset()
                self.loop = 1
            else:
                print(
                    f'[WARNING] [Sound.stop] Sound "{self.file_path}" not currently playing')
        else:
            print("[WARNING] [Sound.stop] Sound not loaded")

    def update(self):
        """
        Update the sound by playing a new audio chunk.

        :rtype: bytes
        :returns: Raw audio data.
        """

        if self.is_loaded:
            if self.is_playing:
                if self.is_finished():
                    self.end_loop()
                    if self.is_playing:
                        return self.get_frames(self.get_chunk_size())
                    return bytes(self.get_chunk_size())

                chunk = self.get_frames(self.get_chunk_size())
                return chunk
            else:
                print(
                    f'[WARNING] [Sound.update] Sound "{self.file_path}" not currently playing')
        else:
            print("[WARNING] [Sound.update] Sound not loaded")

    def end_loop(self):
        """
        Decrement the loop count and reset the sound if necessary.
        """

        self.loop -= 1
        if self.loop == 0:
            self.stop()
        else:
            self.reset()

    def is_finished(self):
        """
        Return True if the playhead has arrived at the end,
        otherwise False.

        :rtype: bool
        :returns: True if the playback has been arrived at the end,
            otherwise False.
        """

        return self.pos >= len(self.samples)

    def set_pos(self, pos):
        """
        Set the playhead position.

        :type pos: int
        :param pos: The new position of the playback
        """

        if 0 <= pos < len(self.samples):
            self.pos = pos
        else:
            print('[WARNING] [Sound.setPos] Position (defined to ' +
                  f'{pos}) must be between 0 and {self.samples}')

    def get_frames(self, nb_frames):
        """
        Get a new audio chunk.

        :type nb_frames: int
        :param nb_frames: The size of the audio chunk to get

        :rtype: bytes
        :returns: A new raw audio chunk
        """

        data_length = len(self.samples)
        if self.pos < data_length:
            chunk = self.samples[self.pos: self.pos+nb_frames]

            # If playback head reached the end
            # add some empty bytes to get a chunk of nb_frames size
            if self.pos + nb_frames >= data_length:
                self.pos = data_length
                chunk += bytes(nb_frames - len(chunk))
            else:
                self.pos += nb_frames
            return chunk
        return bytes(nb_frames)

    def set_chunk_volume(self, chunk, volume):
        """
        Modify a raw data chunk to change the audio volume.

        :type chunk: bytes
        :param chunk: The chunk to modify.

        :type volume: float
        :param volume: A floating point value between 0 and 1.

        :rtype: bytes
        :returns: A modified audio chunk.
        """

        if self.is_loaded:
            return audioop.mul(chunk,
                               self.samples_width,
                               volume)
        else:
            print("[WARNING] [Sound.setChunkVolume] Sound not loaded")
            return chunk

    def set_chunk_framerate(self, chunk, framerate):
        """
        Modify the framerate of an audio chunk.

        :type chunk: bytes
        :param chunk: The chunk to modify.

        :type framerate: int
        :param framerate: The new framerate to set.

        :rtype: bytes
        :returns: A modified audio chunk.
        """

        if self.is_loaded:
            return audioop.ratecv(
                chunk,
                self.samples_width,
                self.nb_channels,
                self.framerate,
                framerate,
                None
            )[0]
        print("[WARNING] [Sound.setChunkFramerate] Sound not loaded")
        return chunk

    def reset(self):
        """
        Set the playhead at the beginning.
        """
        self.pos = 0

    def get_chunk_size(self):
        """
        Get a the size of an audio chunk according to the number of channels,
        the width of each samples and the number of samples per chunk.

        :rtype: int
        :returns: The size of an audio chunk in bytes.
        """

        if self.is_loaded:
            return int(self.audio_player.chunk_size
                       * self.nb_channels
                       * self.samples_width
                       * self.framerate
                       / self.audio_player.default_framerate)
        print("[WARNING] [Sound.get_chunk_size] Sound not loaded")
        return 0

    def copy(self):
        """
        Create a new sound with the same properties and audio data as this
        sound.

        :rtype: audio.sound.Sound
        :returns: A new independant sound.
        """

        snd = Sound(self.audio_player)
        if self.is_loaded:
            snd.framerate = self.framerate
            snd.nb_channels = self.nb_channels
            snd.samples_width = self.samples_width
            snd.file_path = self.file_path
            snd.samples = self.samples
            snd.is_loaded = True
        return snd
