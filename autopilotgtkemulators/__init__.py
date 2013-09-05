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
from autopilot.introspection.dbus import CustomEmulatorBase
import logging
from functools import wraps

logging = logging.getLogger('Autopilot Gtk User Test')
# copied from ubuntuuitoolkit
def log_action(log_func):
    """ Decorator to log the call of an action method """
    
    def middle(f):
        
        @wraps(f)
        def inner(instance, *args, **kwargs):
            class_name = str(instance.__class__.__name__)
            docstring = f.__doc__
            if docstring:
                docstring = docstring.split('\n')[0].strip()
            else:
                docstring = f.__name__
            log_line = '%r: %r. Arguments %r. Keyword arguments: %r.'
            log_func(log_line, class_name, docstring, args, kwargs)
            return f(instance, *args, **kwargs)
        
        return inner
    return middle

class EmulatorException(Exception):
    """ Exception raised when there is an error with the emulator """


class EmulatorTypoException(Exception):
    """ Exception raised when a typo has been made when entering text """

class AutopilotGtkEmulatorBase(CustomEmulatorBase):
    """ Base class for the Gtk Autopilot Emulator """