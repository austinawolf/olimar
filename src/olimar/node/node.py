


class Node:
    def __init__(self, name, ip_address):
        self.name = name
        self.ip_address = ip_address

    def __str__(self):
        return f"{self.name}: {self.ip_address}"

    def __repr__(self):
        return self.__str__()
