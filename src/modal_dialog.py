from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk


@Gtk.Template(resource_path='/net/curioussavage/simplefilemanager/modal_dialog.ui')
class ModalDialog(Gtk.Window):
    __gtype_name__ = 'ModalDialog'

    yes_btn = Gtk.Template.Child()
    cancel_btn = Gtk.Template.Child()

    def __init__(self, parent_win, **kwargs):
        super().__init__(**kwargs)

        self.set_transient_for(parent_win)

        self.connect('key_press_event', self.handle_keys)
        self.cancel_btn.connect('clicked', lambda a: self.destroy())
        self.yes_btn.connect('clicked', self.handle_yes)


    def handle_keys(self, w, event_key):
        if event_key.keyval == Gdk.KEY_Escape:
            self.hide()

    def handle_yes(self, w):
        self.emit('yes_clicked')
        self.destroy()

    @GObject.Signal(flags=GObject.SignalFlags.RUN_LAST, return_type=str,
                    arg_types=None,
                    accumulator=GObject.signal_accumulator_true_handled)
    def yes_clicked(self, *args):
        pass
