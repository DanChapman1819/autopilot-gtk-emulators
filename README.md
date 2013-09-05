Autopilot Gtk Emulators is a set of emulators for interacting with gtk applications
using autopilot. It provides a useful set of utility functions to ease the pain of writing
automated tests for gtk apps.

The emulators are seperated into relevent groups

gtktoplevel:- contains Emulators for GtkWindow, GtkFileChooserDialog and GtkPrintUnicDIalog
              still more to be added.

gtkcontainers:- contains a GtkPathBar and GtkToolbar emulators

gtkcontrols:- contains all other objects such as GtkButton and all other button types,
              GtkLabel, GtkTextView all the main elements you would normally interact with
              in an application.
              
The GtkWindow class functions provide support for launching the Save, Open and Print dialogs
of an application it also has a get_dialog function for any other type of dialog within an app
. These functions return an object of the selected dialog i.e

        save_dialog = self.main_window.open_save_dialog()
        
we now have a save_dialog object which we can access the functions of the GtkFileChooserDialog
class which are

     go_to_directory(dir_path)  # Navigates to the given directory path
     enter_file_name(name)      # enters the filename
     create_folder_with_name(name)  #creates a folder with given name


All objects that are clickable i.e GtkButton, GtkCheckButton .... all have a click() function
so as an example

        button = self.main_window.select_single('GtkButton')
        #we can now just call click
        button.click()
        
For objects such as GtkCheckButtons where they can have more than one state the emulator
checks the state of the object changed once clicked. This saves you time so you don't have to check
that you have selected the object. You can just call the click function on the object and this is taken care of

All text entry objects (GtkEntry, GtkTextView ...) have an enter_text() method. SO you can basically just
select the object and call enter_text() e.g

        text_view = self.main_window.select_single('GtkTextView')
        #and now just call enter_text()
        text_view.enter_text('This text will be entered')

The emulator gets the objects focus, checks the object has no text, if it does then it deletes it
first, then enters the given text and checks the objects corresponding buffer that the text was
entered correctly before returning.

GtkTreeViews now have a select_item() function which selects the item given the UI text value e.g

Say we want to select 'Home' in the 'Places' treeview in Nautilus

        treeview = self.main_window.select_many('GtkTreeView')[0]
        treeitem = treeview.select_item('Home')
        #and then we can just call click()
        treeitem.click()