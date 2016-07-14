import gi, math, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

current_milli_time = lambda: int(round(time.time() * 1000))

class PieChartRenderer:
    def __init__(self, drawingArea, color, initial_groups):
        print("Initializing pie chart renderer...")
        self.area = drawingArea
        self.area.connect('draw', self.draw)
        self.area.connect('button-press-event', self.button_pressed)
        self.area.connect('button-release-event', self.button_released)
        self.area.connect('leave-notify-event', self.mouse_leave)
        self.area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                             Gdk.EventMask.BUTTON_RELEASE_MASK |
                             Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self.chart_color = color
        self.click_active = 0
        self.sections = initial_groups

    def draw(self, widget, event):
        cr = widget.get_property('window').cairo_create()

        cr.set_line_width(2)
        cr.set_source_rgb(0, 0, 0)

        w = widget.get_allocation().width
        h = widget.get_allocation().height
        r = 0
        if w < h:
            r = w / 2 - (w / 10.0)
        else:
            r = h / 2 - (h / 10.0)
        cr.translate(w/2, h/2)
        accum = 0;
        for section in self.sections:
            section_angle = (section.allocation / section.total) * 360.0
            x = r * math.cos(math.radians(section_angle + accum))
            y = r * math.sin(math.radians(section_angle + accum))
            cr.set_source_rgb(0, 0, 0)
            cr.arc(0, 0, r, math.radians(accum), math.radians(section_angle + accum))
            cr.line_to(0, 0)
            accum += section_angle
            cr.stroke_preserve()
            cr.close_path()
            cr.set_source_rgba(self.chart_color[0], self.chart_color[1],
                               self.chart_color[2], 0.6)
            cr.fill()

        cr.set_source_rgb(0, 0, 0)
        cr.arc(0, 0, r, math.radians(accum), 2*math.pi)
        cr.line_to(0, 0)
        cr.stroke_preserve()
        cr.close_path()
        cr.set_source_rgba(self.chart_color[0], self.chart_color[1],
                           self.chart_color[2], 0.1)
        cr.fill()

    def button_pressed(self, widget, event):
        self.click_active = current_milli_time()

    def button_released(self, widget, event):
        if current_milli_time() - self.click_active < 1000:
            print('Clicked!')

    def mouse_leave(self, widget, event):
        self.click_active = 0

