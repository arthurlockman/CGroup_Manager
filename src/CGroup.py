class CGroup:
    def __init__(self, group_name, resource, initial_allocation):
        print('Creating group ', group_name)
        self.name = group_name
        self.resource = resource
        self.allocation = initial_allocation
        self.total = 360
