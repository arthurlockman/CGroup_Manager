import gi
import math
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk


def point_inside_polygon(x, y, poly):
    """
    Determines if a mouse click or point falls inside a polygon
    constructed of (x, y) points. Found from:
    http://goo.gl/kppZzZ

    :param x: x position of click
    :param y: y position of click
    :param poly: a list of polygon tuples defining the area of interest (x, y)
    """
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


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
        self.polygons = []

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
        cr.translate(w / 2, h / 2)
        accum = 0
        self.polygons = []
        for section in self.sections:
            section_angle = (section.allocation / section.total) * 360.0
            x = r * math.cos(math.radians(section_angle + accum))
            y = r * math.sin(math.radians(section_angle + accum))
            x1 = r * math.cos(math.radians(accum))
            y1 = r * math.sin(math.radians(accum))
            cr.set_source_rgb(0, 0, 0)
            cr.arc(0, 0, r, math.radians(accum), math.radians(section_angle + accum))
            cr.line_to(0, 0)
            self.polygons.append(self.generate_click_polygon(accum, section_angle + accum, r))
            accum += section_angle
            cr.stroke_preserve()
            cr.close_path()
            cr.set_source_rgba(self.chart_color[0], self.chart_color[1],
                               self.chart_color[2], 0.6)
            cr.fill()

        cr.set_source_rgb(0, 0, 0)
        cr.arc(0, 0, r, math.radians(accum), 2 * math.pi)
        cr.line_to(0, 0)
        cr.stroke_preserve()
        cr.close_path()
        cr.set_source_rgba(self.chart_color[0], self.chart_color[1],
                           self.chart_color[2], 0.1)
        cr.fill()

    def generate_click_polygon(self, start_theta, end_theta, radius):
        """
        Generate the bounding polygon for the click area on the
        pie chart.
        :param self: self reference
        :param start_theta:
        :param end_theta:
        :param radius:
        """
        polygon = [(0, 0)]
        step_accum = 0
        step_count = 10.0
        step_amount = (end_theta - start_theta) / step_count
        for step in range(int(step_count) + 1):
            x = radius * math.cos(math.radians(start_theta + step_accum))
            y = radius * math.sin(math.radians(start_theta + step_accum))
            polygon.append((x, y))
            step_accum += step_amount
        return polygon

    def button_pressed(self, widget, event):
        self.click_active = int(round(time.time() * 1000))

    def button_released(self, widget, event):
        if int(round(time.time() * 1000)) - self.click_active < 1000:
            window_w = widget.get_allocation().width
            window_h = widget.get_allocation().height
            pointer = widget.get_pointer()
            mouse_x = pointer.x - window_w / 2
            mouse_y = pointer.y - window_h / 2
            for polygon in self.polygons:
                if point_inside_polygon(mouse_x, mouse_y, polygon):
                    idx = self.polygons.index(polygon)
                    group = self.sections[idx]
                    print(group.name)
                    break

    def mouse_leave(self, widget, event):
        self.click_active = 0
