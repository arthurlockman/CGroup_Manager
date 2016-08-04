from Resource import Resource


class Unit:

    def __init__(self, unit_name):
        self.name = unit_name
        self.resources = {}

    def get_list_row(self):
        """
        Gets a row for display in the GTK list view.
        """
        ret = []
        ret.append(self.name)
        for rsrc in ['io', 'mem', 'cpu']:
            if self.resources[rsrc].enabled:
                ret.append(str(self.resources[rsrc].get_percentage() * 100.0) + "%")
            else:
                ret.append('disabled')
        return ret
