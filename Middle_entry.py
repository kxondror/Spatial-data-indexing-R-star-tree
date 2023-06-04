from MBR import MBR


class Middle_entry:
    def __init__(self, child=None, belonging_node=None):
        self.child_pointer = child
        self.MBR = None
        self.belonging_node = belonging_node

    def set_pointer(self, child):
        self.child_pointer = child
        self.MBR = self.set_MBR()

    def set_belonging_node(self, node):
        self.belonging_node = node

    def set_MBR(self):
        if bool(self.child_pointer.entries):
            points = []
            for entry in self.child_pointer.entries:
                total_points = entry.MBR.get_points()
                for point in total_points:
                    points.append(point)

            return MBR(points)
        return None
