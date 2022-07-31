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
Provide update functions

Created on 17/11/2018
"""

import os

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"

from game.config import VERSION, UPDATE_HOST, UPDATE_USER, UPDATE_PASSWORD
from game.ftp_manager import FTPManager
from game.util import get_external_data_path, copy_directory


def get_connection_stream():
    """
    Create a new FTPManager and try to connect it to the server.

    :rtype: game.ftp_manager.FTPManager
    :returns: A new FTP_manager if successfully connected,
        otherwise None.
    """

    ftp = FTPManager(UPDATE_HOST, UPDATE_USER, UPDATE_PASSWORD)
    if ftp.connect():
        return ftp
    print(
        "[WARNING] [update.get_connection_stream] Unable to" + " connect to the server"
    )
    return None


def get_updates(ftp_mgr):
    """
    Search new versions on a server.

    :type ftp_mgr: game.ftp_manager.FTPManager
    :param ftp_mgr: The FTPManager used to download files.

    :rtype: list<str>
    :returns: A list of new versions. Return an empty list
        if something wrong happen.

    :Example: getUpdate(myftp_mgr) -> ["1.2", "1.2.1", "1.3"]
    """

    print("[INFO] [update.checkForUpdate] Checking for new updates")
    versions = ftp_mgr.read_server_file("htdocs/game_update/versions.txt").split("\n")
    version_found = False
    new_versions = []

    for version in versions:
        if version_found:
            new_versions.append(version)
        if version == VERSION:
            version_found = True
    return new_versions


def download_update(ftp_mgr, version):
    """
    Download files associated to a given version from the server.

    :type ftp_mgr: game.ftp_manager.FTPManager
    :param ftp_mgr: The FTPManager used to download files.

    :type version: str
    :param version: Version name (like "1.2.3")

    :rtype: bool
    :returns: False if an error occurs, True otherwise.
    """

    print("[INFO] [update.download_update] Downloading update v" + version)
    downloadfp = get_files_to_download(ftp_mgr, version)
    removefp = get_files_to_remove(ftp_mgr, version)
    server_folder = "htdocs/game_update/" + version + "/"
    local_folder = os.path.join(get_external_data_path(), "game_update")
    to_return = True

    for file_path in downloadfp:
        server_file_path = server_folder + file_path
        local_file_path = os.path.join(local_folder, file_path.replace("/", "\\"))

        if not ftp_mgr.download_file(server_file_path, local_file_path):
            to_return = False

    for file_path in removefp:
        local_file_path = os.path.join(local_folder, file_path.replace("/", "\\"))
        try:
            os.remove(local_file_path)
        except OSError:
            to_return = False
    return to_return


def get_files_to_download(ftp_mgr, version, folder="htdocs/game_update/"):
    """
    Get the name of the files to download for a defined version.

    :type ftp_mgr: game.ftp_manager.FTPManager
    :param ftp_mgr: The FTPManager to use.

    :type version: str
    :param version: The version to download.

    :type folder: str
    :param folder: Optional. The remote folder where to search the list
        of files to download.

    :rtype: list<str>
    :returns: A list of file paths.
    """

    to_remove_content = ftp_mgr.read_server_file(folder + version + "/toDownload.txt")
    if to_remove_content:
        file_paths = to_remove_content.split("\n")
        return file_paths
    return []


def get_files_to_remove(ftp_mgr, version, folder="htdocs/game_update/"):
    """
    Get the name of the files to remove for a defined version.

    :type ftp_mgr: game.ftp_manager.FTPManager
    :param ftp_mgr: The FTPManager to use.

    :type version: str
    :param version: In what version.

    :type folder: str
    :param folder: Optional. The remote folder where to search the list
        of files to remove.

    :rtype: list<str>
    :returns: A list of file paths.
    """

    to_download_content = ftp_mgr.read_server_file(folder + version + "/toRemove.txt")
    if to_download_content:
        file_paths = to_download_content.split("\n")
        return file_paths
    return []


def get_libs_directory():
    """
    Get the lib folder path.

    :rtype: str
    :returns: The absolute path of the lib folder.
    """

    if "lib" in os.listdir():
        return os.path.abspath("lib")
    return os.path.abspath("")


def install_update():
    """
    Copy updated files to the installation directory.

    :rtype: bool
    :returns: True if installation is a success, otherwise False.
    """

    print(
        "[INFO] [update.install_update] Copying update files "
        + "into game installation folder"
    )
    update_directory = os.path.join(get_external_data_path(), "game_update")
    lib_directory = get_libs_directory()
    to_return = True

    if os.path.exists(update_directory):
        file_names = os.listdir(update_directory)

        for file_name in file_names:
            file_path = os.path.join(update_directory, file_name)

            if os.path.isdir(file_path) and file_name != "data":
                if not copy_directory(
                    file_path, os.path.join(lib_directory, file_name)
                ):
                    print(
                        "[WARNING] [update.install_update] Something wrong"
                        + "happened while copying files to install directory"
                    )
                    to_return = False
            else:
                if not copy_directory(file_path, file_name):
                    print(
                        "[WARNING] [update.install_update] Something wrong"
                        + "happened while copying files to install directory"
                    )
                    to_return = False
    else:
        print("[WARNING] [update.install_update] No update found !")
        to_return = False
    return to_return
