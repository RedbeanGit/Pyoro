# -*- coding:utf-8 -*-

# 	This file is part of Pyoro (A Python fan game).
#
# 	Metawars is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	Metawars is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with Metawars. If not, see <https://www.gnu.org/licenses/>

"""
Provide useful functions

Created on 17/11/2018
"""

import ctypes
import enum
import json
import os
import platform
import shutil
import subprocess
import sys
import threading

import pygame
import screeninfo

from pygame.locals import (
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_0,
    K_q,
    K_w,
    K_z,
    K_m,
    K_a,
    K_MINUS,
    K_LEFTBRACKET,
    K_RIGHTBRACKET,
    K_SEMICOLON,
    K_QUOTE,
    K_COMMA,
    K_PERIOD,
    K_SLASH,
    JOYBUTTONDOWN,
    JOYHATMOTION,
    JOYAXISMOTION,
)

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import DEFAULT_OPTIONS, NAME, VERSION


##############################################################################
### Input representation #####################################################
##############################################################################


def get_key_name(key_code):
    """
    Get azerty equivalent of a key from a qwerty keyboard

    :type key_code: int
    :param key_code: The pygame code of a key.

    :rtype: str
    :returns: A key representation.
    """

    new_keys = {
        K_1: "&",
        K_2: "é",
        K_3: '"',
        K_4: "'",
        K_5: "(",
        K_6: "-",
        K_7: "è",
        K_8: "_",
        K_9: "ç",
        K_0: "à",
        K_MINUS: ")",
        K_q: "q",
        K_w: "w",
        K_LEFTBRACKET: "^",
        K_RIGHTBRACKET: "$",
        K_a: "a",
        K_SEMICOLON: "m",
        K_QUOTE: "ù",
        K_z: "z",
        K_m: ",",
        K_COMMA: ";",
        K_PERIOD: ":",
        K_SLASH: "!",
    }

    if key_code in new_keys:
        return new_keys[key_code]
    return pygame.key.name(key_code)


def get_joy_key_name(input_type, **input_kwargs):
    """
    Get a representation of a joystick input.

    :type input_type: int
    :param input_type: The pygame code of a joystick input type.
        It can be JOYBUTTONDOWN, JOYHATMOTION or JOYAXISMOTION.

    :type **input_kwargs: object
    :param **input_kwargs: Some data about the input.

    :rtype: str
    :returns: A representation of the joystick input.
    """

    if input_type == JOYBUTTONDOWN:
        if "button_id" not in input_kwargs:
            input_kwargs["button_id"] = "inconnu"
        return f"Bouton {input_kwargs['button_id']}"
    elif input_type == JOYHATMOTION:
        if "value" not in input_kwargs:
            input_kwargs["value"] = (0, 0)
        input_kwargs["value"] = tuple(input_kwargs["value"])
        if input_kwargs["value"] == (-1, 0):
            return "gauche"
        elif input_kwargs["value"] == (1, 0):
            return "droite"
        elif input_kwargs["value"] == (0, -1):
            return "bas"
        elif input_kwargs["value"] == (0, 1):
            return "haut"
        else:
            return "direction ?"
    elif input_type == JOYAXISMOTION:
        if "axis_id" not in input_kwargs:
            input_kwargs["axis_id"] = 0
        if "value" not in input_kwargs:
            input_kwargs["value"] = 0
        if input_kwargs["axis_id"] == 0:
            if input_kwargs["value"] < 0:
                return "gauche"
            elif input_kwargs["value"] > 0:
                return "droite"
            else:
                return "direction ?"
        elif input_kwargs["axis_id"] == 1:
            if input_kwargs["value"] < 0:
                return "haut"
            elif input_kwargs["value"] > 0:
                return "bas"
            else:
                return "direction ?"


##############################################################################
### Options ##################################################################
##############################################################################


def save_options(options):
    """
    Save options in a json file.

    :type options: dict
    :param options: A dictionary with data to save.
    """

    print("[INFO] [util.save_options] Saving game options")
    option_file_path = os.path.join(get_external_data_path(), "options.json")
    with open(option_file_path, "w", encoding="utf-8") as file:
        json.dump(options, file, indent="\t")


def load_config():
    """
    Load options from a json file. If no option found, return
    game.config.DEFAULT_OPTIONS.

    :rtype: dict
    :returns: A dictionary of saved data.
    """

    print("[INFO] [util.loadOptions] Loading game options")
    option_file_path = os.path.join(get_external_data_path(), "options.json")
    if os.path.exists(option_file_path):
        with open(option_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return DEFAULT_OPTIONS


##############################################################################
### Leave, reset and restart #################################################
##############################################################################


def stop_game():
    """
    Stop the audio player, the debug logger and close the current window.
    """

    print(f"[INFO] [util.stop_game] Stopping {NAME.capitalize()}")
    pygame.quit()
    if Game.audio_player:
        Game.audio_player.stop()
    if Game.options:
        save_options(Game.options)
    if Game.debug_logger:
        Game.debug_logger.close()


def leave_game(error_id=0):
    """
    Stop the game and send an error message if something
    wrong happened.

    :type error_id: int
    :param error_id: Optional. An error id. 0 is used if
        not defined.
    """

    print(f"[INFO] [util.leave_game] Leaving {NAME.capitalize()} v{VERSION}")
    stop_game()
    log_message = " Consultez les logs pour plus de détails "
    message = "Une erreur est survenue ! "

    if error_id == 0:
        sys.exit()
    if error_id == Errors.MODULE_NOT_FOUND:
        message += "Un module Python essentiel est absent !"
    elif error_id == Errors.DATA_NOT_FOUND:
        message += "Impossible de trouver les ressources du jeu !"
    elif error_id == Errors.BOOT_ERROR:
        message += "Le jeu n'a pas réussi à démarrer !"
    elif error_id == Errors.LOOP_ERROR:
        message += "Plantage pendant la boucle de jeu !"
    elif error_id == Errors.UPDATE_ERROR:
        message += "Problème pendant l'installation des mises à jours !"
    elif error_id == Errors.BAD_RESOURCE:
        message += "Une ressource du jeu (image, son, json) est endommagée !"
    elif error_id == Errors.CODE_ERROR:
        message += "Mauvaise utilisation du code par l'un des mods !"

    raise RuntimeError(message + log_message + f"(error={error_id})")


def restart(*args):
    """
    Restart the game with defined arguments.

    :type *args: str
    :param *args: The arguments to pass on reboot.
    """

    print("[INFO] [util.restart] Restarting game")
    if sys.executable == sys.argv[0]:
        subprocess.Popen([sys.executable] + list(args))
    else:
        subprocess.Popen([sys.executable, sys.argv[0]] + list(args))
    leave_game()


def admin_restart(*args):
    """
    Restart by requesting administrator or root privileges.

    :type *args: str
    :param *args: The arguments to pass on reboot.
    """

    print("[INFO] [util.admin_restart] Restarting game with admin elevation")
    system_name = platform.system()
    args = list(args)

    if sys.executable != sys.argv[0]:
        args.insert(0, sys.argv[0])

    def uac_prompt():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(args), None, 1
        )

    def root_prompt():
        to_return = 0
        # If the user isn't a super user
        if os.geteuid() != 0:
            msg = "[sudo] password for %u:"
            to_return = subprocess.check_call(f"sudo -v -p '{msg}'", shell=True)
        return to_return

    if system_name == "Windows":
        threading.Thread(target=uac_prompt).start()
        leave_game()
    else:
        if root_prompt() == 0:
            restart()
        else:
            print("[WARNING] [util.admin_restart] Unable to get root privileges")
            leave_game()


def reset_game():
    """
    Reset the game and restart.
    """

    print("[INFO] [util.reset_game] Reseting game! Restarting...")
    option_file_path = os.path.join(get_external_data_path(), "options.json")
    if os.path.exists(option_file_path):
        os.remove(option_file_path)
    restart()


##############################################################################
### Data and modules managment ###############################################
##############################################################################


def check_data():
    """
    Check if there is resources.json file.

    :rtype: bool
    :returns: True if found, otherwise False.
    """

    print("[INFO] [util.check_data] Checking data")
    return os.path.exists(os.path.join("data", "resources.json"))


def check_modules():
    """
    Check needed python modules.

    :rtype: bool
    :returns: True if all needed modules are installed, otherwise False.
    """

    print("[INFO] [util.chechModules] Checking required modules")
    required = (
        "os",
        "sys",
        "pygame",
        "json",
        "wave",
        "audioop",
        "pyaudio",
        "threading",
        "traceback",
        "time",
        "platform",
        "shutil",
        "ftplib",
        "enum",
        "collections",
    )

    for module_name in required:
        try:
            print(f'[INFO] [util.chechModules] Checking "{module_name}"')
            exec("import " + module_name)
        except ImportError:
            print(
                "[WARNING] [util.chechModules] No module "
                + f'"{module_name}" detected !'
            )
            return False
    return True


def get_resource_paths(resource_type):
    """
    Get the path of all resources in a defined category.

    :type resource_type: str
    :param resource_type: The category of resource. It can be
        "musics", "sounds" and "images"

    :rtype: list<str>
    :returns: A list of paths to files of the specified category.
        If somethinf wrong happen, return an empty list.
    """

    print(f'[INFO] [util.get_resource_paths] Detecting "{resource_type}" resources')
    res_file_path = os.path.join("data", "resources.json")
    if os.path.exists(res_file_path):
        with open(res_file_path, "r", encoding="utf-8") as file:
            resources = json.load(file)
            if resource_type in resources:
                return resources[resource_type]
            print(
                f'[WARNING] [util.get_resource_paths] "{resource_type}"'
                + " is not a valid resource type"
            )
    else:
        print(
            "[WARNING] [util.get_resource_paths] " + f'Unable to find "{res_file_path}"'
        )
    leave_game(Errors.BAD_RESOURCE)


def get_external_data_path():
    r"""
    Get the path to the game data folder according to the host
    operating system.
        - %AppData%\Pyoro on Windows
        - /home/<user>/share/Pyoro on Linux distributions
        - /home/<user>/Library/Pyoro on MacOS.
    """

    system_name = platform.system()
    if system_name == "Windows":
        return os.path.join(os.environ["APPDATA"], NAME.capitalize())
    elif system_name == "Linux":
        return os.path.join(os.path.expanduser("~"), "share", NAME.capitalize())
    elif system_name == "Darwin":
        return os.path.join(os.path.expanduser("~"), "Library", NAME.capitalize())
    print("[WARNING] [util.get_external_data_path] Unknown operating system")
    return "saves"


def copy_directory(from_path, to_path):
    """
    Recursion copy file or folder.

    :type from_path: str
    :param from_path: The folder path to copy from.

    :type to_path: str
    :param to_path: The destination file or folder.

    :rtype: bool
    :returns: True if files and folders has been copied successfuly,
        otherwise False.
    """

    print(f"[INFO] [util.copy_directory] Copying folder {from_path} to {to_path}")
    to_return = True

    if os.path.isdir(from_path):
        file_names = os.listdir(from_path)
        for file_name in file_names:
            source_file_path = os.path.join(from_path, file_name)
            new_file_path = os.path.join(to_path, file_name)
            if not copy_directory(source_file_path, new_file_path):
                to_return = False
    else:
        if os.path.exists(from_path):
            if not os.path.exists(os.path.dirname(to_path)):
                os.makedirs(os.path.dirname(to_path))

            try:
                shutil.copyfile(from_path, to_path)
            except Exception:
                print(
                    "[WARNING] [util.copy_directory] Error while copying"
                    + f" {from_path} to {to_path} ! Ignoring it"
                )
                to_return = False
        else:
            print(
                "[WARNING] [util.copy_directory] File "
                + f'"{from_path}" doesn\'t exist'
            )
            to_return = False

    return to_return


##############################################################################
### Screen Infos #############################################################
##############################################################################


def get_layout_template(ratio):
    """
    Get the best layout for a given ratio.

    :type ratio: float
    :param ratio: The ratio of the game window.

    :rtype: dict
    :returns: A dictionary representing placement informations about
        the graphical components of the game menu.
    """

    # Detecting best layout name accourding to the resolution
    if ratio > 1:
        best_layout_name = "Wide"
    elif ratio < 1:
        best_layout_name = "Narrow"
    else:
        best_layout_name = "Square"

    layout_file_path = os.path.join("data", "layouts.json")
    if os.path.exists(layout_file_path):
        with open(layout_file_path, "r", encoding="utf-8") as file:
            layouts = json.load(file)

            # Searching the best layout
            for layout in layouts:
                if "name" in layout:
                    if layout["name"] == best_layout_name:
                        print(
                            "[INFO] [util.get_layout_template] Layout"
                            + f' "{best_layout_name}" choosen'
                        )
                        return layout
                else:
                    print(
                        "[WARNING] [util.get_layout_template] Some layouts"
                        + " aren't named"
                    )

        print(
            "[WARNING] [util.get_layout_template] Unable to find a layout"
            + " which fit the given ratio"
        )
        return {}
    print(
        "[WARNING] [util.get_layout_template] Unable" + f' to find "{layout_file_path}"'
    )
    leave_game(Errors.BAD_RESOURCE)


def get_monitor_size():
    """
    Return the screen size in mm.

    :rtype: tuple
    :returns: (width, height) tuple where width and height are ints which
        represent the default screen size in millimeters.
    """

    monitors = screeninfo.get_monitors()
    monitor = monitors[0]

    return monitor.width_mm, monitor.height_mm


def get_screen_size():
    """
    Return the screen size in pixels.

    :rtype: tuple
    :returns: (width, height) tuple where width and height are ints which
        represent the default screen size in pixels.
    """

    monitors = screeninfo.get_monitors()
    monitor = monitors[0]

    return monitor.width, monitor.height


def get_screen_ratio():
    """
    Return the screen resolution (width / height).

    :rtype: float
    :returns: A floating point value representing the ratio width / height.
    """

    width, height = get_screen_size()
    if height:
        return width / height
    print("[WARNING] [util.get_screen_ratio] Height can't be null")
    return 1


def get_monitor_density():
    """
    Return the monitor density in dpm.

    :rtype: tuple
    :returns: An (w, h) tuple where w and h are bot float numbers.
    """

    monitor_width, monitor_height = get_monitor_size()
    screen_width, screen_height = get_screen_size()
    return screen_width / monitor_width, screen_height / monitor_height


##############################################################################
### Enumerations #############################################################
##############################################################################


class Game:
    """
    Store main objects (unique instances).
    """

    window = None
    debug_logger = None
    audio_player = None
    options = None


class Errors(enum.Enum):
    """
    Provide common errors constants.
    """

    MODULE_NOT_FOUND = 1
    DATA_NOT_FOUND = 2
    BOOT_ERROR = 3
    LOOP_ERROR = 4
    UPDATE_ERROR = 5
    BAD_RESOURCE = 6
    CODE_ERROR = 7
