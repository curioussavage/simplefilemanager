from gi.repository import Gtk


@Gtk.Template(resource_path='/net/curioussavage/simplefilemanager/file_widget.ui')
class FileWidget(Gtk.EventBox):
    __gtype_name__ = 'FileWidget'

    file_label = Gtk.Template.Child()
    image = Gtk.Template.Child()

    def __init__(self, dir_entry, window, **kwargs):
        super().__init__(**kwargs)

        self.long_press = Gtk.GestureLongPress.new(self)
        self.long_press.connect('pressed', self.handle_long_pressed)
        self.dir_entry = dir_entry
        self.window = window

        self.multi_press = Gtk.GestureMultiPress.new(self)
        self.multi_press.connect_after('released', self.handle_multi_pressed)


        self.file_label.set_text(dir_entry.name)

        if dir_entry.is_file():
            self.image.set_from_icon_name('text-x-generic', 6)

        #self.connect_after('button-release-event', self.handle_clicked)

    def handle_multi_pressed(self, gesture, press_num, x, y):
        #import pdb; pdb.set_trace()
        print('multi pressed')
        if not self.dir_entry.is_file():
            self.window.change_dir(self.dir_entry.path)


    def handle_long_pressed(self, event, var, baz):
        #import pdb; pdb.set_trace()
        event.set_state(Gtk.EventSequenceState.CLAIMED)
        id = None
        def handle_press(ev, num, x, y):
            ev.set_state(Gtk.EventSequenceState.CLAIMED)
            print('\n\n disconnected')
            self.multi_press.disconnect(id)
            return True
        id = self.multi_press.connect('released', handle_press)
        print('long pressed')

    def handle_clicked(self, widget, event):
        print('\n click handler')
        if not self.dir_entry.is_file():
            self.window.change_dir(self.dir_entry.path)


