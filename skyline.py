from R_star_tree import RTree
from Record import Record
from Comparators import Wrapper
import numpy as np
import heapq
import sys


class skyline:
    """
    This class contains the necessary attributes and functions for the execution of a skyline query.
    """
    def __init__(self):

        self.min_heap = []
        heapq.heapify(self.min_heap)
        self.discovered_points = []

    def skyline_query(self, node):
        """
        Given the root node of an R-tree or any other middle node, recursively calculates all the skyline points
        below the given node and stores them into the self.discovered_points list.

        :param node: (Node) The root or any middle node.
        :return: None
        """
        for entry in node.entries:
            wrapper = Wrapper(distance=self._CityBlock_distance(entry.MBR), entry=entry)
            heapq.heappush(self.min_heap, wrapper)

        while len(self.min_heap) > 0:
            best_entry = heapq.heappop(self.min_heap).entry
            if isinstance(best_entry, Record):
                if not self._is_dominated(best_entry):
                    self.discovered_points.append(best_entry)
            else:
                self.skyline_query(best_entry.child_pointer)

    @staticmethod
    def _CityBlock_distance(mbr) -> int:
        """
        Calculates and returns the city block (L1) distance between the given minimum bounding rectangles (MBRs),
        bottom left point and the initial axis point (0,0).

        :param mbr: (MBR) The MBR of an entry.
        :return: (int) The L1 distance.
        """
        result = np.sum([abs(a - b) for (a, b) in zip((0, 0), mbr.bottom_left)])
        return int(result)

    def _is_dominated(self, data_point):
        """
        Checks whether the given data point is dominated (has larger value in each dimension) between every other
        skyline point.

        :param data_point: (Record) The data point.
        :return: (Boolean) True if it's dominated; otherwise False.
        """
        for skyline_point in self.discovered_points:
            counter = 0
            for count, value in enumerate(data_point.cordinates):
                if value >= skyline_point.cordinates[count]:
                    counter += 1
            if counter == len(data_point.cordinates):
                return True
        return False


if __name__ == '__main__':

    if len(sys.argv) > 2:
        raise ValueError("Too many arguments!")
    elif len(sys.argv) == 1:
        raise ValueError("Νo dimension number entered!")

    # Example based on the e-learning Skyline slides.
    Tree = RTree()

    data = [(1, 9), (2, 10), (3, 2), (4, 3), (4, 8), (5, 6), (6, 2), (6, 7), (7, 5), (8, 3), (9, 1), (10, 4)]
    for record in data:
        Tree.Insert_data(Record(None, None, (record[0], record[1])))
    Tree.print_tree(Tree.root)

    print("\n----------skyline----------")
    query = skyline()
    query.skyline_query(Tree.root)
    print(f"skyline points : {[i.cordinates for i in query.discovered_points]}")
    print("------end of skyline-------")
