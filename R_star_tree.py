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
        self.total_levels = 1

    def Insert_data(self, rectangle):
        if self.root is None:
            self.root = Node(level=1)
            self.overflow_flags[self.root.level] = True

        # ID1 Invoke Insert starting with the leaf level as a parameter, to Insert a new data rectangle
        self.Insert(rectangle)

    def Insert(self, rectangle):

        # I1 Invoke ChooseSubtree. with the level as a parameter,to find an appropriate node N in which to place the
        # new entry E

        N = self.choose_subtree(self.root, rectangle)

        # I2 If N has less than M entries, accommodate rectangle in N
        if not N.is_full():
            N.add_entry(rectangle, self.total_levels)
        else:
            self.OverflowTreatment(node=N, new_entry=rectangle)
            # If N has M entries. invoke OverflowTreatment with the level of N
            # as a parameter [for reinsertion or split]

    def choose_subtree(self, node, rectangle):

        if node.level == self.total_levels:
            return node

        else:
            min_heap = []
            heapq.heapify(min_heap)
            # CS2 If the child-pointers in N point to leaves
            if node.level == (self.total_levels - 1):
                for middle_entry in node.entries:
                    wrapper = MinHeap_overlap(middle_entry, rectangle)
                    heapq.heappush(min_heap, wrapper)
            else:  # CS2 If the child-pointers in N do not point to leaves
                for middle_entry in node.entries:
                    wrapper = MinHeap_areaExpansion(middle_entry, rectangle)
                    heapq.heappush(min_heap, wrapper)

            best_entry = min_heap[0].entry
            return self.choose_subtree(best_entry.child_pointer, rectangle)

    def OverflowTreatment(self, node, new_entry):

        if node.level != 1 and self.overflow_flags[node.level]:
            self.overflow_flags[node.level] = False
            self.ReInsert(node, new_entry)
        else:
            self.split(node, new_entry)

    def ReInsert(self, node, new_entry):

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
        for wrapper in distances[int(node.MAX_DEGREE * 0.4):]:
            if not node.is_full():
                node.add_entry(wrapper[0], self.total_levels)
            else:
                raise "no entries should be left behind"

        node.parent_entry.MBR = node.parent_entry.set_MBR()

        # RI4 In the sort, defined in RI2, starting with the maximum distance (= far reinsert) invoke Insert to
        # reinsert the entries
        for reinsert_entries in reversed(distances[:int(node.MAX_DEGREE * 0.4)]):
            self.Insert(reinsert_entries[0])

    def split(self, node, new_entry):

        slit_axis = node.ChooseSpiltAxis(new_entry)
        distribution1, distribution2 = node.ChooseSpiltIndex(slit_axis)

        if node.level != 1: #not the root
            parent_node = node.parent_entry.belonging_node

            for entry in parent_node.entries:
                if entry.child_pointer == node:
                    parent_node.entries.remove(entry)
                    break

            for dist in [distribution1, distribution2]:
                m = Middle_entry(belonging_node=parent_node)
                new_node = Node(level=node.level, entries=dist, parent_entry=m)
                m.set_pointer(new_node)

                if not parent_node.is_full():
                    parent_node.add_entry(m, self.total_levels)
                else:
                    self.OverflowTreatment(parent_node, m)

        else:# split happens on the root
            self.total_levels += 1
            self.overflow_flags[self.total_levels] = True

            self.root = Node(level=1)

            m1 = Middle_entry(belonging_node=self.root)
            new_node1 = Node(level=(self.root.level + 1), entries=distribution1, parent_entry=m1)

            Node.update_levels_topdown(new_node1, self.total_levels)
            m1.set_pointer(new_node1)

            m2 = Middle_entry(belonging_node=self.root)
            new_node2 = Node(level=(self.root.level + 1), entries=distribution2, parent_entry=m2)
            Node.update_levels_topdown(new_node2, self.total_levels)
            m2.set_pointer(new_node2)

            self.root.add_entry(m1, self.total_levels)
            self.root.add_entry(m2, self.total_levels)


    def print_tree(self, node):
        if node.level == self.total_levels:
            for entry in node.entries:
                print(entry.cordinates, "level:", node.level)
        else:
            for entry in node.entries:
                print(f"Middle entry: {entry.MBR.get_points()} ,level :{node.level}")
                self.print_tree(entry.child_pointer)
    """

    def print_tree(self, node):
        for entry in node.entries:
            if isinstance(entry, Middle_entry):
                print(f"Middle entry: {entry.MBR.get_points()} ,level :{node.level}")
                self.print_tree(entry.child_pointer)
            else:
                print(entry.cordinates, "level:", node.level)
    """