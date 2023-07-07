import sys
import math


class MBR:
    """
    Class representing the minimum bounding rectangle of an entry.
    """

    def __init__(self, points) -> None:
        self.points = points
        self.bottom_left, self.upper_right = MBR.min_bounding_box(self)

    def get_points(self) -> tuple:
        """
        Getter for the Bottom left and upper_right points of the rectangle.

        :return: (tuple) The point points
        """
        return self.bottom_left, self.upper_right

    def get_center(self) -> list:
        """
        Calculates and returns the center of the MBR.

        :return: (int) The center point.
        """
        center = [(self.bottom_left[dimension] + self.upper_right[dimension]) / int(sys.argv[1]) for dimension in
                  range(int(sys.argv[1]))]
        return center

    def get_area(self) -> float:
        """
        Calculates and returns the total area of the MBR.

        :return: (int) The total area.
        """
        bottom_right = list(self.upper_right)
        upper_left = list(self.bottom_left)

        # Update the coordinates based on the number of dimensions
        for dimension in range(int(sys.argv[1])):
            bottom_right[dimension] = self.upper_right[dimension]
            upper_left[dimension] = self.bottom_left[dimension]

        # Calculate the differences in each dimension
        differences = [bottom_right[dimension] - self.bottom_left[dimension] for dimension in range(int(sys.argv[1]))]

        # Calculate the total area by multiplying the differences
        area = 1
        for difference in differences:
            area *= difference

        return area

    def calculate_area_expansion(self, entry) -> float:
        """
        Calculates and returns the extra area that will be added to the MBR if we add a new entry.

        :param entry: (Middle_entry | Record) The entry we want to add.
        :return: (int) The total area expansion.
        """
        new_bl, new_ur = entry.MBR.get_points()

        for dimension in range(int(sys.argv[1])):
            if not (self.bottom_left[dimension] <= new_bl[dimension] <= self.upper_right[dimension]) or \
                    not (self.bottom_left[dimension] <= new_ur[dimension] <= self.upper_right[dimension]):
                temp_points = [point for point in self.get_points()]
                temp_points.append(new_bl)
                temp_points.append(new_ur)
                temp = MBR(temp_points)
                return temp.get_area() - self.get_area()

        return 0

    def calculate_overlap(self, entry) -> float:
        """
        Calculates and returns the overlap between the two MBRs (self.MBR and entry.MBR).

        :param entry: (Middle_entry | Record) The entry we want to add.
        :return: (int) The total overlap value.
        """
        new_bl, new_ur = entry.MBR.get_points()

        overlap_product = 1
        for dimension in range(int(sys.argv[1])):
            overlap = max(0, min(self.upper_right[dimension], new_ur[dimension]) - max(self.bottom_left[dimension],
                                                                                       new_bl[dimension]))
            overlap_product *= overlap

        return overlap_product

    def rectangles_overlap(self, entry) -> bool:
        """
        Checks if the entry's MBR coming from the argument , overlaps with the self one.

        :param entry: (Middle_entry | Record) The entry we want check for overlapping.
        :return: (bool) True if the MBRs are overlapping; otherwise False
        """
        for dimension in range(int(sys.argv[1])):
            if self.upper_right[dimension] >= entry.MBR.bottom_left[dimension] and \
                    self.bottom_left[dimension] <= entry.MBR.upper_right[dimension]:
                continue
            else:
                return False
        return True

    def min_dist(self, point) -> float:
        """
        Calculates and returns the Minimum distance (mindist) between the self Mbr and the argument point.
        Concept described here: https://www.cs.mcgill.ca/~fzamal/Project/concepts.htm

        :param point: (tuple) The point we want to calculate the distance from.
        :return: (float) The minimum distance.
        """
        minDistance = 0

        for dimension in range(int(sys.argv[1])):
            if self.bottom_left[dimension] > point[dimension]:
                rd = self.bottom_left[dimension]
            elif self.upper_right[dimension] < point[dimension]:
                rd = self.upper_right[dimension]
            else:
                rd = point[dimension]
            minDistance += math.pow(point[dimension] - rd, 2)

        return math.sqrt(minDistance)

    def overlaps_with_point(self, point, radius) -> bool:
        """
        Checks if the distance from the given point to the self rectangle is less or equal to the radius parameter.

        :param point: (tuple) The center point of the range query.
        :param radius: (float) The radius of the circle for the range query.
        :return: True if the point-rectangle distance is less than or equal to the radius; otherwise False.
        """
        minDistance = self.min_dist(point)
        return True if minDistance <= radius else False

    def min_bounding_box(self) -> tuple:
        """
        Calculates and returns the minimum bounding rectangle points (bottom_left and upper_right) based on the total
        points we provide.

        :return: (tuple) The two corner points.
        """
        upper_right = []
        bottom_left = []

        for index in range(int(sys.argv[1])):
            upper_right.append(max([point[index] for point in self.points]))
            bottom_left.append(min([point[index] for point in self.points]))

        return tuple(bottom_left), tuple(upper_right)
