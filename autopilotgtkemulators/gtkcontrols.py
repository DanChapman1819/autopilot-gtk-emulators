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
from autopilotgtkemulators import EmulatorTypoException
from autopilotgtkemulators import log_action, logging

class GtkEntry(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkEntry widget """
    def __init__(self, *args):
        super(GtkEntry, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()
    
    def click(self, ):
        """ Click on GtkEntry """
        self.pointing_device.click_object(self)
    
    @log_action(logging.info)
    def enter_text(self, text):
        """ Enters given text into a GtkEntry widget
        
            Does not require GtkEntry to be clicked first and will delete any text currently in the entry when called
        
            :param text: String of text to enter in the entry
        """
        self._get_focus()
        assert self.is_focus == 1
        # if the entry is not empty lets empty it first
        if self.text != '':
            self.kbd.press_and_release('Ctrl+a')
            self.kbd.press_and_release('Delete')
        assert self.text == ''
        self.kbd.type(text)
        if self.text != text:
            raise EmulatorTypoException(
                "Typo Found: The text was not entered correctly. \
                The GtkEntry contains: '{0}' but should have been: '{1}'. \
                Possible causes are: The entry did not clear correctly before \
                entering text, or the keyboard mistyped".format(self.text, text))

    
    def _get_focus(self, ):
        self.pointing_device.click_object(self)
        self.is_focus.wait_for(1)

class GtkFileChooserEntry(GtkEntry):
    """ extends GtkEntry emulator"""
    def __init__(self, *args):
        super(GtkFileChooserEntry, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()

    @log_action(logging.info)
    def enter_text(self, text, isDirPath=False):
        """ Enters given text into a GtkFileChooserEntry widget
            
            Does not require GtkEntry to be clicked first and will delete any text currently in the entry when called
            
            params:
                :text: String of text to enter in the entry
                
                :isDirPath: If set to True will cause the dialog to navigate
                           to given directory
                        e.g see: GtkFileChooserDialog.go_to_directory()
        """
        self._get_focus()
        assert self.is_focus == 1
        # if the entry is not empty lets empty it first
        if self.text != '':
            self.kbd.press_and_release('Ctrl+a')
            self.kbd.press_and_release('Delete')
        assert self.text == ''
        self.kbd.type(text)
        assert self.text is not None
        #lets delete any highlighted autocompletion
        self.kbd.press_and_release('Delete')
        # the buffer should now match the given text
        if self.text != text:
            raise EmulatorTypoException(
                "Typo Found: The text was not entered correctly. \
                The GtkFileChooserEntry contains: '{0}' but should have been: '{1}'. \
                Possible causes are: The entry did not clear correctly before \
                entering text, or the keyboard mistyped".format(self.text, text))
        # if the text is a directory path then we want to hit enter
        # to navigate to path so we can enter filename in correct path
        if isDirPath:
            self.kbd.press_and_release('Enter')


class GtkButton(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkButton Instance """
    def __init__(self, *args):
        super(GtkButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self,):
        """ Clicks a GtkButton widget
        
            On some occasions you may need to wait for a button to become sensitive. 
            So when calling this function if the sensitive property is 0 it will wait for 10 seconds
            for button to become sensitive before clicking
        """
        #sometimes we may need to wait for the button to become clickable
        # so lets wait for it if we do
        if self.sensitive == 0:
            self.sensitive.wait_for(1)
        self.pointing_device.click_object(self)


class GtkToolButton(GtkButton):
    """ Emulator for a GtkToolButton instance
    
        Inherits from GtkButton
    """
    def __init__(self, *args):
        super(GtkToolButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())


class GtkLabel(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkLabel Instance"""
    def __init__(self, *args):
        super(GtkLabel, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        """ Clicks on a GtkLabel """
        self.pointing_device.click_object(self)
    
class GtkToggleButton(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkToggleButton instance """
    def __init__(self, *args):
        super(GtkToggleButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        """ Clicks a GtkToggleButton, and waits for the active state (toggled/nottoggled)
            to change after being clicked """
        #get current state
        new_val = 0
        if self.active == 0:
            new_val = 1
        #now click it
        self.pointing_device.click_object(self)
        #now wait for state to change
        self.active.wait_for(new_val)


class GtkToggleToolButton(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkToggleToolButton instance """
    def __init__(self, *args):
        super(GtkToggleToolButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        """ Clicks a GtkToggleToolButton, and waits for the active state (toggled/nottoggled)
            to change after being clicked """
        #get current state
        new_val = 0
        if self.active == 0:
            new_val = 1
        #now click it
        self.pointing_device.click_object(self)
        #now wait for state to change
        self.active.wait_for(new_val)


class GtkMenuToolButton(GtkButton):
    """ Emulator for a GtkMenuToolButton instance """
    def __init__(self, *args):
        super(GtkMenuToolButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())


class GtkCheckButton(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkCheckButton instance """
    def __init__(self, *args):
        super(GtkCheckButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        """ Clicks a GtkCheckButton, and waits for the active state (checked/notchecked)
            to change after being clicked """
        #get current state
        new_val = 0
        if self.active == 0:
            new_val = 1
        #now click it
        self.pointing_device.click_object(self)
        #now wait for state to change
        self.active.wait_for(new_val)
        


class GtkRadioButton(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkRadioButton instance """
    def __init__(self, *args):
        super(GtkRadioButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        """ Clicks a GtkRadioButton, and waits for the active state (checked/notchecked)
            to change after being clicked """
        #get current state
        new_val = 0
        if self.active == 0:
            new_val = 1
        #now click it
        self.pointing_device.click_object(self)
        #now wait for state to change
        self.active.wait_for(new_val)
        # TODO: lets look for its accessible prop and check that checked == True


class GtkSwitch(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkSwitch instance """
    def __init__(self, *args):
        super(GtkSwitch, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        #TODO: add checks to assert the switched changed state
        self.pointing_device.click_object(self)
        

class GtkTreeView(AutopilotGtkEmulatorBase):
    """ Emulator for a GtkTreeView instance """
    def __init__(self, *args):
        super(GtkTreeView, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        """ This simply clicks a treeview object """
        self.pointing_device.click_object(self)
        assert self.is_focus == 1

    @log_action(logging.info) 
    def select_item(self, label_text):
        """ Selects an item in a GtkTreeView by its UI label text
            
            :param label_text: The label value of the tree item as seen on the UI
            :returns: An object of the requested treeitem
            
            e.g. If you want to click say an item displaying 'Home' in a treeview
            then it would be::
                
                >>> treeitem = treeview.select_item('Home')
                
            also see GtkFileChooserDialog.go_to_directory() for another example
            
            if for some reason this doesn't work then use the .click()
            function to get the treeviews focus
        """
        treeview = self._get_gail_treeview()
        # if we can't get the gail treeview lets try a full scan
        if treeview is None:
            root = self.get_root_instance()
            treeview_item = root.select_single('GtkCellTextAccessible',
                                               accessible_name=str(label_text))
            assert treeview_item is not None
            return treeview_item
        #and now select the item from within the GAILTreeView. 
        item = treeview.select_item(str(label_text))
        assert item is not None
        return item
    
    
    def _get_gail_treeview(self, ):
        """ Gets the GtkTreeViews corresponding GtkTreeViewAccessible object """
        # lets get a root instance
        root = self.get_root_instance()
        assert root is not None
        # As the treeview item is in the GAILWindow tree and not our current tree
        # We want to select the treeviewaccessible with the same globalRect as us
        treeviews = root.select_many('GtkTreeViewAccessible',
                                     globalRect=self.globalRect)
        # if the treeviews are nested they could potentially have the
        # same globalRect so lets pick out the one thats visible
        for treeview in treeviews:
            if treeview.visible == True:
                return treeview
        
class GtkComboBox(AutopilotGtkEmulatorBase):
    
    def __init__(self, *args):
        super(GtkComboBox, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        #TODO: setup state changes
        #get current state i.e is it already open?

        #now click it
        self.pointing_device.click_object(self)
        #now check the state after to check that it changed
        #if not throw an error
        
    
    #TODO: can we create a function for selecting an item inside the
    #       combobox


class GtkComboBoxText(AutopilotGtkEmulatorBase):

    def __init__(self, *args):
        super(GtkComboBoxText, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    @log_action(logging.info)
    def click(self, ):
        #TODO: setup state changes
        #get current state i.e is it already open?

        #now click it
        self.pointing_device.click_object(self)
        #now check the state after to check that it changed
        #if not throw an error
        
    #TODO: can we create a function for selecting an item inside the
    #       combobox

class GtkSpinButton(AutopilotGtkEmulatorBase):

    def __init__(self, *args):
        super(GtkSpinButton, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())

    #def enter_value(self, ):
    #    #TODO: sort out entering a value in a spinbutton entry
    #    entry = self._select_entry()
    #
    #def _select_entry(self, ):
    #    #TODO: as experienced on ubiquity test when selecting a spin button
    #    # when the mouse clicks the center it does not get the entry focus
    #    # so we have to move mouse left by 10 px and click again to get entry focus
    #    # I'm not sure how safe this is and if it should be just left out.
    #    #We should have a way to use the spin button in ap though??
    #    pass

#TODO: This needs reworking as some filechooserbutton dont display gtkfilechooserdialog
# but instead works in the style of a gtkcombobox. hmmm maybe just use a simple click and leave
# it to the test author to handle??
#class GtkFileChooserButton(AutopilotGtkEmulatorBase):
#
#    def __init__(self, *args):
#        super(GtkFileChooserButton, self).__init__(*args)
#        self.pointing_device = Pointer(Mouse.create())
#
#    def click(self, ):
#        """ This returns the GtkFileChooserDialog object
#            that opens after button is clicked
#        """
#        self.pointing_device.click_object(self)
#        dialog = self._get_file_chooser_dialog()
#        return dialog
#
#    def _get_file_chooser_dialog(self, ):
#        root = self.get_root_instance()
#        assert root is not None
#        dialog = root.select_single('GtkFileChooserDialog')
#        assert dialog is not None
#        return dialog


class GtkTextView(AutopilotGtkEmulatorBase):

    def __init__(self, *args):
        super(GtkTextView, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()

    @log_action(logging.info)
    def enter_text(self, text):
        """ Enter given text into a GtkTextView widget
        
            Function will delete any text currently in the buffer when called
        
            params:
                :text: String of text to enter in the entry
        """
        self._get_focus()
        assert self.is_focus == 1
        # if the entry is not empty lets empty it first
        if self.buffer != '':
            self.kbd.press_and_release('Ctrl+a')
            self.kbd.press_and_release('Delete')
        assert self.buffer == ''
        self.kbd.type(text)
        if self.buffer != text:
            raise EmulatorTypoException(
                "Typo Found: The text was not entered correctly. \
                The GtkTextView contains: '{0}' but should have been: '{1}'. \
                Possible causes are: The textview did not clear correctly before \
                entering text, or the keyboard mistyped".format(self.buffer, text))
        #TODO: would it be good to return the buffer?

    
    def _get_focus(self, ):
        self.pointing_device.click_object(self)
        self.is_focus.wait_for(1)
