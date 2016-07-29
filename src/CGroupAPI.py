import dbus
import subprocess
import re
import multiprocessing

from Unit import Unit
from Resource import Resource


class CGroupAPI:

    def __init__(self):
        print('Bringing up CGroup API...')
        self.processors = multiprocessing.cpu_count()
        print('Found', self.processors, 'cores')
        dbus_proxy = dbus.SystemBus()  # initializing system dbus
        self.systemd = dbus_proxy.get_object('org.freedesktop.systemd1',
                                             '/org/freedesktop/systemd1')
        self.units = []

    def get_group_property(self, prop, group):
        """
        Get a property from a group.
        """
        systemctl_cmd = subprocess.Popen(
            ['systemctl', 'show', group, '-p', prop], stdout=subprocess.PIPE)
        systemctl_prop = systemctl_cmd.communicate()[0].decode(
            'utf-8').replace('\n', '').split('=')
        if (len(systemctl_prop) > 1):
            non_decimal = re.compile(r'[^\d.]+')
            return_prop = non_decimal.sub('', systemctl_prop[1])
            if (return_prop != ''):
                return_prop = int(return_prop)
            else:
                return_prop = 0
        else:
            return_prop = 0
        return return_prop

    def refresh(self, resource_name, pie_chart):
        self.units = []
        units = self.systemd.ListUnits(
            dbus_interface='org.freedesktop.systemd1.Manager')
        for unit in units:
            new_unit = Unit(unit[0])
            res = Resource(resource_name, self.get_group_property(
                resource_name, new_unit.name), self.processors * 1000)
            new_unit.resources[resource_name] = res
            self.units.append(new_unit)
        pie_chart.set_sections(self.units)


if __name__ == '__main__':
    cg = CGroupAPI()
