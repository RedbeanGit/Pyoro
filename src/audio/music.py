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

    def __init__(self, audio_player):
        """
        Initialize a Music object.

        :type audio_player: audio.audio_player.Audio_player
        :param audio_player: The player that will update this Music object.
        """

        Sound.__init__(self, audio_player)
        self.wave_file = None

    def load(self, file_path):
        """
        Open a wav file at the given path to load it during playback.

        :type file_path: str
        :param file_path: The path of the file to load
        """

        if os.path.exists(file_path):
            try:
                # Openning new stream
                self.wave_file = wave.open(file_path, "rb")
                self.file_path = file_path,
                self.framerate = self.wave_file.getframerate()
                self.nb_channels = self.wave_file.getnchannels()
                self.samples_width = self.wave_file.getsampwidth()
                self.is_loaded = True
            except Exception:
                print(f'[WARNING] [Music.load] Unable to load "{file_path}"')
        else:
            print(f'[WARNING] [Music.load] Unable to find "{file_path}"')

    def unload(self):
        """
        Clear the sound properties and audio data, and close the wave file.
        """

        if self.is_loaded and self.wave_file:
            self.wave_file.close()
            Sound.unload(self)
        else:
            print("[WARNING] [Music.unload] Music not loaded")

    def is_finished(self):
        """
        Return True if the playhead has arrived at the end,
        otherwise False.
        """
        if self.wave_file:
            return self.pos >= self.wave_file.getnframes()

    def set_pos(self, pos):
        """
        Set the playhead position.

        :type pos: int
        :param pos: The new position of the playback
        """
        if self.wave_file:
            self.wave_file.setpos(pos)
            self.pos = pos

    def get_frames(self, nb_frames):
        """
        Get a new audio chunk.

        :type nb_frames: int
        :param nb_frames: The size of the audio chunk to get

        :rtype: bytes
        :returns: A new raw audio chunk
        """

        if self.wave_file:
            nb_frames = int(nb_frames)
            chunk_size = int(nb_frames / self.nb_channels / self.samples_width)
            chunk = self.wave_file.readframes(chunk_size)
            self.pos = self.wave_file.tell()
            return chunk + bytes(nb_frames - len(chunk))

    def reset(self):
        """
        Set the playhead at the beginning.
        """

        if self.is_loaded and self.wave_file:
            self.wave_file.rewind()
        else:
            print("[WARNING] [Music.get_file_info] Music not loaded")

    def copy(self):
        """
        Create a new music with the same properties and audio data as this
        music.

        :rtype: audio.music.Music
        :returns: A new independant music.
        """

        msc = Music(self.audio_player)
        if self.is_loaded:
            msc.framerate = self.framerate
            msc.nb_channels = self.nb_channels
            msc.samples_width = self.samples_width
            msc.file_path = self.file_path
            msc.samples = self.samples
            msc.wave_file = self.wave_file
            msc.is_loaded = True

        return msc
