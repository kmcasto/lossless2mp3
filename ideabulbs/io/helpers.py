#!/usr/bin/python
# -*- coding: utf-8 -*-
# This file is part of lossless2mp3.
#
# lossless2mp3 is free software: you can redistribute it and / or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# lossless2mp3 is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with lossless2mp3. If not, see <http://www.gnu.org/licenses/>.

"""Program description
@author: Andrei Matveyeu
@license: GNU GPL
@contact: arilou649@gmail.com
"""
import os
import sys
import fnmatch
import string

def escape_path(path):
    """Returns a path string fully escaped for script usage.
    @param path: path to be escaped
    @type path: string
    @return: escaped path
    @rtype:  string
    """
    return '"%s"' % (
        path
        .replace('\\', '\\\\')
        .replace('"', '\"')
        .replace(']', '\]')
        .replace('[', '\[')
        .replace(')', '\)')
        .replace('(', '\(')
        .replace(' ', '\ ')
        .replace('$', '\$')
        .replace('`', '\`')
        )

class File:
    """File class definition
    @author: Andrei Matveyeu
    @organization: ideabulbs.com
    @license: GNU GPL
    @contact: andrei@ideabulbs.com
    @since: 2012-05-20
    @status: in production
    @requires: $HOME/scripts/python added to PYTHONPATH environment variable
    """

    def __init__(self, file_name):
        """File default constructor
        @param file_name: name of a file (with full path or without)
        @type file_name: string
        """
        self._full_name = file_name
        self._file_name_only = file_name.split(os.sep)[:-1]
        self._directory = string.join(file_name.split(os.sep)[:-1], "/")

    def get_full_name(self):
        """Returns full file name including path, exactly as the
        argument specified by the constructor
        @return: file name
        @rtype: string
        """
        return self._full_name

    def get_full_escaped_name(self):
        """
        Returns fully escaped file name with path
        @return: escaped file name with path
        @rtype: string
        """
        return escape_path(self._full_name)

    def get_file_name_only(self):
        """Returns only the file name if the extension has been
        specified.
        @return: file name without path
        @rtype: string
        """

    def get_directory(self):
        """Returns the directory where the file is located.
        @return: directory
        @rtype: string
        """
        return self._directory

    def exists(self):
        """Checks if the file is existent.
        @return: true or false
        @rtype: boolean
        """
        return os.path.isfile(self._full_name)

    def is_absolute(self):
        """Checks if the file has absolute path specified.
        @return: true or false
        @rtype: boolean
        """
        return os.path.isabs(self._full_name)

    def is_directory(self):
        """Returns true if the current file is a directory
        @return: check if a File object is a directory
        @rtype: boolean
        """
        return os.path.isdir(self._full_name)

    def is_regular_file(self):
        """Returns true if the current file is a regular file, i. e. not
        a directory and not a symbolic link.
        @return: check if a File object is a regular file.
        @rtype: boolean
        """
        return os.path.isfile(self._full_name)

    def is_link(self):
        """Returns true if the current file is a symbolic link
        @return: check if a File object is a symbolic link
        @rtype: boolean
        """
        return os.path.islink(self._full_name)

    def is_mount_point(self):
        """Returns true if the current file is a mount point.
        @return: check if a File object is a mount point
        @rtype: boolean
        """
        return os.path.ismount(self._full_name)

    def get_extension(self):
        """Returns the file extension.
        @return: file extension
        @rtype: string
        """
        result =  self._full_name.split(".")
        if len(result) == 1:
            result = ""
        else:
            result =  "." + result[-1]
        return result

    def tree_level_depth(self):
        """Returns how many levels deep the file is.  The result does
        not take account of whether the path is absolute or relative.
        @return: depth level
        @rtype: int
        """
        result = len(self._full_name.split(os.sep)[1:-1])
        return result

    def read_lines(self):
        """
        Slurps the file and returns an array of lines.  The file is
        opened and closed automatically. There is no need to handle it
        on a higher level.

        @return: file lines
        @rtype: array
        """
        file_handler = open(self._full_name, "r")
        data = file_handler.readlines()
        file_handler.close()
        return data

    def count_lines(self):
        """Returns how many lines the file contains.
        @return: line count
        @rtype: int
        """
        return len(self.read_lines())

    def has_windows_linebreaks(self):
        """Checks if the file has Windows-style linebreaks. Returns
        False if the linebreaks are absent or aren't Windows standard.
        @return:  true or false
        @rtype:  boolean
        """
        result = False
        file_handler = open(self._full_name, "r")
        first_line = file_handler.readline()
        if first_line.endswidth("\r\n"):
            result = True
        return result

    def has_unix_linebreaks(self):
        """Checks if the file has Unix-style linebreaks. Returns
        False if the linebreaks are absent or aren't Unix standard.
        @return:  true or false
        @rtype:  boolean
        """
        result = False
        file_handler = open(self._full_name, "r")
        first_line = file_handler.readline()
        if first_line.endswidth("\r\n") == False and first_line.endswidth("\n") == True:
            result = True
        return result

    def has_mac_linebreaks(self):
        """Checks if the file has Mac-style linebreaks. Returns
        False if the linebreaks are absent or aren't Mac standard.
        @return:  true or false
        @rtype:  boolean
        """
        result = False
        file_handler = open(self._full_name, "r")
        first_line = file_handler.readline()
        if first_line.endswidth("\r") == True:
            result = True
        return result

    def get_file_size(self):
        """Returns the size of the current file."""
        return os.path.getsize(self._full_name)


def get_recursive_matches(directory, match):
    """Walks down over the sub-directory tree and looks for matches.
    @param directory: directory where the search starts.
    @type directory: string
    @param match: file name match to look for
    @type match: string
    @return: array of matching file names
    @rtype: array of strings
    """
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, match):
            matches.append(os.path.join(root, filename))
    return matches

