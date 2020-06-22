# window.py
#
# Copyright 2020 curioussavage
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk
import os
import stat
import mimetypes
import shutil

from pathlib import Path
from .file_widget import FileWidget
from .modal_dialog import ModalDialog

mimetypes.init()

@Gtk.Template(resource_path='/net/curioussavage/simplefilemanager/window.ui')
class SimplefilemanagerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SimplefilemanagerWindow'

    modify_mode = False
    modify_type = None

    details_path = None
    modify_path = None

    toggle_hidden = Gtk.Template.Child()
    file_grid = Gtk.Template.Child()
    header_bar = Gtk.Template.Child()
    go_up = Gtk.Template.Child()

    main_stack = Gtk.Template.Child()
    file_view = Gtk.Template.Child()
    detail_view = Gtk.Template.Child()

    #details page
    go_back = Gtk.Template.Child()
    details_file_name = Gtk.Template.Child()
    details_file_type = Gtk.Template.Child()
    details_file_icon = Gtk.Template.Child()
    details_file_size = Gtk.Template.Child()
    move_btn = Gtk.Template.Child()
    copy_btn = Gtk.Template.Child()
    delete_btn = Gtk.Template.Child()

    modify_action_bar = Gtk.Template.Child()
    cancel_action_btn = Gtk.Template.Child()
    action_btn = Gtk.Template.Child()
    action_path = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = kwargs['application']._settings

        self.settings.connect('changed::show-hidden-files', self.show_hidden_toggle_handler)

        self.toggle_hidden.set_active(self.settings.get_boolean("show-hidden-files"))

        self.toggle_hidden.connect('toggled', self.toggle_view_hidden)

        self.change_dir(Path.home())
        self.go_up.connect('clicked', self.go_up_handler)
        self.go_back.connect('clicked', self.go_back_handler)

        self.move_btn.connect('clicked', self.move_handler)
        self.copy_btn.connect('clicked', self.copy_handler)
        self.delete_btn.connect('clicked', self.delete_handler)

        self.cancel_action_btn.connect('clicked', self.cancel_action)
        self.action_btn.connect('clicked', self.do_file_action)

    def toggle_view_hidden(self, w):
        val = self.settings.get_value('show-hidden-files')
        self.settings.set_boolean('show-hidden-files', not val)

    def show_hidden_toggle_handler(self, settings, value):
        self.change_dir(self.selected_dir)

    def enable_modify_mode(self, modify_type):
        self.modify_mode = True
        self.modify_path = self.details_path
        self.modify_type = modify_type
        self.action_btn.set_label(modify_type + ' here')
        self.action_path.set_text( self.modify_path.name)

        self.modify_action_bar.show()

    def cancel_action(self, w):
        self.modify_action_bar.hide()
        self.modify_mode = False
        self.modify_type = None
        self.modify_path = None

    def do_file_action(self, w):
        if self.modify_type == 'copy':
            if self.modify_path.is_file():
                try:
                    shutil.copy2(self.modify_path, self.selected_dir)
                except Exception:
                    print('couldn\'t copy file')
            else:
                # for directories
                try:
                    shutil.copytree(self.modify_path, self.selected_dir)
                except:
                    print('couldn\'nt copy dir')
            print('copied files')
        elif self.modify_type == 'move':
            try:
                shutil.move(self.modify_path, self.selected_dir)
            except Exception:
                print('could not move file')
            print('moved')
        self.cancel_action(None)
        self.change_dir(self.selected_dir)

    def move_handler(self, w):
        self.enable_modify_mode('move')
        self.main_stack.set_visible_child(self.file_view)

    def copy_handler(self, w):
        self.enable_modify_mode('copy')
        self.main_stack.set_visible_child(self.file_view)

    def delete_file(self):
        try:
            if self.details_path.is_file():
                os.remove(self.details_path)
            else:
                #TODO os.rmdir for empty dir
                shutil.rmtree(self.details_path)
        except Exception as e:
            print(e)

    def delete_handler(self, w):
        x = ModalDialog(self)

        def del_fn(w):
            self.delete_file()
            self.change_dir(self.selected_dir)
            self.go_back_handler(None)

        x.connect('yes_clicked', del_fn)
        # TODO use trash and implement undo
        x.show()

    def go_back_handler(self, w):
        self.go_back.hide()
        self.go_up.show()
        self.main_stack.set_visible_child(self.file_view)

    def open_detail_view(self, path):
        self.details_path = path
        self.go_up.hide()
        stat_res = path.stat()
        self.details_file_name.set_text(path.name)
        type = 'folder'
        if path.is_file():
            ext = path.name.split('.')[1]
            type = mimetypes.types_map.get('.' + ext)
            if not type:
                type = 'unknown'
        self.details_file_type.set_text(type)
        self.details_file_size.set_text(str(stat_res.st_size) + ' bytes')
        self.main_stack.set_visible_child(self.detail_view)
        self.go_back.show()

    def go_up_handler(self, w):
        self.change_dir(self.selected_dir.parent)

    def change_dir(self, path):
        self.selected_dir = Path(path)
        self.header_bar.set_title(self.selected_dir.name)

        self.file_grid.foreach(lambda child: self.file_grid.remove(child))

        files = os.scandir(self.selected_dir)

        sorted_files = []
        row = []

        for file in files:
            if file.name.startswith('.') and not self.settings.get_value('show-hidden-files'):
                continue
            #TODO actually sort them

            if len(row) == 3:
                sorted_files.append(row.copy())
                row.clear()

            row.append(file)
        if len(row):
            sorted_files.append(row)

        for row_num, row in enumerate(sorted_files):
            for file_num, file in enumerate(row):
                file_widget = FileWidget(file, self)
                self.file_grid.attach(file_widget, file_num, row_num, 1, 1)




        
