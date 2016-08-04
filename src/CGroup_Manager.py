import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from multiprocessing import Process
from PieChartRenderer import PieChartRenderer
from Unit import Unit
from CGroupAPI import CGroupAPI


class AppEventHandler:

    def __init__(self, manager):
        self.manager = manager

    def on_delete_window(self, *args):
        Gtk.main_quit(*args)

    def on_refresh(self, *args):
        print('refreshing view...')
        self.manager.refresh()


class CGroupManager:

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        gladeFile = os.path.join(path, "MainAppWindow.glade")

        builder = Gtk.Builder()
        builder.add_from_file(gladeFile)
        builder.connect_signals(AppEventHandler(self))

        self.api = CGroupAPI()

        self.unitListArea = builder.get_object('unitListArea')
        self.unit_liststore = Gtk.ListStore(str, str, str, str)
        self.unitListArea.set_model(self.unit_liststore)
        renderer1 = Gtk.CellRendererText()
        col1 = Gtk.TreeViewColumn("Unit", renderer1, text=0)
        renderer2 = Gtk.CellRendererText()
        col2 = Gtk.TreeViewColumn("I/O", renderer2, text=0)
        renderer3 = Gtk.CellRendererText()
        col3 = Gtk.TreeViewColumn("Memory", renderer3, text=0)
        renderer4 = Gtk.CellRendererText()
        col4 = Gtk.TreeViewColumn("CPU", renderer4, text=0)
        self.unitListArea.append_column(col1)
        self.unitListArea.append_column(col2)
        self.unitListArea.append_column(col3)
        self.unitListArea.append_column(col4)
        self.ioChartRenderer = PieChartRenderer(builder.get_object('ioChartArea'),
                                                (51 / 255.0, 102 /
                                                 255.0, 255 / 255.0),
                                                'io')
        self.cpuChartRenderer = PieChartRenderer(builder.get_object('cpuChartArea'),
                                                 (102 / 255.0, 51 /
                                                  255.0, 255 / 255.0),
                                                 'cpu')
        self.memChartRenderer = PieChartRenderer(builder.get_object('memChartArea'),
                                                 (204 / 255.0, 51 /
                                                  255.0, 255 / 255.0),
                                                 'mem')
        self.refresh()
        self.window = builder.get_object("mainAppWindow")
        headerBar = builder.get_object("headerBar")
        self.window.set_titlebar(headerBar)

    def main(self):
        self.window.show_all()
        Gtk.main()

    def refresh(self):
        self.api.refresh([self.ioChartRenderer, self.cpuChartRenderer,
                          self.memChartRenderer], self.unitListArea)

if __name__ == '__main__':
    cgroup_manager = CGroupManager()
    cgroup_manager.main()
