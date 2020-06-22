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

from pathlib import Path
from .file_widget import FileWidget

mimetypes.init()

@Gtk.Template(resource_path='/net/curioussavage/simplefilemanager/window.ui')
class SimplefilemanagerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SimplefilemanagerWindow'

    label = Gtk.Template.Child()
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.change_dir(Path.home())
        self.go_up.connect('clicked', self.go_up_handler)
        self.go_back.connect('clicked', self.go_back_handler)


    def go_back_handler(self, w):
        self.go_back.hide()
        self.go_up.show()
        self.main_stack.set_visible_child(self.file_view)

    def open_detail_view(self, path):
        self.go_up.hide()
        stat_res = path.stat()
        self.details_file_name.set_text(path.name)
        type = 'folder'
        if path.is_file():
            ext = path.name.split('.')[1]
            type = mimetypes.types_map.get('.' + ext)
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
            if file.name.startswith('.'): #  TODO check setting here
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
                print(file_num)
                file_widget = FileWidget(file, self)
                self.file_grid.attach(file_widget, file_num, row_num, 1, 1)




        
