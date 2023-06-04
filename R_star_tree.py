from Node import Node
from Middle_entry import Middle_entry
from Comparators import MinHeap_overlap, MinHeap_areaExpansion

from collections import defaultdict
import math
import heapq


class RTree:
    def __init__(self):
        self.root = None
        self.overflow_flags = {}

    def Insert_data(self, rectangle):
        if self.root is None:
            self.root = Node(level=1, entries=[], parent_entry=None)
            self.overflow_flags[self.root.level] = True

        # ID1 Invoke Insert starting with the leaf level as a parameter, to Insert a new data rectangle
        self.Insert(rectangle, leaf_level=list(self.overflow_flags)[-1])

    def Insert(self, rectangle, leaf_level):

        # I1 Invoke ChooseSubtree. with the level as a parameter,to find an appropriate node N in which to place the
        # new entry E

        N = self.choose_subtree(self.root, rectangle, level=leaf_level)

        # I2 If N has less than M entries, accommodate rectangle in N
        if len(N.entries) < N.MAX_DEGREE:
            N.add_entry(rectangle, list(self.overflow_flags))
        else:
            self.OverflowTreatment(node=N, new_entry=rectangle,
                                   level=N.level)  # If N has M entries. invoke OverflowTreatment with the level of N
            # as a parameter [for reinsertion or split]

    def choose_subtree(self, node, rectangle, level):

        if node.level == level:
            return node

        else:
            min_heap = []
            heapq.heapify(min_heap)
            # CS2 If the child-pointers in N point to leaves
            if node.level == list(self.overflow_flags)[-2]:
                for middle_entry in node.entries:
                    wrapper = MinHeap_overlap(middle_entry, rectangle)
                    heapq.heappush(min_heap, wrapper)
            else:  # CS2 If the child-pointers in N do not point to leaves
                for middle_entry in node.entries:
                    wrapper = MinHeap_areaExpansion(middle_entry, rectangle)
                    heapq.heappush(min_heap, wrapper)

            best_entry = min_heap[0].entry
            return self.choose_subtree(best_entry.child_pointer, rectangle, level=best_entry.child_pointer.level)

    def OverflowTreatment(self, node, new_entry, level):

        if level != 1 and self.overflow_flags[level]:
            self.overflow_flags[level] = False
            self.ReInsert(node, new_entry)
        else:
            self.split(node, new_entry)

    def ReInsert(self, node, new_entry):

        distances = defaultdict(float)

        for entry in node.entries:
            distances[entry] = math.dist(entry.MBR.get_center(), node.parent_entry.MBR.get_center())
        distances[new_entry] = math.dist(new_entry.MBR.get_center(), node.parent_entry.MBR.get_center())

        distances = sorted(distances.items(), key=lambda item: item[1], reverse=True)

        node.entries = [row[0] for row in distances[int(node.MAX_DEGREE * 0.4):]]
        node.parent_entry.set_pointer(node)

        for reinsert_entries in reversed(distances[:int(node.MAX_DEGREE * 0.4)]):
            self.Insert(reinsert_entries[0], node.level)

    def split(self, node, new_entry):

        slit_axis = node.ChooseSpiltAxis(new_entry)
        distribution1, distribution2 = node.ChooseSpiltIndex(slit_axis)

        if node.level == 1:
            self.overflow_flags[node.level + 1] = True

            self.root = Node(level=1, parent_entry=None)

            m1 = Middle_entry(belonging_node=self.root)
            new_node1 = Node(level=self.root.level + 1, entries=distribution1, parent_entry=m1)
            m1.set_pointer(new_node1)

            m2 = Middle_entry(belonging_node=self.root)
            new_node2 = Node(level=self.root.level + 1, entries=distribution2, parent_entry=m2)
            m2.set_pointer(new_node2)

            self.root.add_entry(m1, list(self.overflow_flags))
            self.root.add_entry(m2, list(self.overflow_flags))

        else:
            parent_node = node.parent_entry.belonging_node

            for new_entry in parent_node.entries:
                if new_entry.child_pointer == node:
                    parent_node.entries.remove(new_entry)
                    break

            if len(parent_node.entries) <= (parent_node.MAX_DEGREE - 2):

                m1 = Middle_entry(belonging_node=parent_node)
                new_node1 = Node(level=node.level, entries=distribution1, parent_entry=m1)
                m1.set_pointer(new_node1)

                m2 = Middle_entry(belonging_node=parent_node)
                new_node2 = Node(level=node.level, entries=distribution2, parent_entry=m2)
                m2.set_pointer(new_node2)

                parent_node.add_entry(m1, list(self.overflow_flags))
                parent_node.add_entry(m2, list(self.overflow_flags))

            else:
                m1 = Middle_entry(belonging_node=parent_node)
                new_node1 = Node(level=node.level, entries=distribution1, parent_entry=m1)
                m1.set_pointer(new_node1)
                parent_node.add_entry(m1, list(self.overflow_flags))

                m2 = Middle_entry(belonging_node=parent_node)
                new_node2 = Node(level=node.level, entries=distribution2, parent_entry=m2)
                m2.set_pointer(new_node2)
                self.OverflowTreatment(parent_node, m2, parent_node.level)

    def print_tree(self, node):
        if node.entries is None:
            print(node.level)
            input("ok")

        if node.level == list(self.overflow_flags)[-1]:
            for entry in node.entries:
                print(entry.cordinates)
            return
        else:
            for i in node.entries:
                print(f"Middle entry: {i.MBR.get_points()} ,level :{node.level}")
                self.print_tree(i.child_pointer)
