class Resource:

    def __init__(self, name, allocation, max_allocation, enabled):
        self.name = name
        self.allocation = allocation
        self.max_allocation = max_allocation
        self.enabled = enabled
