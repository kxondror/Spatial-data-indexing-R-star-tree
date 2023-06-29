from MBR import MBR


class Record:
    """
    Class representing an entry that exists at the leaf nodes of the tree and contains all the information about the
    geospatial data we being dealt with.
    """
    def __init__(self, slot, block, cordinates):
        self.record_slot = slot
        self.block_id = block
        self.cordinates = cordinates
        self.MBR = MBR(points=self.get_record_mbr())
        self.belonging_node = None

    def set_belonging_node(self, node) -> None:
        """
        Sets the node to which the entry belongs.

        :param node: (Node) The node that the entry is part of.
        :return: None
        """
        self.belonging_node = node

    def get_record_mbr(self) -> tuple:
        """
        Returns a tuple representing the minimum bounding rectangle (MBR) of the record, where both the bottom left
        and upper right points have the same value.

        :return: (tuple) The two corner points.
        """
        return tuple([cord for cord in self.cordinates]), tuple([cord for cord in self.cordinates])

    def compair_records(self, record):
        """
        Checks if two records are equal based on their arguments.

        :param record: (Record) The record we want to compair the current(self) one.
        :return: (Boolean) True if the records are equal; otherwise, returns false.
        """
        if record.block_id == self.block_id and \
                record.record_slot == self.record_slot:
            for counter, cord in enumerate(self.cordinates):
                if record.cordinates[counter] != cord:
                    return False
        else: return False
        return True
