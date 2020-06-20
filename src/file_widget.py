from gi.repository import Gtk


@Gtk.Template(resource_path='/net/curioussavage/simplefilemanager/file_widget.ui')
class FileWidget(Gtk.EventBox):
    __gtype_name__ = 'FileWidget'

    file_label = Gtk.Template.Child()
    image = Gtk.Template.Child()

    def __init__(self, dir_entry, window, **kwargs):
        super().__init__(**kwargs)
        self.dir_entry = dir_entry
        self.window = window

        self.file_label.set_text(dir_entry.name)

        if dir_entry.is_file():
            self.image.set_from_icon_name('text-x-generic', 6)

        self.connect('button-release-event', self.handle_clicked)

    def handle_clicked(self, widget, event):
        if not self.dir_entry.is_file():
            self.window.change_dir(self.dir_entry.path)


