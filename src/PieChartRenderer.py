import gi, math
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PieChartRenderer:
    def __init__(self, drawingArea, color):
        print("Initializing pie chart renderer...")
        self.area = drawingArea
        self.area.connect('draw', self.draw)
        self.chart_color = color
        self.sections = [45, 10, 60, 90]

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
            x = r * math.cos(math.radians(section + accum))
            y = r * math.sin(math.radians(section + accum))
            cr.set_source_rgb(0, 0, 0)
            cr.arc(0, 0, r, math.radians(accum), math.radians(section + accum))
            cr.line_to(0, 0)
            accum += section
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

