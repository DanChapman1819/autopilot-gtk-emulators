# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (C) 2013
#
# Author: Daniel Chapman daniel@chapman-mail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import sys
from autopilot.input import Pointer, Mouse, Keyboard
from autopilotgtkemulators import AutopilotGtkEmulatorBase
from autopilotgtkemulators.gtkcontrols import GtkLabel, GtkToolButton
from autopilotgtkemulators import gtkaccessible
from autopilotgtkemulators import log_action, logging


class GtkPathBar(AutopilotGtkEmulatorBase):
    """ Emulator class for a GtkPathBar instance"""
    def __init__(self, *args):
        super(GtkPathBar, self).__init__(*args)

    @log_action(logging.info)
    def is_path_in_pathbar(self, dir_path):
        """
        Checks that the path contains the given path
        
        :param dir_path: Path to directory you want to test
        :raises: **ValueError** if pathbar does not contain path
        """
        # lets split the path
        split_path = self._splitpath(dir_path)
        labels = self.select_many('GtkLabel')
        # if we just get the last dir in the path (which should be our cwd)
        # and check for a label in pathbar which should be in bold
        last_dir = split_path[-1]
        for label in labels:
            if label.label == '<b>%s</b>' % last_dir:
                return
            else:
                raise ValueError('path bar did not contain %s' % last_dir)

    
    def _splitpath(self, path):
        path_parts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:
                path_parts.insert(0, parts[0])
                break
            elif parts[1] == path:
                path_parts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                path_parts.insert(0, parts[1])
        return path_parts


class GtkToolbar(AutopilotGtkEmulatorBase):
    """ Emulator class for a GtkToolBarInstance
    
        DO_NOT_USE this is not complete or even working in a sane fashion
    """
    def __init__(self, *args):
        super(GtkToolbar, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click_tool_button(self, **kwargs):
        button = self._get_button('GtkToolButton', **kwargs)
        button.click()


    def _get_button(self, *args, **kwargs):

        return self.select_single(*args, **kwargs)
    
class GtkBox(AutopilotGtkEmulatorBase):
    """ Emulator class for a GtkBox instance """
    def __init__(self, *args):
        super(GtkBox, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
