import gi, math, os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PieChartRenderer import PieChartRenderer

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")

path = os.path.dirname(os.path.abspath(__file__))
gladeFile = os.path.join(path, "MainAppWindow.glade")

builder = Gtk.Builder()
builder.add_from_file(gladeFile)
builder.connect_signals(Handler())

ioChartRenderer = PieChartRenderer(builder.get_object('ioChartArea'),
                                  (51/255.0, 102/255.0, 255/255.0))
cpuhartRenderer = PieChartRenderer(builder.get_object('cpuChartArea'),
                                  (102/255.0, 51/255.0, 255/255.0))
memhartRenderer = PieChartRenderer(builder.get_object('memChartArea'),
                                  (204/255.0, 51/255.0, 255/255.0))
netChartRenderer = PieChartRenderer(builder.get_object('netChartArea'),
                                   (255/255.0, 51/255.0, 204/255.0))
window = builder.get_object("mainAppWindo")
headerBar = builder.get_object("headerBar")
window.set_titlebar(headerBar)
window.show_all()

Gtk.main()
