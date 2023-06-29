from Node import Node
from Middle_entry import Middle_entry
from Record import Record
from Comparators import MinHeap_overlap, MinHeap_areaExpansion
from collections import defaultdict

import math
import heapq


class RTree:
    """
    The R-tree class containing all the in memory data and functions.
    """

    def __init__(self) -> None:
        self.root = None
        self.overflow_flags = {}
        self.total_levels = 1

    def Insert_data(self, rectangle) -> None:
        """
        Main function for inserting a new rectangle into the tree.

        :param rectangle:(Record) The multidimensional point.
        :return: None
        """
        if self.root is None:
            self.root = Node()
            self.overflow_flags[1] = False

        # ID1 Invoke Insert starting with the leaf level as a parameter, to Insert a new data rectangle
        self._Insert(rectangle=rectangle, level=1)

    def _Insert(self, rectangle, level) -> None:
        """
        Finds the appropriate leaf node for the rectangle to fit into.
        If the node N (returned node) is found, the entry is added to it; otherwise, the overflowTreatment is executed.

        :param rectangle:(Record) The multidimensional point.
        :param level:(int) The root level.
        :return: None
        """

        # I1 Invoke ChooseSubtree, with the level as parameter to find an appropriate node N in which to place the new
        # entry E
        N = self._choose_subtree(node=self.root, rectangle=rectangle, level=level)

        # I2 If N has less than M entries, accommodate rectangle in N
        if not N.is_full():
            N.add_entry(entry=rectangle)
        else:
            self._overflow_treatment(node=N, new_entry=rectangle, level=level)
            # If N has M entries. invoke OverflowTreatment with the level of N
            # as a parameter [for reinsertion or split]

    def _choose_subtree(self, node, rectangle, level) -> Node:
        """
        Recursively loop throw the tree(from top to bottom)and returns the best possible node for the rectangle to fit.
        Criteria to choose the node: -> Minimum overlap or minimum area expansion after the addition of the rectangle.

        :param node:(Node) The node we examine.
        :param rectangle:(Record) The multidimensional point.
        :param level:(int) The level of the node.
        :return:(Node) The best possible node.
        """

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
        return self._choose_subtree(node=best_entry.child_pointer, rectangle=rectangle, level=level + 1)

    def _overflow_treatment(self, node, new_entry, level) -> None:
        """
        Determines the method to be used when the new_entry cannot fit directly into the appropriate node.
        There are two ways to handle overflow:
        a) Split the node into two sub-nodes.
        b) Rearrange the node and reinsert the entry that was left behind into a better node if possible.

        :param node:(Node) The node with the maximum entries.
        :param new_entry:(Record | Middle_entry) The entry we want to add to the node.
        :param level:(int) The level of the node.
        :return: None
        """
        if node is not self.root and self.overflow_flags[level]:
            self.overflow_flags[level] = False
            self._re_insert(node=node, new_entry=new_entry, level=level)
        else:
            self._split(node=node, new_entry=new_entry, level=level)

    def _re_insert(self, node, new_entry, level) -> None:
        """
        Rearranging the entries of the node and inserting the one that was left out from the top to (possibly) prevent a
        potential split.

        :param node: (Node) The node with the maximum entries.
        :param new_entry:(Record | Middle_entry) The entry we want to add to the node.
        :param level:(int) The level of the node.
        :return: None
        """

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
            self._Insert(rectangle=reinsert_entries[0], level=level)

    def _split(self, node, new_entry, level) -> None:
        """
        Performs a split on the node based on the distributions returned from the ChooseSplitIndex() function.
        If the split occurs on the root node, the overall level of the tree is increased by one.

        :param node:(Node) The node with the maximum entries.
        :param new_entry:(Record | Middle_entry) The entry we want to add to the node.
        :param level:(int) The level of the node.
        :return: None
        """

        # S1 Invoke ChooseSplitAxis to determine the axis, perpendicular to which the split is performed
        slit_axis = node.ChooseSpiltAxis(entry=new_entry)
        # S2 Invoke ChooseSpiltIndex to determine the best distribution into two groups along that axis
        distribution1, distribution2 = Node.ChooseSpiltIndex(axis=slit_axis)
        # S3 Distribute the entries into two groups

        if node.parent_entry is not None:
            parent_node = node.parent_entry.belonging_node

            # Delete the node from its parent entries.
            for entry in parent_node.entries:
                if entry.child_pointer == node:
                    parent_node.entries.remove(entry)
                    break
            # Creates and adds the two new split nodes to the ":param node" parent entries.
            for dist in [distribution1, distribution2]:
                m = Middle_entry(belonging_node=parent_node)
                new_node = Node(entries=dist, parent_entry=m)
                m.set_pointer(child=new_node)

                if not parent_node.is_full():
                    parent_node.add_entry(entry=m)
                else:
                    # If parent node is full.
                    self._overflow_treatment(node=parent_node, new_entry=m, level=level)

        # Perform a split on the root node
        if node is self.root:
            self.total_levels += 1
            self.overflow_flags[self.total_levels] = True

            # Create new root
            self.root = Node()

            m1 = Middle_entry(belonging_node=self.root)
            new_node1 = Node(entries=distribution1, parent_entry=m1)
            m1.set_pointer(child=new_node1)

            m2 = Middle_entry(belonging_node=self.root)
            new_node2 = Node(entries=distribution2, parent_entry=m2)
            m2.set_pointer(child=new_node2)

            self.root.add_entry(entry=m1)
            self.root.add_entry(entry=m2)

    def delete_record(self, rectangle) -> None:
        """
        Finds and removes the given rectangle from the tree if it exists.

        :param rectangle:(Record) The multidimensional point.
        :return: None
        """
        N = self._find_leaf(node=self.root, entry=rectangle, level=1, Q=[])
        if N is None:
            print("Record doesn't exist!")
            return
        for entry in N.entries:
            if entry.compair_records(rectangle):
                N.entries.remove(entry)
                self._condense_tree(N, [])

    def _find_leaf(self, node, entry, level, Q) -> Node:
        """
        Used by the delete_record() function to find and return the leaf node where the rectangle is stored,
        if it exists. It is based on recursion.

        :param node:(Node) The root node.
        :param entry:(Record) The rectangle we want to delete.
        :param level:(int) The root level.
        :param Q:(list) And empty list for adding the visited entries.
        :return:(Node) The leaf node where entry is stored.
        """
        if isinstance(node.entries[0], Record):
            for e in node.entries:
                if e.compair_records(entry):
                    return node
            else:
                return self._find_leaf(node=node.parent_entry.belonging_node, entry=entry, level=level - 1, Q=Q)
        else:
            for e in node.entries:
                if e not in Q:
                    Q.append(e)
                else:
                    continue
                if e.MBR.rectangles_overlap(entry):
                    return self._find_leaf(node=e.child_pointer, entry=entry, level=level + 1, Q=Q)
            else:
                if node.parent_entry is not None:
                    return self._find_leaf(node=node.parent_entry.belonging_node, entry=entry, level=level - 1, Q=Q)

    def _condense_tree(self, N, Q):
        """
        Given a leaf node N from which an entry has been deleted, eliminate the node if it has too few entries and
        relocate its entries.
        Propagate node elimination upward as necessary.
        Adjust all covering rectangles on the path to the root.

        :param N: (Node) The leaf node where entry is stored.
        :param Q: (list) An empty list.
        :return: None
        """
        if N is self.root:
            for node in Q:
                for entry in node.entries:
                    self.Insert_data(entry)
        else:
            P = N.parent_entry.belonging_node
            En = N.parent_entry
            if len(N.entries) < N.MIN_FILL_FACTOR:
                P.remove_entry(En)
                Q.append(N)
            else:
                En.MBR = En.set_MBR()
            self._condense_tree(P, Q)

    def print_tree(self, node, level=1) -> None:
        """
        Recursively prints out the nodes and their entries of the tree based on the DFS algorithm.

        :param node: (Node) The root node.
        :param level: (int) The root level.
        :return: None
        """
        if isinstance(node.entries[0], Record):
            for entry in node.entries:
                print(f"{entry.cordinates}, level: {level}")
        else:
            for entry in node.entries:
                print(f"Middle entry: {entry.MBR.get_points()}, level: {level}")
                self.print_tree(node=entry.child_pointer, level=level + 1)
