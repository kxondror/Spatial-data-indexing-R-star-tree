from R_star_tree import RTree
from Record import Record
from Comparators import Wrapper
from matplotlib import pyplot as plt
import main
import seaborn as sns
import heapq
import math
import sys
import time


class Knn:
    """
    This class contains the necessary attributes and functions for the execution of a K-Nearest Neighbors query.
    """

    def __init__(self, point, k_neighbors):
        self.point = point
        self.K = k_neighbors

        self.result_neighbors = []
        self.min_heap = []
        heapq.heapify(self.min_heap)

    def Knn_query(self, root):
        """
        Based on the data inside the minimum heap, retains the K records with the smallest distance.

        :param root: (Node) The root of the tree.
        :return: (None)
        """
        self._traverse_tree(root)
        while len(self.result_neighbors) < self.K and self.min_heap:
            wrapper = heapq.heappop(self.min_heap)
            if isinstance(wrapper.entry, Record):
                self.result_neighbors.append((wrapper.entry, wrapper.distance))
            else:
                self._traverse_tree(wrapper.entry.child_pointer)

    def _traverse_tree(self, node):
        """
        Given a node of the R-tree, calculates the distances of an MBR or Record from the central point and adds it
        to the heap.

        :param node: (Node) Any node from the R* tree.
        :return: None
        """
        if isinstance(node.entries[0], Record):
            for entry in node.entries:
                dist = entry.MBR.min_dist(self.point)
                wrapper = Wrapper(distance=dist, entry=entry)
                heapq.heappush(self.min_heap, wrapper)
        else:
            for entry in node.entries:
                center = entry.MBR.get_center()
                dist = math.dist(self.point, center)
                wrapper = Wrapper(distance=dist, entry=entry)
                heapq.heappush(self.min_heap, wrapper)


def time_difference_plot(tree) -> None:
    """
    Measures and plots the elapsed time of knn queries for different number of neighbors.

    :param tree:(RTree) An instance of the R-tree.
    :return: (None)
    """
    sns.set_style("whitegrid")
    main.read_location(tree, None)
    number_of_neighbors = [i for i in range(10, 5000)]
    times = []

    for k in number_of_neighbors:
        start = time.time()
        query = Knn(point=(40.5872698, 22.9706448), k_neighbors=k)
        query.Knn_query(Tree.root)
        end = time.time()
        times.append(end - start)
    sns.lineplot(x=number_of_neighbors, y=times, markers=True, color="red")
    plt.title("Time per query")
    plt.xlabel("Number of neighbors")
    plt.ylabel("Time in seconds")
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments!")
    elif len(sys.argv) == 1:
        raise ValueError("Νo dimension number entered!")

    # Knn example query
    Tree = RTree()
    # time_difference_plot(Tree)

    print("\n----------Knn Query----------")
    data = [(1, 1), (1, 2), (4, 1), (4, 2), (5, 1), (5, 2)]
    for record in data:
        Tree.Insert_data(Record(1, 1, (record[0], record[1])))
    query = Knn(point=(2, 1), k_neighbors=4)
    query.Knn_query(Tree.root)

    print(f"Nearest points : {[i[0].cordinates for i in query.result_neighbors]}")
    print("------End of the Knn query-------")
