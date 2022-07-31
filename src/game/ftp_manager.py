# -*- coding: utf-8 -*-

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
Povides useful class for connecting, sending and receiving
files on a FTPs server.

Created on 27/10/2018
"""

import os
import ftplib

__author__ = "RedbeanGit"
__repo__ = "https://github.com/RedbeanGit/Pyoro"


class FTPManager:
    """
    Simplify sending and downloading files on a FTPs server.
    """

    def __init__(self, host, user="", password=""):
        """
        Initialize a FTPManager object. To connect it to the server,
        run FTPManager.connect().

        :type host: str
        :param host: The host address (IP or DNS).

        :type user: str
        :param user: Optional. The username to use for login.

        :type password: str
        :param password: Optional. The password to use for login.
        """

        self.stream = None
        self.connected = False
        self.host = host
        self.user = user
        self.password = password
        self.buffer = ""

    def __print_error__(
        self, error, method_name="__print_error__", msg="An error occured !"
    ):
        """
        Internal method used to display a specific message according to
        a defined error.

        :type error: Exception
        :param error: The error to manage.

        :type method_name: str
        :param method_name: Optional. The FTPManager method that had
            an error.

        :type msg: str
        :param msg: Optional. A message to display.
        """

        to_display = "%s%s"
        if isinstance(error, ftplib.error_temp):
            to_display = "[WARNING] [FTPManager.%s] %s Temporary unvailable"
        elif isinstance(error, ftplib.error_perm):
            to_display = (
                "[WARNING] [FTPManager.%s]"
                + " %s Permanent error, check server file permission"
            )
        elif isinstance(error, ftplib.error_proto):
            to_display = (
                "[WARNING] [FTPManager.%s]"
                + " %s The server reply does not fit the FTP specifications"
            )
        elif isinstance(error, ftplib.error_reply):
            to_display = (
                "[WARNING] [FTPManager.%s]" + " %s Unexpected reply from the server"
            )
        elif isinstance(error, IOError):
            to_display = (
                "[WARNING] [FTPManager.%s] %s "
                + "An error occured while writing in a local file"
            )
        else:
            to_display = "[WARNING] [FTPManager.%s] %s Unknown cause"
        print(to_display % (method_name, msg))

    def connect(self, user=None, password=None):
        """
        Try to connect to the FTPs server.

        :type user: str
        :param user: Optional. If not defined, the default user is used.

        :type password: str
        :param password: Optional. If not defined, the default password
            is used.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        print("[INFO] [FTPManager.connect] Connecting to the server")
        user = user if user else self.user
        password = password if password else self.password
        try:
            self.stream = ftplib.FTP_TLS(self.host, user, password)
            self.connected = True
            print("[INFO] [FTPManager.connect] Connected successfuly !")
            return True
        except Exception as error:
            self.__print_error__(
                error, "connect", "Unable to connect or to login to the server !"
            )
        self.connected = False
        return False

    def disconnect(self):
        """
        Try to disconnect to the FTPs server.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if self.connected:
            try:
                self.stream.quit()
                self.connected = False
                return True
            except Exception as error:
                self.__print_error__(
                    error, "disconnect", "Unable to disconnect from the server !"
                )
        else:
            print("[WARNING] [FTPManager.disconnect]" + " Not connected to the server")
        return False

    def read_server_file(self, server_file_path):
        """
        Read a text file (utf-8 encoding) on the server.

        :type server_file_path: str
        :param server_file_path: The path to the file on the server.

        :rtype: str
        :returns: A string of the file content.
            Empty string if something wrong happen.
        """

        self.buffer = ""

        def write(binary):
            self.buffer += binary.decode()

        if self.connected:
            try:
                self.stream.retrbinary("RETR " + server_file_path, write)
            except Exception as error:
                self.__print_error__(
                    error,
                    "read_server_file",
                    f'Unable to read "{server_file_path}" from the server !',
                )
            return self.buffer
        print(
            "[WARNING] [FTPManager.read_server_file]" + " Not connected to the server"
        )
        return ""

    def download_file(self, server_file_path, local_file_path):
        """
        Download a file from the server.

        :type server_file_path: str
        :param server_file_path: The path to the file on the server.

        :type local_file_path: str
        :param local_file_path: The path of the new local file.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if self.connected:
            try:
                if not os.path.exists(os.path.dirname(local_file_path)):
                    os.makedirs(os.path.dirname(local_file_path))

                with open(local_file_path, "wb") as file:
                    self.stream.retrbinary("RETR " + server_file_path, file.write)

                return True
            except Exception as error:
                self.__print_error__(
                    error,
                    "download_file",
                    f'Unable to download "{server_file_path}" from'
                    + f' the server to "{local_file_path}"!',
                )
        else:
            print(
                "[WARNING] [FTPManager.download_file]" + " Not connected to the server"
            )
        return False

    def send_file(self, local_file_path, server_file_path):
        """
        Send a file to the server.

        :type local_file_path: str
        :param local_file_path: The path of the local file to send.

        :type server_file_path: str
        :param server_file_path: The path to the new file on the server.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if self.connected:
            try:

                with open(local_file_path, "rb") as file:
                    self.stream.storbinary("STOR " + server_file_path, file)

                return True
            except Exception as error:
                self.__print_error__(
                    error,
                    "send_file",
                    f'Unable to send "{local_file_path}"'
                    + f' to the server from "{server_file_path}" !',
                )
        else:
            print("[WARNING] [FTPManager.send_file]" + " Not connected to the server")
        return False

    def get_server_file_names(self, server_folder_path=None):
        """
        Get the names of all files and directories in a specific
        folder on the server.

        :type server_folder_path: str
        :param server_folder_path: Optional. The path to the folder
            on the server.

        :rtype: list<str>
        :returns: A list of file names.
        """

        if self.connected:
            if not server_folder_path:
                server_folder_path = self.stream.pwd()
            try:
                return self.stream.nlst(server_folder_path)
            except Exception as error:
                self.__print_error__(
                    error,
                    "get_server_file_names",
                    f'Unable to get file names in "{server_folder_path}" !',
                )
        else:
            print(
                "[WARNING] [FTPManager.get_server_file_names]"
                + " Not connected to the server"
            )
        return []

    def get_current_directory(self):
        """
        Get the current working directory path on the server.

        :rtype: str
        :returns: The path of the current working directory.
            Return an empty string if something wrong happen.
        """

        if self.connected:
            return self.stream.pwd()
        print(
            "[WARNING] FTPManager.get_current_directory]"
            + " Not connected to the server"
        )
        return ""

    def set_current_directory(self, server_path):
        """
        Set the working directory path.

        :type server_path: str
        :param server_path: The path to the new working directory.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if self.connected:
            try:
                self.stream.cwd(server_path)
                return True
            except Exception as error:
                self.__print_error__(
                    error,
                    "set_current_directory",
                    f'Unable to define "{server_path}"' + " as the current directory !",
                )
        else:
            print(
                "[WARNING] [FTPManager.get_current_directory]"
                + " Not connected to the server"
            )
        return False

    def rename_server_path(self, from_name, to_name):
        """
        Rename a file or a folder on the server.

        :type from_name: str
        :param from_name: The path to the file or folder to rename.

        :type to_name: str
        :param to_name: The new path to give to the file
            or folder to rename.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if self.connected:
            try:
                self.stream.rename(from_name, to_name)
                return True
            except Exception as error:
                self.__print_error__(
                    error,
                    "rename_server_path",
                    f'Unable to rename "{from_name}"' + f' to "{to_name}" !',
                )
        else:
            print(
                "[WARNING] [FTPManager.rename_server_path]"
                + " Not connected to the server"
            )
        return False

    def remove_server_file(self, server_file_path):
        """
        Remove a file (doesn't work for folders) on the server.

        :type server_file_path: str
        :param server_file_path: The path to the file to remove.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if self.connected:
            try:
                self.stream.delete(server_file_path)
                return True
            except Exception as error:
                self.__print_error__(
                    error,
                    "remove_server_file",
                    f'Unable to remove "{server_file_path}" from the server !',
                )
        else:
            print(
                "[WARNING] [FTPManager.remove_server_file] Not connected to the server"
            )
        return False

    def remove_server_directory(self, server_folder_path):
        """
        Remove a folder (doesn't work for a file) on the server.

        :type server_folder_path: str
        :param server_folder_path: The path to the folder to remove.

        :rtype: bool
        :returns: True if it's a success, otherwise False.
        """

        if self.connected:
            try:
                self.stream.rmd(server_folder_path)
                return True
            except Exception as error:
                self.__print_error__(
                    error,
                    "remove_server_directory",
                    f'Unable to remove "{server_folder_path}" from the server !',
                )
        else:
            print(
                "[WARNING] [FTPManager.remove_server_directory]"
                + " Not connected to the server"
            )
        return False

    def get_file_size(self, server_file_path):
        """
        Get the file of a file on the server.

        :type server_file_path: str
        :param server_file_path: The path to the file to get the size.

        :rtype: int
        :returns: The size of the file.
        """

        if self.connected:
            try:
                return self.stream.size(server_file_path)
            except Exception as error:
                self.__print_error__(
                    error,
                    "get_file_size",
                    f'Unable to get the size of "{server_file_path}" !',
                )
        else:
            print(
                "[WARNING] [FTPManager.get_file_size]" + " Not connected to the server"
            )
        return 0
