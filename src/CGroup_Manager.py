import gi, math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")

    def draw(self, widget, event):
        cr = widget.get_property('window').cairo_create()

        cr.set_line_width(9)
        cr.set_source_rgb(0.7, 0.2, 0.0)

        w = widget.get_allocation().width
        h = widget.get_allocation().height

        cr.translate(w/2, h/2)
        cr.arc(0, 0, 50, 0, 2*math.pi)
        cr.stroke_preserve()

        cr.set_source_rgb(0.3, 0.4, 0.6)
        cr.fill()

builder = Gtk.Builder()
builder.add_from_file("MainAppWindow.glade")
builder.connect_signals(Handler())

window = builder.get_object("mainAppWindo")
headerBar = builder.get_object("headerBar")
window.set_titlebar(headerBar)
window.show_all()

Gtk.main()
