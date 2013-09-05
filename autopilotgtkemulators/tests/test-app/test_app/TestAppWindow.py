# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('test_app')

from test_app_lib import Window
from test_app.AboutTestAppDialog import AboutTestAppDialog


# See test_app_lib.Window.py for more details about how this class works
class TestAppWindow(Window):
    __gtype_name__ = "TestAppWindow"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(TestAppWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutTestAppDialog

        # Code for other initialization actions should be added here.
        self.open_dialog = self.builder.get_object('gtkfilechooserdialog')
        self.status_label = self.builder.get_object('statuslabel')

    def on_mnu_open_activate(self, menuitem, data=None):
        """Display the open-dialog for test-app."""
        if self.open_dialog is not None:
            response = self.open_dialog.run()
            self.open_dialog.hide()

    def on_mnu_save_activate(self, menuitem, data=None):
        if self.open_dialog is not None:
            response = self.open_dialog.run()
            self.open_dialog.hide()

    def on_mnu_save_as_activate(self, menuitem, data=None):
        if self.open_dialog is not None:
            self.response = self.open_dialog.run()
            self.open_dialog.hide()

    def on_openfile_button_clicked(self, widget, data=None):
        self.open_dialog.hide()

    def on_toolbutton_clicked(self, widget, data=None):
        self.status_label.set_text('GtkToolButton was clicked')

    def on_gtktoggletoolbutton_clicked(self, widget, data=None):
        self.status_label.set_text('GtkToggleToolButton was clicked')

    def on_gtkmenutoolbutton_clicked(self, widget, data=None):
        self.status_label.set_text('GtkMenuToolButton was clicked')

    def on_gtkbutton_clicked(self, widget, data=None):
        self.status_label.set_text('GtkButton was clicked')

    def on_gtktogglebutton_clicked(self, widget, data=None):
        self.status_label.set_text('GtkToggleButton was clicked')

    def on_gtkcheckbutton_clicked(self, widget, data=None):
        self.status_label.set_text('GtkCheckButton was clicked')

