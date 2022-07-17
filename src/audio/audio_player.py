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
import audioop
import threading
import pyaudio

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from audio.sound import Sound
from audio.music import Music
from game.config import LOW_AUDIO
from game.util import get_resource_path


class AudioPlayer:
    """
    Play sounds and musics with a defined volume and speed.

    Actually, only sound files with 2 channels, a 44100Hz framerate
    and an audio format defined on 32bit can be played correctly! It will
    be updated in the future.
    """

    default_framerate = 44100  # CD quality (22050 samples per second)

    def __init__(self, nb_channels=2, samples_width=2, chunk_size=1024):
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
        self.nb_channels = nb_channels
        self.samples_width = samples_width
        self.chunk_size = chunk_size
        self.framerate = AudioPlayer.default_framerate

        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = self.pyaudio_instance.open(
            format=self.pyaudio_instance.get_format_from_width(
                self.samples_width),
            rate=AudioPlayer.default_framerate,
            channels=self.nb_channels,
            output=True
        )

        self.sounds = {}
        self.musics = {}
        self.mixer = []

        self.sound_volume = 1
        self.music_volume = 1

        self.active = False
        self.thread = None
        self.lock = threading.RLock()

    def load_audio(self):
        """
        Load the sounds and musics in the default audio data location.
        """

        print("[INFO] [Audio_player.loadAudio] Loading sounds and musics")
        for sound_path in get_resource_path("sounds"):
            self.load_sound(os.path.join("data", *sound_path))
        for music_path in get_resource_path("musics"):
            self.load_music(os.path.join("data", *music_path))

    def load_sound(self, sound_path):
        """
        Load a specific wav file as a Sound in a defined path.

        :type soundPath: str
        :param soundPath: The file path of the sound to load.
        """

        snd = Sound(self)
        snd.load(sound_path)
        self.sounds[sound_path] = snd

    def load_music(self, music_path):
        """
        Load a specific wav file as a Music in a defined path.

        :type musicPath: str
        :param musicPath: The file path of the music to load.
        """

        msc = Music(self)
        msc.load(music_path)
        self.musics[music_path] = msc

    def get_sound(self, sound_path):
        """
        Get a loaded sound. If the sound file at the given
        path is not loaded, return an empty sound.

        :type soundPath: str
        :param soundPath: The path of the sound file.

        :rtype: audio.sound.Sound
        :returns: A loaded sound.
        """

        if sound_path in self.sounds:
            snd = self.sounds[sound_path].copy()
        else:
            print('[WARNING] [Audio_player.getSound] Unable to get '
                  + f'"{sound_path}" ! Creating empty sound')
            snd = Sound(self)
            snd.file_path = sound_path
        self.sounds[sound_path, "copy", snd] = snd
        return snd

    def get_music(self, music_path):
        """
        Get a loaded music. If the music file at the given
        path is not loaded, return an empty sound.

        :type musicPath: str
        :param musicPath: The path of the music file.

        :rtype: audio.music.Music
        :returns: A loaded music or empty sound.
        """

        if music_path in self.musics:
            return self.musics[music_path]
        print('[WARNING] [Audio_player.getMusic] Unable to get '
              + f'"{music_path}" ! Creating empty sound')
        snd = Sound(self)
        snd.file_path = music_path
        return snd

    def remove_sound(self, sound):
        """
        Remove a sound from the sound list.

        :type sound: audio.sound.Sound
        :param sound: The sound to remove.
        """

        if (sound.file_path, "copy", sound) in self.sounds:
            self.sounds.pop((sound.file_path, "copy", sound))

    def remove_music(self, music):
        """
        Remove a music from the music list.

        :type music: audio.music.Music
        :param music: The music to remove.
        """

        if music.file_path in self.musics:
            self.musics.pop(music.file_path)

    def is_playable(self, sound):
        """
        Check if the sound can be played by this Audio_player.

        :type sound: audio.sound.Sound
        :param sound: The sound to check.

        :rtype: bool
        :returns: True if the sound is playable, otherwise False.
        """

        return sound.samples_width == self.samples_width \
            and sound.nb_channels == self.nb_channels

    def start(self):
        """
        Start the audio player in a new thread.
        """

        def loop():
            while self.active:
                if LOW_AUDIO:
                    self.update_low()
                else:
                    self.update()

        self.active = True
        self.thread = threading.Thread(target=loop)
        self.thread.start()
        print("[INFO] [Audio_player.start] Player started in a new thread")

    def stop(self):
        """
        Stop the audio player if started.
        """

        if self.active and self.thread:
            print("[INFO] [Audio_player.stop] Stopping player")
            self.active = False
            self.thread.join()
        else:
            print("[WARNING] [Audio_player.stop] Audio_player already stopped")

    def is_music(self, sound):
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
                if sound.is_playing and self.is_playable(sound):
                    if self.is_music(sound):
                        volume = self.music_volume
                    else:
                        volume = self.sound_volume

                    chunk = sound.set_chunk_framerate(
                        sound.set_chunk_volume(
                            sound.update(),
                            volume * sound.volume),
                        framerate)
                    if chunks:
                        chunks = audioop.add(chunks, chunk, self.samples_width)
                    else:
                        chunks = chunk
            if chunks:
                self.stream.write(chunks)

    def update_low(self):
        """
        Update sounds and music and play a new audio samples but use less
        resources than Audio_player.update() method.
        """

        with self.lock:
            framerate = int(self.framerate)
            chunks = bytes(self.chunk_size *
                           self.samples_width * self.nb_channels // 2)

            for sound in self.mixer:
                if sound.is_playing and self.is_playable(sound):
                    if self.is_music(sound):
                        volume = self.music_volume
                    else:
                        volume = self.sound_volume

                    chunk = sound.set_chunk_volume(sound.update(), volume
                                                   * sound.volume)
                    chunks = audioop.add(chunks, chunk, self.samples_width)
            chunks = audioop.ratecv(chunks, self.samples_width, self.nb_channels,
                                    AudioPlayer.default_framerate, framerate * 2, None)[0]
            self.stream.write(chunks)

    def get_music_in_mixer(self):
        """
        Get all musics in the mixer.

        :rtype: list
        :returns: A list of audio.music.Music.
        """

        return [music for music in self.mixer if isinstance(music, Music)]

    def get_sound_in_mixer(self):
        """
        Get all sounds in the mixer.

        :rtype: list
        :returns: A list of audio.sound.Sound.
        """

        return [sound for sound in self.mixer if not isinstance(sound, Music)]

    def stop_audio(self):
        """
        Stop all sounds and musics in the mixer.
        """

        for sound in self.mixer:
            sound.stop()
        self.mixer.clear()

    def pause_audio(self):
        """
        Pause all sounds and musics in the mixer.
        """

        for sound in self.mixer:
            sound.pause()

    def unpause_audio(self):
        """
        Unpause sounds and musics in the mixer.
        """

        for sound in self.mixer:
            sound.play()

    def set_speed(self, speed):
        """
        Set the reading speed of the audio player.

        :type speed: float
        :param speed: The speed of the audio player (default is 1)
        """
        self.framerate = AudioPlayer.default_framerate / speed

    def get_speed(self):
        """
        Get the current reading speed of the audio player.

        :rtype: float
        :returns: The current speed of the audio player (-1 if the default
            framerate is 0).
        """

        if AudioPlayer.default_framerate != 0:
            return AudioPlayer.default_framerate / self.framerate
        return -1
