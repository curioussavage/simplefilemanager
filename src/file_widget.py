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

        self.long_press = Gtk.GestureLongPress.new(self)
        self.long_press.connect('pressed', self.handle_long_pressed)
        self.multi_press = Gtk.GestureMultiPress.new(self)
        self.long_press.group(self.multi_press)
        self.multi_press.connect_after('released', self.handle_multi_pressed)


        self.file_label.set_text(dir_entry.name)

        if dir_entry.is_file():
            self.image.set_from_icon_name('text-x-generic', 6)


    def handle_multi_pressed(self, gesture, press_num, x, y):
        if not self.dir_entry.is_file():
            self.window.change_dir(self.dir_entry.path)


    def handle_long_pressed(self, event, var, baz):
        event.set_state(Gtk.EventSequenceState.CLAIMED) # TODO look into why this doesn't work even on pinephone
        self.window.open_detail_view(self.dir_entry)
        return True

