from MBR import MBR


class Middle_entry:
    """
    Class representing an entry that exists at the non-leaf nodes of the tree and points to a node at a lower level.
    """
    def __init__(self, belonging_node=None) -> None:
        self.child_pointer = None
        self.MBR = None
        self.belonging_node = belonging_node

    def set_pointer(self, child) -> None:
        """
        Sets the pointer to a node and updates the MBR of the entry based on the rectangles contained in the node.

        :param child: (Node) The node we want the entry to point.
        :return: None
        """
        self.child_pointer = child
        self.MBR = self.set_MBR()

    def set_belonging_node(self, node) -> None:
        """
        Sets the node to which the entry belongs.

        :param node: (Node) The node that the entry is part of.
        :return: None
        """
        self.belonging_node = node

    def set_MBR(self) -> MBR | None:
        """
        Calculates and returns the minimum bounding rectangle (MBR) based on the MBRs of the entries in the node
        pointed to by this entry.

        :return: (MBR) The MBR object.
        """
        if bool(self.child_pointer.entries):
            points = []
            for entry in self.child_pointer.entries:
                total_points = entry.MBR.get_points()
                for point in total_points:
                    points.append(point)

            return MBR(points=points)
        return None
