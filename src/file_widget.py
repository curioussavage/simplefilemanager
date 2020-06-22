from gi.repository import Gtk

from contextlib import contextmanager


@Gtk.Template(resource_path='/net/curioussavage/simplefilemanager/file_widget.ui')
class FileWidget(Gtk.EventBox):
    __gtype_name__ = 'FileWidget'

    file_label = Gtk.Template.Child()
    image = Gtk.Template.Child()

    def __init__(self, dir_entry, window, **kwargs):
        super().__init__(**kwargs)
        self.tap_was_handled = False

        self.dir_entry = dir_entry
        self.window = window

        self.long_press = Gtk.GestureLongPress.new(self)
        self.long_press.set_property('delay_factor', 1.1)
        self.long_press.connect('pressed', self.handle_long_pressed)
        self.multi_press = Gtk.GestureMultiPress.new(self)
        self.multi_press.connect('released', self.handle_multi_released)
        self.multi_press.connect('pressed', self.handle_multi_pressed)


        self.file_label.set_text(dir_entry.name)

        if dir_entry.is_file():
            self.image.set_from_icon_name('text-x-generic', 6)

    @contextmanager
    def tap_handled(self):
        yield
        if self.tap_was_handled == False:
            self.tap_was_handled = True
        else:
           self.tap_was_handled = False

    def handle_multi_released(self, gesture, press_num, x, y):
        with self.tap_handled():
            if not self.tap_was_handled:
                if not self.dir_entry.is_file():
                    self.window.change_dir(self.dir_entry.path)

    def handle_multi_pressed(self, guesture, num, x, y):
        pass
        #todo set a background

    def handle_long_pressed(self, event, var, baz):
        with self.tap_handled():
            if not self.tap_was_handled:
                event.set_state(Gtk.EventSequenceState.CLAIMED) # TODO look into why this doesn't work even on pinephone
                self.window.open_detail_view(self.dir_entry)
                return True

