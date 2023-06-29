from Record import Record
from Middle_entry import Middle_entry
from Comparators import MinHeap_overlap
from MBR import MBR

import sys
import heapq


class Node:
    """
    Class representing a node of the Tree. The entries it contains are of type Record if the node is at a leaf level;
    otherwise, it contains entries of type Middle_entry.
    """

    def __init__(self, entries=None, parent_entry=None) -> None:
        if entries is None:
            entries = []

        self.MAX_DEGREE = 2  # change after tests
        self.MIN_FILL_FACTOR = int(.50 * self.MAX_DEGREE)  # change after tests
        self.entries = self.update_belonging_node(entries)
        self.parent_entry = parent_entry

    def update_belonging_node(self, entries) -> list:
        """
        Iterates through all the entries in the node and updates their belonging_node attribute to point to this
        specific node.

        :param entries: (Record | Middle_entry) The entries of this node.
        :return: (list) A list of entries with their belonging_node attribute changed.
        """
        for entry in entries:
            entry.set_belonging_node(self)
        return entries

    def add_entry(self, entry) -> None:
        """
        Adds an entry to the node and updates the MBR of the entry(parent_entry) that points to this node.

        :param entry: (Record | Middle_entry) The entry we want to append.
        :return: None
        """
        entry.set_belonging_node(self)
        self.entries.append(entry)

        self.propagate_MBR(self)

    def remove_entry(self, entry) -> None:
        """
        Removes an entry from the node and updates the MBR of the entry(parent_entry) that points to this node.

        :param entry: (Record | Middle_entry) The entry we want to remove.
        :return: None
        """
        self.entries.remove(entry)
        del entry
        self.propagate_MBR(self)

    def propagate_MBR(self, node):
        """
        Updates recursively the MBRs of the nodes above the given argument node until it reaches the root node.

        :param node: (Node) The node we want to propagate upwards.
        :return: None
        """
        if node.parent_entry is not None:
            parent_entry = node.parent_entry
            parent_entry.MBR = parent_entry.set_MBR()
            self.propagate_MBR(parent_entry.belonging_node)

    def points_to_leaf(self) -> bool:
        """
        Checks whether this node is one level above the leaf level.Useful for the _choose_subtree() function in the
        R_star_tree.py file.

        :return: (Boolean) True if the node is the penultimate node; otherwise, returns false.
        """
        if isinstance(self.entries[0], Middle_entry):
            pointer = self.entries[0].child_pointer
            return True if isinstance(pointer.entries[0], Record) else False
        return False

    def is_full(self) -> bool:
        """
        Checks if the list of entries in the current node is full.

        :return: (Boolean) True if the entries list length is equal to the MAX_DEGREE; otherwise, returns false.
        """
        total_entries = len(self.entries)
        if total_entries < self.MAX_DEGREE:
            return False
        elif total_entries == self.MAX_DEGREE:
            return True
        else:
            raise "A Node cant have more than :3 entries!"

    def ChooseSpiltAxis(self, entry) -> list:
        """
        Calculates and determines the axis, to which the split will be performed.

        :param entry: (Middle_entry | Record) The entry that cannot be added to the node.
        :return: (list) A list with the proper split axis.
        """
        M = self.entries.copy()
        M.append(entry)
        MAX_MARGIN = sys.maxsize
        splitAxisDistribution = None

        # CSA1 For each axis
        for dimension in range(2):
            # CSA1 Sort the entries by the lower and then by the upper value of their rectangle
            entriesSortedByLower = sorted([entry for entry in M], key=lambda x: (
                x.MBR.get_points()[0][dimension], x.MBR.get_points()[0][dimension]))
            entriesSortedByHigher = sorted([entry for entry in M], key=lambda x: (
                x.MBR.get_points()[1][dimension], x.MBR.get_points()[1][dimension]))

            margin_sum = 0
            distributions = []
            # CSA1 Determine all distributions
            for Lists in [entriesSortedByLower + entriesSortedByHigher]:
                for k in range(1, self.MAX_DEGREE - 2 * self.MIN_FILL_FACTOR + 3):  # check paper 5.1 for the + 3
                    first_group = []
                    second_group = []

                    # 4 2 The first group contains the first (m-l)+k entries, the second group contains the remaining
                    # entries
                    for j in range(0, (self.MIN_FILL_FACTOR - 1) + k):
                        first_group.append(Lists[j])

                    for j in range((self.MIN_FILL_FACTOR - 1) + k, len(M)):
                        second_group.append(Lists[j])

                    # 4 2 For each distribution, goodness values are determined. Depending on these goodness values
                    # (margin value in this case) the final distribution of the entries is determined
                    distribution = (Split_group(first_group), Split_group(second_group))
                    distributions.append(distribution)

                    margin_sum += distribution[0].MBR.get_area() + distribution[1].MBR.get_area()

                # CSA2 Choose the axis with the overall minimum margin
                if margin_sum < MAX_MARGIN:
                    MAX_MARGIN = margin_sum
                    splitAxisDistribution = distributions

        return splitAxisDistribution

    @staticmethod
    def ChooseSpiltIndex(axis) -> tuple:
        """
        Calculates and returns a tuple with properly split entries.

        According to the paper:
        CSIl Along the chosen split axis, choose the distribution with the minimum overlap-value
        Resolve ties by choosing the distribution with minimum area-value

        :param axis: (list) The distributions calculated from the ChooseSpiltAxis() function.
        :return: (tuple) The split entries.
        """
        min_heap = []
        heapq.heapify(min_heap)

        for distribution in axis:
            sample = MinHeap_overlap(distribution, None, is_group=True)
            heapq.heappush(min_heap, sample)

        split_index = min_heap[0]
        return split_index.distribution[0].entries, split_index.distribution[1].entries


class Split_group:
    """
    A wrapper class for holding the split distribution group and its minimum bounding rectangle.
    """

    def __init__(self, group):
        self.entries = group
        self.MBR = self.set_MBR()

    def set_MBR(self) -> MBR:
        """
        Calculates and returns the minimum bounding rectangle (MBR) of the distribution group that will be useful for
        the ChooseSplitIndex() function.

        :return: (MBR) The MBR of the entries in the group.
        """
        total_points = []
        for point in self.entries:
            point1, point2 = point.MBR.get_points()
            total_points.append(point1)
            total_points.append(point2)

        return MBR(total_points)
