import gi
import os

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PieChartRenderer import PieChartRenderer
from CGroup import CGroup


class AppEventHandler:

    def on_delete_window(self, *args):
        Gtk.main_quit(*args)


class CGroupManager:

    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        gladeFile = os.path.join(path, "MainAppWindow.glade")

        builder = Gtk.Builder()
        builder.add_from_file(gladeFile)
        builder.connect_signals(AppEventHandler())

        # TOOD: Remove this
        sections = [45, 90, 20, 15, 165]
        groups = []
        i = 0
        for s in sections:
            groups.append(CGroup('test' + str(i), 'cpu', s))
            i += 1

        self.ioChartRenderer = PieChartRenderer(builder.get_object('ioChartArea'),
                                                (51 / 255.0, 102 /
                                                 255.0, 255 / 255.0),
                                                groups)
        self.cpuChartRenderer = PieChartRenderer(builder.get_object('cpuChartArea'),
                                                 (102 / 255.0, 51 /
                                                  255.0, 255 / 255.0),
                                                 groups)
        self.memChartRenderer = PieChartRenderer(builder.get_object('memChartArea'),
                                                 (204 / 255.0, 51 /
                                                  255.0, 255 / 255.0),
                                                 groups)
        self.netChartRenderer = PieChartRenderer(builder.get_object('netChartArea'),
                                                 (255 / 255.0, 51 /
                                                  255.0, 204 / 255.0),
                                                 groups)

        self.window = builder.get_object("mainAppWindow")
        headerBar = builder.get_object("headerBar")
        self.window.set_titlebar(headerBar)

    def main(self):
        self.window.show_all()
        Gtk.main()

if __name__ == '__main__':
    cgroup_manager = CGroupManager()
    cgroup_manager.main()
