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
from pathlib import Path
from .file_widget import FileWidget


@Gtk.Template(resource_path='/net/curioussavage/simplefilemanager/window.ui')
class SimplefilemanagerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'SimplefilemanagerWindow'

    label = Gtk.Template.Child()
    file_grid = Gtk.Template.Child()
    header_bar = Gtk.Template.Child()
    go_up = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.change_dir(Path.home())
        self.go_up.connect('clicked', self.go_up_handler)

    def go_up_handler(self, w):
        self.change_dir(self.selected_dir.parent)

    def change_dir(self, path):
        self.selected_dir = Path(path)
        self.header_bar.set_title(self.selected_dir.name)

        self.file_grid.foreach(lambda child: self.file_grid.remove(child))
        #self.file_grid.remove_column(3)
        #self.file_grid.remove_column(2)
        #self.file_grid.remove_column(1)

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


        for row_num, row in enumerate(sorted_files):
            for file_num, file in enumerate(row):
                file_widget = FileWidget(file, self)
                #self.file_grid.add(file_widget)
                self.file_grid.attach(file_widget, file_num, row_num, 1, 1)




        
