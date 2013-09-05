 #-*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
 #
 #Copyright (C) 2013
 #
 #Author: Daniel Chapman daniel@chapman-mail.com
 #
 #This program is free software; you can redistribute it and/or modify
 #it under the terms of the GNU Lesser General Public License as published by
 #the Free Software Foundation; version 3.
 #
 #This program is distributed in the hope that it will be useful,
 #but WITHOUT ANY WARRANTY; without even the implied warranty of
 #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 #GNU Lesser General Public License for more details.
 #
 #You should have received a copy of the GNU Lesser General Public License
 #along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
from autopilot.matchers import Eventually
from testtools.matchers import Equals, FileExists, Contains
from autopilot.input import Pointer, Mouse, Keyboard
from autopilotgtkemulators import AutopilotGtkEmulatorBase
import time
from autopilotgtkemulators import gtktoplevel, gtkcontrols
from autopilot.testcase import AutopilotTestCase
from os.path import abspath, dirname, join

for root, dirs, files in os.walk(os.getcwd()):
    for name in files:
        if name == 'test-app':
            FULL_PATH = os.path.abspath(os.path.join(root, name))


class TestAppWindow(gtktoplevel.GtkWindow):

    def __init__(self, *args):
        super(TestAppWindow, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()


class EmulatorTest(AutopilotTestCase):

    def setUp(self):
        super(EmulatorTest, self).setUp()

        self.app = self.launch_test_application(FULL_PATH,
                                                app_type='gtk',
                                                emulator_base=AutopilotGtkEmulatorBase)
        self.pointing_device = Pointer(Mouse.create())
        self.assertThat(self.main_window.visible, Eventually(Equals(1)))
        self.status_label = self.app.select_single(BuilderName='statuslabel')

    @property
    def main_window(self, ):
        return self.app.select_single(TestAppWindow)

    def test_window(self, ):
        self.assertIsInstance(self.main_window, gtktoplevel.GtkWindow)
    
        self.assertThat(self.main_window.title,
                        Eventually(Contains('Test')))
    
    def test_click_gtkbutton(self):
        button = self.main_window.select_single('GtkButton',
                                                BuilderName='gtkbutton')
        self.assertIsInstance(button, gtkcontrols.GtkButton)
        button.click()
        self.assertThat(self.status_label.label,
                        Eventually(Equals('GtkButton was clicked')))
    
    def test_toolbar_entry(self):
        entry = self.main_window.select_single('GtkEntry',
                                               BuilderName='toolbarentry')
        self.assertIsInstance(entry, gtkcontrols.GtkEntry)
        entry.enter_text('Hello Autopilot')
        self.assertThat(entry.text, Equals('Hello Autopilot'))

    def test_openfile_dialog(self):
        dialog = self.main_window.open_openfile_dialog()
        self.assertIsInstance(dialog, gtktoplevel.GtkFileChooserDialog)
        dialog.go_to_directory('/tmp')
        dialog.enter_file_name('this_is_a_test_file_name')
        open_button = dialog.select_single('GtkButton', BuilderName='openfile_button')
        open_button.click()

    def test_save_dialog(self, ):
        dialog = self.main_window.open_save_dialog()
        self.assertIsInstance(dialog, gtktoplevel.GtkFileChooserDialog)
        dialog.go_to_directory('/tmp')
        dialog.enter_file_name('test_save_filename')
        save_button = dialog.select_single('GtkButton', BuilderName='savefile_button')
        save_button.click()

    def test_toolbar_button(self):
        button = self.main_window.select_single('GtkToolButton',
                                                BuilderName='toolbutton')
        self.assertIsInstance(button, gtkcontrols.GtkToolButton)
        button.click()
        self.assertThat(self.status_label.label,
                        Eventually(Equals('GtkToolButton was clicked')))
    
    def test_toggle_toolbar_button(self):
        button = self.main_window.select_single('GtkToggleToolButton',
                                                BuilderName='gtktoggletoolbutton')
        self.assertIsInstance(button, gtkcontrols.GtkToggleToolButton)
        button.click()
        self.assertThat(self.status_label.label,
                        Eventually(Equals('GtkToggleToolButton was clicked')))
        #TODO: test that it toggles
    
    def test_gtkmenutoolbutton(self):
        button = self.main_window.select_single('GtkMenuToolButton',
                                                BuilderName='gtkmenutoolbutton')
        self.assertIsInstance(button, gtkcontrols.GtkMenuToolButton)
        button.click()
        self.assertThat(self.status_label.label,
                        Eventually(Equals('GtkMenuToolButton was clicked')))
    
    def test_gtktogglebutton(self):
        button = self.main_window.select_single('GtkToggleButton',
                                                BuilderName='gtktogglebutton')
        self.assertIsInstance(button, gtkcontrols.GtkToggleButton)
        button.click()
        self.assertThat(self.status_label.label,
                        Eventually(Equals('GtkToggleButton was clicked')))
    
    def test_gtkcheckbutton(self):
        button = self.main_window.select_single('GtkCheckButton',
                                                BuilderName='gtkcheckbutton')
        self.assertIsInstance(button, gtkcontrols.GtkCheckButton)
        button.click()
        self.assertThat(self.status_label.label,
                        Eventually(Equals('GtkCheckButton was clicked')))
    
    def test_gtkentry(self):
        entry = self.main_window.select_single('GtkEntry',
                                               BuilderName='gtkentry')
        self.assertIsInstance(entry, gtkcontrols.GtkEntry)
        entry.enter_text('Hello Autopilot')
        self.assertThat(entry.text, Equals('Hello Autopilot'))
    
    def test_gtktextview(self):
        view = self.main_window.select_single('GtkTextView',
                                              BuilderName='gtktextview')
        self.assertIsInstance(view, gtkcontrols.GtkTextView)
        view.enter_text('This is testing a GtkTextView')
