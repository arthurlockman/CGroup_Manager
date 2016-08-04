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
        ret.append(str(self.resources['io'].allocation))
        ret.append(str(self.resources['mem'].allocation))
        ret.append(str(self.resources['cpu'].allocation))
        return ret
