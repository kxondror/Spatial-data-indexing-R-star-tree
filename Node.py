from Record import Record
from Middle_entry import Middle_entry
from Split_group import Split_group
from Comparators import MinHeap_overlap

import sys
import heapq


class Node:
    def __init__(self, level, entries=[]):
        self.MAX_DEGREE = 3
        self.MIN_FILL_FACTOR = int(.40 * self.MAX_DEGREE)

        self.level = level
        self.entries = entries

    def add_entry(self, entry, parent_entry, overflow_dict):

        if isinstance(entry, Record) and self.level == overflow_dict[-1]:
            self.entries.append(entry)
            if parent_entry is not None:
                parent_entry.MBR = parent_entry.set_MBR()
        elif isinstance(entry, Middle_entry) and self.level != overflow_dict[-1]:
            self.entries.append(entry)



    def is_full(self):
        return True if len(self.entries) >= self.MAX_DEGREE else False

    def ChooseSpiltAxis(self, entry):
        M = self.entries
        M.append(entry)
        MAX_MARGIN = sys.maxsize
        splitAxisDistribution = None

        for dimension in range(2):

            entriesSortedByLower = sorted([entry for entry in M], key=lambda x: (x.MBR.get_points()[0][dimension], x.MBR.get_points()[0][dimension]))
            entriesSortedByHigher = sorted([entry for entry in M], key=lambda x: (x.MBR.get_points()[1][dimension], x.MBR.get_points()[1][dimension]))

            margin_sum = 0
            distributions = []
            for Lists in [entriesSortedByLower + entriesSortedByHigher]:
                for k in range(1, self.MAX_DEGREE - 2 * self.MIN_FILL_FACTOR + 3): #check paper 5.1 for the + 3
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

