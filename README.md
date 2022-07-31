# Pyoro (A Python fan game)

![Main menu](https://github.com/RedbeanGit/Pyoro/blob/main/Pyoro.png?raw=true)

## What is Pyoro?

Pyoro (A Python fan game) is a Nintendo GameBoy Game recreated with Python. The player plays a little bird with a very long tongue that he can use to eat beans which are falling from the sky.
Throughout the game, the music and the background change according to the time elapsed and the player's score. The game ends when a bean hit Pyoro. If the player reaches 10,000 points, a new mode appears. Let's have fun!

## Requirements

This project have been made for GNU/Linux based distributions.

It requires at least [Python 3.8](https://www.python.org/downloads/), [Pipenv](https://pypi.org/project/pipenv/) and [Portaudio 19](http://www.portaudio.com/) to run.

For Debian users, you can run the following command to install Python 3.8, Pipenv and Portaudio 19:

```bash
apt install python3.8 pipenv portaudio19-dev
```

## Installation

First clone this repo:

```bash
git clone git@github.com:RedbeanGit/pyoro.git
cd pyoro
```

Then setup a new pipenv virtual environment with dependencies needed:

```bash
pipenv install
```

## Run

First navigate to the project root directory:

```bash
cd path/to/pyoro
```

Then activate the Pipenv virtual environment:

```bash
pipenv shell
```

Finally start Pyoro:

```bash
./src/main.py
```

## Modding

At each start, the game tries to load any mods stored in the game save folder. If you want to modify the game without having to change the source code, you just need to place your mod (in .py format) in `/home/<user>/share/Pyoro` folder.
