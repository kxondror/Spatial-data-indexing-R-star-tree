from Record import Record
from Middle_entry import Middle_entry
from Split_group import Split_group
from Comparators import MinHeap_overlap

import sys
import heapq


class Node:
    def __init__(self, level, entries=None, parent_entry=None):
        self.entries = None
        if entries is None:
            entries = []

        self.MAX_DEGREE = 2 # change after tests
        self.MIN_FILL_FACTOR = int(.50 * self.MAX_DEGREE) # change after tests
        self.entries = self.update_belonging_node(entries)
        self.level = level
        self.parent_entry = parent_entry

    def update_belonging_node(self, entries):
        for entry in entries:
            entry.set_belonging_node(self)
        return entries

    def add_entry(self, entry, leaf_level):

        if isinstance(entry, Record) and self.level == leaf_level:
            entry.set_belonging_node(self)
            self.entries.append(entry)
        elif isinstance(entry, Middle_entry) and self.level != leaf_level:
            entry.set_belonging_node(self)
            self.entries.append(entry)
        else:
            raise "Illegal Insertion!"

        if self.parent_entry is not None:
            self.parent_entry.MBR = self.parent_entry.set_MBR()

    @staticmethod
    def update_levels_topdown(node, leaf_level):
        for entry in node.entries:

            if isinstance(entry, Middle_entry):
                child_node = entry.child_pointer
                child_node.level = (node.level + 1)
                Node.update_levels_topdown(child_node, leaf_level)

            else:
                if node.level != leaf_level:
                    print("wrong")

    def is_full(self):
        total_entries = len(self.entries)
        if total_entries < self.MAX_DEGREE:
            return False
        elif total_entries == self.MAX_DEGREE:
            return True
        else:
            raise "A Node cant have more than :3 entries!"

    def ChooseSpiltAxis(self, entry):
        M = self.entries.copy()
        M.append(entry)
        MAX_MARGIN = sys.maxsize
        splitAxisDistribution = None

        for dimension in range(2):

            entriesSortedByLower = sorted([entry for entry in M], key=lambda x: (
                x.MBR.get_points()[0][dimension], x.MBR.get_points()[0][dimension]))
            entriesSortedByHigher = sorted([entry for entry in M], key=lambda x: (
                x.MBR.get_points()[1][dimension], x.MBR.get_points()[1][dimension]))

            margin_sum = 0
            distributions = []
            for Lists in [entriesSortedByLower + entriesSortedByHigher]:
                for k in range(1, self.MAX_DEGREE - 2 * self.MIN_FILL_FACTOR + 3):  # check paper 5.1 for the + 3
                    first_group = []
                    second_group = []

                    for j in range(0, (self.MIN_FILL_FACTOR - 1) + k):
                        first_group.append(Lists[j])

                    for j in range((self.MIN_FILL_FACTOR - 1) + k, len(M)):
                        second_group.append(Lists[j])

                    distribution = (Split_group(first_group), Split_group(second_group))
                    distributions.append(distribution)

                    margin_sum += distribution[0].MBR.get_area() + distribution[1].MBR.get_area()

                if margin_sum < MAX_MARGIN:
                    MAX_MARGIN = margin_sum
                    splitAxisDistribution = distributions

        return splitAxisDistribution

    def ChooseSpiltIndex(self, axis):
        min_heap = []
        heapq.heapify(min_heap)

        for distribution in axis:
            sample = MinHeap_overlap(distribution, None, isgroup=True)
            heapq.heappush(min_heap, sample)

        split_index = min_heap[0]
        return split_index.distribution[0].entries, split_index.distribution[1].entries
