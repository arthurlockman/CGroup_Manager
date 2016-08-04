import dbus
import subprocess
import re
import multiprocessing
import os

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

    def shell_command(self, group, prop):
        process = subprocess.Popen(['systemctl', 'show', group, '-p', prop], stdout=subprocess.PIPE)
        val = process.communicate()[0]
        return val.decode('utf-8')

    def get_resource(self, group, resource):
        enable_prop = ''
        value_prop = ''
        enabled = False
        max_allocation = 0
        allocation = 0
        if resource == 'cpu':
            enable_prop = 'CPUAccounting'
            value_prop = 'CPUQuotaPerSecUSec'
            max_allocation = self.processors * 1000
        elif resource == 'mem':
            enable_prop = 'MemoryAccounting'
            value_prop = 'MemoryLimit'
            max_allocation = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        elif resource == 'blkio':
            enable_prop = 'BlockIOAccounting'
            value_prop = 'BlockIOWeight'
            max_allocation = 1000  # TODO: Fix this

        tmp = self.shell_command(group, enable_prop)
        enable_val = tmp.replace('\n', '').split('=')
        if len(enable_val) > 1:
            if enable_val[1] == 'yes' or enable_val[1] == 'Yes':
                enabled = True

        tmp = self.shell_command(group, value_prop)
        value_val = tmp.replace('\n', '').split('=')
        if len(value_val) > 1:
            unit = 'ms'
            if resource == 'cpu':
                if 'ms' in value_val[1]:
                    unit = 'ms'
                elif 's' in value_val[1]:
                    unit = 's'
            non_decimal = re.compile(r'[^\d.]+')
            tmp = non_decimal.sub('', value_val[1])
            if tmp != '':
                if unit == 's':
                    allocation = int(float(tmp) * 1000)
                else:
                    allocation = int(tmp)
            else:
                allocation = 0
        else:
            allocation = 0
        return Resource(resource, allocation, max_allocation, enabled)

    def refresh(self, resource, pie_chart):
        self.units = []
        units = self.systemd.ListUnits(
            dbus_interface='org.freedesktop.systemd1.Manager')
        for unit in units:
            new_unit = Unit(unit[0])
            res = self.get_resource(new_unit.name, resource)
            new_unit.resources[resource] = res
            self.units.append(new_unit)
        pie_chart.set_sections(self.units)


if __name__ == '__main__':
    cg = CGroupAPI()
