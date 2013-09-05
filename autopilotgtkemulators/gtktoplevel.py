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
import time
from autopilot.input import Pointer, Mouse, Keyboard
from autopilotgtkemulators import AutopilotGtkEmulatorBase, EmulatorException
from autopilotgtkemulators import gtkaccessible, gtkcontainers, gtkcontrols
from autopilotgtkemulators import log_action, logging


class GtkWindow(AutopilotGtkEmulatorBase):
    """ Emulator class for a GtkWindow instance """
    def __init__(self, *args):

        super(GtkWindow, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()
        
    @log_action(logging.info)
    def open_save_dialog(self, dialogType='GtkFileChooserDialog'):
        """ Opens the save dialog

                :param dialogType: defaults to GtkFileChooserDialog if you have created
                            a custom dialog emulator then just override the default
                            dialog type
                :returns: an object of the save dialog
                :raises: **ValueError** if returned object is None
        """
        self.kbd.press_and_release('Ctrl+s')
        save_dialog = self.get_dialog(dialogType)
        if save_dialog is None:
            raise ValueError("Returned object is NoneType and not {0}".format(dialogType))
        save_dialog.visible.wait_for(1)
        return save_dialog
    
    #TODO: decide on new function name, this is confusing!
    @log_action(logging.info)
    def open_openfile_dialog(self, dialogType='GtkFileChooserDialog'):
        """ Opens the open file dialog

                :param dialogType: defaults to GtkFileChooserDialog if you have created
                            a custom dialog emulator then just override the default
                            dialog type
                :returns: an object of the open dialog
                :raises: **ValueError** if returned object is None
        """
        #TODO: add support for using open file button
        self.kbd.press_and_release('Ctrl+o')
        open_dialog = self.get_dialog(dialogType)
        if open_dialog is None:
            raise ValueError(
                "Returned object is NoneType and not {0}".format(dialogType))
        open_dialog.visible.wait_for(1)
        return open_dialog
    
    @log_action(logging.info)
    def open_print_dialog(self, dialogType='GtkPrintUnixDialog'):

        self.kbd.press_and_release('Ctrl+p')
        print_dialog = self.get_dialog(dialogType)
        print_dialog.visible.wait_for(1)
        return print_dialog

    @log_action(logging.info)
    def get_dialog(self, dialogType):
        """ gets an object for a dialog window
            
                :param dialogType: Window type of the dialog e.g 'GtkDialog'
                :returns: a dialog object of the given dialogType
                :raises: **EmulatorException** if a root instance cannot be obtained
                :raises: **ValueError** if the returned object is NoneType
        """
        root = self.get_root_instance()
        if root is None:
            raise EmulatorException("Emulator could not get root instance")
        dialog = root.select_single(dialogType)
        if dialog is None:
            raise ValueError(
                "Returned object is NoneType and not {0}".format(dialogType))
        return dialog


class GtkFileChooserDialog(AutopilotGtkEmulatorBase):
    """ Emulator class for a gtk file chooser dialog """
    def __init__(self, *args):
        super(GtkFileChooserDialog, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()
    
    
    def get_file_chooser_entry(self, ):
        """ Gets the file chooser entry in a GtkFileChooserDialog
            
            :returns: Returns an object of the GtkFileChooserEntry
            
            Which then provides access to the :class:`GtkFileChooserEntry` emulator
        """
        return self.select_single('GtkFileChooserEntry')

    
    def get_create_folder_button(self, ):
        """ Gets the create folder button """
        return self.select_single('GtkButton', label='Create Fo_lder')

    
    def get_path_bar(self, ):
        """ Gets the path bar in a GtkFileChooserDialog"""
        return self.select_single('GtkPathBar')
    
    @log_action(logging.info)
    def go_to_directory(self, dir_path):
        """ Navigates the file chooser dialog to the given directory path
        
        :param dir_path: path to required directory e.g '/tmp'
            
        .. note:: This function will get the focus of the :class:`GtkFileChooserEntry`
            so you do not need to do this first.
            
        Once you have got an object of a :class:`GtkFileChooserDialog` you can call this function
        straight away::
        
            >>> dialog = self.main_window.get_dialog()
            >>> dialog.go_to_directory('/tmp')
        """
        # select file system from the treeview so we are in the root directory
        treeview = self.select_many('GtkTreeView')[0]
        file_sys_item = treeview.select_item('File System')
        file_sys_item.click()
        # If GtkFileChooserDialog has a location togglebutton
        # try and select it and make sure its active so the
        # location entry is visible
        try:
            toggle_button = self.select_single('GtkToggleButton',
                                                tooltip_text='Type a file name')
            if toggle_button.active == 0:
                toggle_button.click()
        # If not then the dialog didn't have a toggle so we can safely catch
        # value exception and safely proceed
        except ValueError:
            pass
        
        entry = self.get_file_chooser_entry()
        entry.enter_text(dir_path, isDirPath=True)
        # lets add here that path bar contains dir_path
        # before returning
        path_bar = self.get_path_bar()
        path_bar.visible.wait_for(1)
        path_bar.is_path_in_pathbar(dir_path)
    
    @log_action(logging.info)
    def enter_file_name(self, filename):
        """ Enter the name of the file
        
            :param filename: Name of file
        """
        # this function is slighty different to go_to_directory
        # as it does not check the path bar that we are in the correct
        # dir_path
        entry = self.get_file_chooser_entry()
        entry.enter_text(filename)

    @log_action(logging.info)
    def create_folder_with_name(self, folderName):
        """ Creates a folder with given name
        
            :param folderName: name of folder
        """
        folder_button = self.get_create_folder_button()
        folder_button.click()
        self.kbd.type(folderName+'\n')

##TODO: Print Dialog
#class GtkPrintUnixDialog(AutopilotGtkEmulatorBase):
#
#    def __init__(self, *args):
#        super(GtkPrintUnixDialog, self).__init__(*args)
#        self.pointing_device = Pointer(Mouse.create())
#
#    def print_to_file(self, dir_path, filename):
#        """ Prints to a file
#
#            params:
#                    dir_path: path to required print location
#                    filename: name for file thats printed
#        """
#        pass
    
