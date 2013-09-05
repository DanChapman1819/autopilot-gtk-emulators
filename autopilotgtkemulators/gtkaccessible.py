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
from autopilotgtkemulators import log_action, logging

class GtkTextCellAccessible(AutopilotGtkEmulatorBase):

    def __init__(self, *args):
        super(GtkTextCellAccessible, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
    
    @log_action(logging.info)
    def click(self, ):
        #TODO: raise an error if the object has negative global rect's as these can't be clicked
        self.pointing_device.click_object(self)
        
class GtkTreeViewAccessible(AutopilotGtkEmulatorBase):

    def __init__(self, *args):
        super(GtkTreeViewAccessible, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
    
    @log_action(logging.info)    
    def select_item(self, label):
        #TODO: raise an error if the object has negative global rect's as these can't be clicked
        item = self._get_item(label)
        return item
    
    
    def _get_item(self, label):
        return self.select_single('GtkTextCellAccessible', accessible_name=label)
    
    