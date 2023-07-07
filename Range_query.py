from Record import Record
from R_star_tree import RTree
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import sys
import main
import time
import math


class range_query:
    """
    This class contains the necessary attributes and functions for the execution of a range query.
    """

    def __init__(self, point, radius):
        self.search_point = point
        self.range_from_point = radius
        self.discovered_points = []

    def search(self, node):
        """
        Given the root node of an R-tree or any other middle node, recursively calculates all the points that are
        inside the radius from the center point and stores them into the self.discovered_points list.

        :param node: (Node) The root or any middle node.
        :return: None
        """
        if isinstance(node.entries[0], Record):
            for entry in node.entries:
                if math.dist(self.search_point, entry.cordinates) <= self.range_from_point:
                    self.discovered_points.append(entry)
        else:
            for entry in node.entries:
                if entry.MBR.overlaps_with_point(self.search_point, self.range_from_point):
                    self.search(entry.child_pointer)


def time_difference_plot(tree) -> None:
    """
    Measures and plots the elapsed time of range queries for different radius values.

    :param tree:(RTree) An instance of the R-tree.
    :return: (None)
    """
    sns.set_style("whitegrid")
    main.read_location(tree, 1000)
    radius_values = [i for i in np.arange(0, .1, .0005)]
    times = []

    for radius in radius_values:
        start = time.time()
        query = range_query(point=(40.5872698, 22.9706448), radius=radius)
        query.search(tree.root)
        end = time.time()
        times.append(end - start)
    sns.lineplot(x=radius_values, y=times, markers=True, color="red")
    plt.title("Time per query")
    plt.xlabel("Value of radius")
    plt.ylabel("Time in seconds")
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments!")
    elif len(sys.argv) == 1:
        raise ValueError("Νo dimension number entered!")

    # Range query example
    Tree = RTree()
    # time_difference_plot(Tree)

    print("\n----------Range Query----------")

    data = [(1, 1), (1, 2), (4, 1), (4, 2), (5, 1), (5, 2)]
    for record in data:
         Tree.Insert_data(Record(1, 1, (record[0], record[1])))
    query = range_query(point=(2, 1), radius=2)
    query.search(Tree.root)

    print(f"Points inside the radius : {[i.cordinates for i in query.discovered_points]}")
    print("------End of the Query-------")
