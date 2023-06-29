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
        center = [(self.bottom_left[i] + self.upper_right[i]) / 2 for i in range(2)]
        return center

    def get_area(self) -> float:
        """
        Calculates and returns the total area of the MBR.

        :return: (int) The total area.
        """
        bottom_right = [self.upper_right[0], self.bottom_left[1]]
        upper_left = [self.bottom_left[0], self.upper_right[1]]

        x = bottom_right[0] - self.bottom_left[0]
        y = upper_left[1] - self.bottom_left[1]
        return x * y

    def calculate_area_expansion(self, entry) -> float:
        """
        Calculates and returns the extra area that will be added to the MBR if we add a new entry.

        :param entry: (Middle_entry | Record) The entry we want to add.
        :return: (int) The total area expansion.
        """
        new_bl, new_ur = entry.MBR.get_points()

        if self.bottom_left[1] <= new_bl[1] <= self.upper_right[1] and \
                self.bottom_left[0] <= new_ur[0] <= self.upper_right[0]:
            return 0

        temp_points = [point for point in self.get_points()]
        temp_points.append(new_bl)
        temp_points.append(new_ur)
        temp = MBR(temp_points)
        return temp.get_area() - self.get_area()

    def calculate_overlap(self, entry) -> float:
        """
        Calculates and returns the overlap between the two MBRs (self.MBR and entry.MBR).

        :param entry: (Middle_entry | Record) The entry we want to add.
        :return: (int) The total overlap value.
        """
        new_bl, new_ur = entry.MBR.get_points()

        x_overlap = max(0, min(self.upper_right[0], new_ur[0]) - max(self.bottom_left[0], new_bl[0]))
        y_overlap = max(0, min(self.upper_right[1], new_ur[1]) - max(self.bottom_left[1], new_bl[1]))

        return x_overlap * y_overlap

    def rectangles_overlap(self, entry):

        for i in range(len(self.upper_right)):
            if self.upper_right[i] >= entry.MBR.bottom_left[i] and \
                    self.bottom_left[i] <= entry.MBR.upper_right[i]:
                continue
            else:
                return False
        return True

    def min_bounding_box(self) -> tuple:
        """
        Calculates and returns the minimum bounding rectangle points (bottom_left and upper_right) based on the total
        points we provide.

        :return: (tuple) The two corner points.
        """
        upper_right = []
        bottom_left = []

        for index in range(2):
            upper_right.append(max([point[index] for point in self.points]))
            bottom_left.append(min([point[index] for point in self.points]))

        return tuple(bottom_left), tuple(upper_right)
