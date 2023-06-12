from Node import Node
from Middle_entry import Middle_entry
from Record import Record
from Comparators import MinHeap_overlap, MinHeap_areaExpansion
from collections import defaultdict

import math
import heapq


class RTree:
    def __init__(self) -> None:
        self.root = None
        self.overflow_flags = {}
        self.total_levels = 1

    def Insert_data(self, rectangle) -> None:
        if self.root is None:
            self.root = Node()
            self.overflow_flags[1] = False

        # ID1 Invoke Insert starting with the leaf level as a parameter, to Insert a new data rectangle
        self.Insert(rectangle=rectangle, level=1)

    def Insert(self, rectangle, level) -> None:

        # I1 Invoke ChooseSubtree, with the level as parameter to find an appropriate node N in which to place the new
        # entry E
        N = self.choose_subtree(node=self.root, rectangle=rectangle, level=level)

        # I2 If N has less than M entries, accommodate rectangle in N
        if not N.is_full():
            N.add_entry(entry=rectangle)
        else:
            self.OverflowTreatment(node=N, new_entry=rectangle, level=level)
            # If N has M entries. invoke OverflowTreatment with the level of N
            # as a parameter [for reinsertion or split]

    def choose_subtree(self, node, rectangle, level) -> Node:

        if level == list(self.overflow_flags)[-1]:
            return node

        min_heap = []
        heapq.heapify(min_heap)
        # CS2 If the child-pointers in N point to leaves
        if node.points_to_leaf():
            for middle_entry in node.entries:
                wrapper = MinHeap_overlap(middle_entry, rectangle)
                heapq.heappush(min_heap, wrapper)
        else:  # CS2 If the child-pointers in N do not point to leaves
            for middle_entry in node.entries:
                wrapper = MinHeap_areaExpansion(middle_entry, rectangle)
                heapq.heappush(min_heap, wrapper)

        best_entry = min_heap[0].entry
        return self.choose_subtree(node=best_entry.child_pointer, rectangle=rectangle, level=level + 1)

    def OverflowTreatment(self, node, new_entry, level) -> None:

        if node is not self.root and self.overflow_flags[level]:
            self.overflow_flags[level] = False
            self.ReInsert(node=node, new_entry=new_entry, level=level)
        else:
            self.split(node=node, new_entry=new_entry, level=level)

    def ReInsert(self, node, new_entry, level) -> None:

        distances = defaultdict(float)
        # RI1 For all M+l entries of a node N, compute the distance between the centers of their rectangles and the
        # center of the bounding rectangle of N
        for entry in node.entries:
            distances[entry] = math.dist(entry.MBR.get_center(), node.parent_entry.MBR.get_center())
        distances[new_entry] = math.dist(new_entry.MBR.get_center(), node.parent_entry.MBR.get_center())

        # RI2 Sort the entries m decreasing order of their distances computed m RI1
        distances = sorted(distances.items(), key=lambda item: item[1], reverse=True)

        # RI3 Remove the first p entries from N and adjust the bounding rectangle of N
        node.entries.clear()
        for wrapper in distances[int(node.MAX_DEGREE * 0.5):]:  # change after tests
            if not node.is_full():
                node.add_entry(wrapper[0])
            else:
                raise "no entries should be left behind"
        node.parent_entry.MBR = node.parent_entry.set_MBR()

        # RI4 In the sort, defined in RI2, starting with the maximum distance (= far reinsert) invoke Insert to
        # reinsert the entries
        for reinsert_entries in reversed(distances[:int(node.MAX_DEGREE * 0.5)]):
            self.Insert(rectangle=reinsert_entries[0], level=level)

    def split(self, node, new_entry, level) -> None:

        slit_axis = node.ChooseSpiltAxis(entry=new_entry)
        distribution1, distribution2 = Node.ChooseSpiltIndex(axis=slit_axis)

        if node.parent_entry is not None:
            parent_node = node.parent_entry.belonging_node

            for entry in parent_node.entries:
                if entry.child_pointer == node:
                    parent_node.entries.remove(entry)
                    break

            for dist in [distribution1, distribution2]:
                m = Middle_entry(belonging_node=parent_node)
                new_node = Node(entries=dist, parent_entry=m)
                m.set_pointer(child=new_node)

                if not parent_node.is_full():
                    parent_node.add_entry(entry=m)
                else:
                    self.OverflowTreatment(node=parent_node, new_entry=m, level=level)

        if node is self.root:
            self.total_levels += 1
            self.overflow_flags[self.total_levels] = True

            self.root = Node()

            m1 = Middle_entry(belonging_node=self.root)
            new_node1 = Node(entries=distribution1, parent_entry=m1)
            m1.set_pointer(child=new_node1)

            m2 = Middle_entry(belonging_node=self.root)
            new_node2 = Node(entries=distribution2, parent_entry=m2)
            m2.set_pointer(child=new_node2)

            self.root.add_entry(entry=m1)
            self.root.add_entry(entry=m2)

    def print_tree(self, node) -> None:
        if isinstance(node.entries[0], Record):
            for entry in node.entries:
                print(entry.cordinates)
        else:
            for entry in node.entries:
                print(f"Middle entry: {entry.MBR.get_points()}")
                self.print_tree(node=entry.child_pointer)
