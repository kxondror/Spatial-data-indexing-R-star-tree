from Node import Node
from Middle_entry import Middle_entry
from Comparators import MinHeap_overlap, MinHeap_areaExpansion

from collections import defaultdict
import math
import heapq


class RTree:
    def __init__(self):
        self.root = None
        self.overflow_flag = {}

    def Insert(self, record):
        if self.root is None:
            self.root = Node(level=1)
            self.overflow_flag[self.root.level] = True

        self.choose_subtree(self.root, record, level=list(self.overflow_flag)[-1])

    def choose_subtree(self, node, record, level, parent_entry=None, parent_node=None):

        if node.level == level:
            if not node.is_full():
                node.add_entry(record, parent_entry, list(self.overflow_flag))
            else:
                self.overflow(node, record, parent_entry, parent_node)

        else:
            min_heap = []
            heapq.heapify(min_heap)
            if node.level == list(self.overflow_flag)[-2]:
                for middle_entry in node.entries:
                    sample = MinHeap_overlap(middle_entry, record)
                    heapq.heappush(min_heap, sample)
            else:
                for middle_entry in node.entries:
                    sample = MinHeap_areaExpansion(middle_entry, record)
                    heapq.heappush(min_heap, sample)

            best_entry = min_heap[0].node.child_pointer
            self.choose_subtree(best_entry, record, level=best_entry.level, parent_entry=min_heap[0].node, parent_node=node)

    def overflow(self, node, record, parent_entry, parent_node):
        if not node == self.root and self.overflow_flag[node.level]:
            self.overflow_flag[node.level] = False
            self.ReInsert(node, record, parent_entry)
        else:
            self.split(node, record, parent_entry,parent_node)

    def ReInsert(self, node, record, parent_entry):

        distances = defaultdict(float)

        for entry in node.entries:
            distances[entry] = math.dist(entry.MBR.get_center(), parent_entry.MBR.get_center())
        distances[record] = math.dist(record.MBR.get_center(), parent_entry.MBR.get_center())

        distances = sorted(distances.items(), key=lambda item: item[1], reverse=True)

        node.entries = [row[0] for row in distances[int(node.MAX_DEGREE * 0.4):]]
        parent_entry.set_pointer(node)

        for reinsert_entries in reversed(distances[:int(node.MAX_DEGREE * 0.4)]):
            self.Insert(reinsert_entries[0])

    def split(self, node, entry, parent_entry, parent_node):

        slit_axis = node.ChooseSpiltAxis(entry)
        distribution1, distribution2 = node.ChooseSpiltIndex(slit_axis)

        if node == self.root:
            self.overflow_flag[node.level + 1] = True
            new_node1 = Node(level=node.level + 1, entries=distribution1)
            new_node2 = Node(level=node.level + 1, entries=distribution2)

            self.root = Node(level=1, entries=[Middle_entry(new_node1), Middle_entry(new_node2)])
        else:

            for entry in parent_node.entries:
                if entry.child_pointer == node:
                    parent_node.entries.remove(entry)
                    break

            if len(parent_node.entries) <= (parent_node.MAX_DEGREE - 2):
                parent_node.add_entry(Middle_entry(Node(level=node.level, entries=distribution1)), None, list(self.overflow_flag))
                parent_node.add_entry(Middle_entry(Node(level=node.level, entries=distribution2)), None , list(self.overflow_flag))
            elif len(parent_node.entries) <= (parent_node.MAX_DEGREE - 1):

                parent_node.add_entry(Middle_entry(Node(level=node.level, entries=distribution1)), "paok", list(self.overflow_flag))
                self.overflow(parent_node, Middle_entry(Node(level=node.level, entries=distribution2)),"paok","aok" )
            else:
                raise "cant have exactly 3 entries"



    def print_tree(self, node):

        if node.level == list(self.overflow_flag)[-1]:
            for entry in node.entries:
                print(entry.cordinates)
            return
        else:
            for i in node.entries:
                print(f"Middle entry:{i.MBR.get_points()}")
                self.print_tree(i.child_pointer)
