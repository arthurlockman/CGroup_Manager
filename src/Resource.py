class Resource:

    def __init__(self, name, allocation, max_allocation, enabled):
        self.name = name
        self.allocation = allocation
        self.max_allocation = max_allocation
        self.enabled = enabled

    def get_percentage(self):
        if self.enabled:
            return self.allocation / self.max_allocation
        else:
            return 0
