import numpy as np
from R_star_tree import RTree
from Comparators import Wrapper
from Knn import Knn
from Range_query import range_query
import main
from matplotlib import pyplot as plt
from Record import Record
import file_handler
import re

import seaborn as sns
import heapq
import math
import sys
import time


class Sequential_scan:
    """
    This class contains the necessary attributes and functions for the execution of a sequential scan knn and
    sequential scan range queries.
    """

    def __init__(self):
        self.min_heap = []
        self.discovered_points = []
        heapq.heapify(self.min_heap)

    def sequential_knn(self, point, k_neighbors, number_of_entries=None):
        """
        Sequentially reads all the data or a specified number of entries from the datafile.bin and calculates the
        K-Nearest Neighbors.

        :param point: (tuple) The point for which we want to calculate its nearest neighbors.
        :param k_neighbors: (int) The number of neighbors.
        :param number_of_entries: (int) The number of entries to be read from the file.
        :return: (None)
        """

        current_location = []
        for counter, location in enumerate(file_handler.read_file("secondary memory files/datafile.bin")):

            if number_of_entries is not None and counter >= number_of_entries: break
            if re.search('^Block+', str(location)):
                continue
            else:
                current_location.append(location)

                if len(current_location) == 3:
                    entry = Record("-", "-", (current_location[1], current_location[2])).cordinates
                    dist = math.dist(point, entry)
                    wrapper = Wrapper(distance=dist, entry=entry)
                    heapq.heappush(self.min_heap, wrapper)

                    current_location.clear()

        self.discovered_points = heapq.nsmallest(k_neighbors, self.min_heap)

    def sequential_range(self, point, radius, number_of_entries=None):
        """
        Sequentially reads all the data or a specified number of entries from the datafile.bin and calculates all the
        points that are inside the radius from the center point.

        :param point: (tuple) The central point .
        :param radius: (int) The range from central point.
        :param number_of_entries: (int) The number of entries to be read from the file.
        :return: (None)
        """

        current_location = []
        for counter, location in enumerate(file_handler.read_file("secondary memory files/datafile.bin")):

            if number_of_entries is not None and counter >= number_of_entries: break
            if re.search('^Block+', str(location)):
                continue
            else:
                current_location.append(location)

                if len(current_location) == 3:
                    entry = Record("-", "-", (current_location[1], current_location[2])).cordinates
                    dist = math.dist(point, entry)
                    if dist <= radius:
                        wrapper = Wrapper(distance=dist, entry=entry)
                        heapq.heappush(self.min_heap, wrapper)

                    current_location.clear()


def plot_knn_vs_sequential(tree):
    """
    Measures and plots the elapsed time of knn queries for different number of neighbors.

    :param tree:(RTree) An instance of the R-tree.
    :return: (None)
    """
    fig, ax = plt.subplots()
    sns.set_style("whitegrid")
    main.read_location(tree, None)
    number_of_neighbors = [i for i in range(10, 1000)]
    times = []

    for k in number_of_neighbors:
        start = time.time()
        query = Sequential_scan()
        query.sequential_knn(point=(40.5872698, 22.9706448), k_neighbors=k, number_of_entries=None)
        end = time.time()
        times.append(end - start)

    sns.lineplot(x=number_of_neighbors, y=times, markers=True, color="tab:red", ax=ax)
    plt.legend(["Sequential"])
    ax2 = ax.twinx()

    times = []
    for k in number_of_neighbors:
        start = time.time()
        query = Knn(point=(40.5872698, 22.9706448), k_neighbors=k)
        query.Knn_query(Tree.root)
        end = time.time()
        times.append(end - start)

    sns.lineplot(x=number_of_neighbors, y=times, markers=True, color="tab:orange", ax=ax2)

    plt.title("Time per query")
    plt.xlabel("Value of radius")
    plt.ylabel("Time in seconds")
    plt.legend(["R* tree"], loc='upper left')
    plt.show()


def plot_range_vs_sequential(tree):
    """
    Measures and plots the elapsed time of range queries for different radius values.

    :param tree: (RTree) An instance of the R-tree.
    :return: (None)
    """
    fig, ax = plt.subplots()
    sns.set_style("whitegrid")
    main.read_location(tree, None)
    radius_values = [i for i in np.arange(0, .01, .00005)]
    times = []

    for radius in radius_values:
        start = time.time()
        query = Sequential_scan()
        query.sequential_range(point=(40.5872698, 22.9706448), radius=radius, number_of_entries=None)
        end = time.time()
        times.append(end - start)

    sns.lineplot(x=radius_values, y=times, markers=True, color="tab:red", ax=ax)
    plt.legend(["Sequential"])
    ax2 = ax.twinx()

    times = []
    for radius in radius_values:
        start = time.time()
        query = range_query(point=(40.5872698, 22.9706448), radius=radius)
        query.search(tree.root)
        end = time.time()
        times.append(end - start)

    sns.lineplot(x=radius_values, y=times, markers=True, color="tab:orange", ax=ax2)

    plt.title("Time per query")
    plt.xlabel("Value of radius")
    plt.ylabel("Time in seconds")
    plt.legend(["R* tree"], loc='upper left')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments!")
    elif len(sys.argv) == 1:
        raise ValueError("Νo dimension number entered!")

    Tree = RTree()
    #plot_knn_vs_sequential(Tree)
    plot_range_vs_sequential(Tree)
