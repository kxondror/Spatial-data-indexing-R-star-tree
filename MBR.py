class MBR:
    def __init__(self, points):
        self.points = points
        self.bottom_left, self.upper_right = MBR.min_bounding_box(self)

    def get_points(self):
        return self.bottom_left, self.upper_right

    def get_center(self):
        center = [(self.bottom_left[i] + self.upper_right[i]) / 2 for i in range(2)]
        return center

    def get_margin(self):
        margin = 0
        for dim in range(2):
            margin += abs(self.upper_right[dim] - self.bottom_left[dim])
        return margin

    def get_area(self):
        bottom_right = [self.upper_right[0], self.bottom_left[1]]
        upper_left = [self.bottom_left[0], self.upper_right[1]]

        x = bottom_right[0] - self.bottom_left[0]
        y = upper_left[1] - self.bottom_left[1]
        return x * y

    def calculate_area_expansion(self, entry):
        new_bl, new_ur = entry.MBR.get_points()

        if self.bottom_left[1] <= new_bl[1] <= self.upper_right[1] and \
                self.bottom_left[0] <= new_ur[0] <= self.upper_right[0]:
            return 0

        temp_points = [point for point in self.get_points()]
        temp_points.append(new_bl)
        temp_points.append(new_ur)
        temp = MBR(temp_points)
        return temp.get_area() - self.get_area()

    def calculate_overlap(self, entry):
        new_bl, new_ur = entry.MBR.get_points()

        x_overlap = max(0, min(self.upper_right[0], new_ur[0]) - max(self.bottom_left[0], new_bl[0]))
        y_overlap = max(0, min(self.upper_right[1], new_ur[1]) - max(self.bottom_left[1], new_bl[1]))

        return x_overlap * y_overlap

    def min_bounding_box(self):
        upper_right = []
        bottom_left = []

        # for 2d points
        for index in range(2):
            upper_right.append(max([point[index] for point in self.points]))
            bottom_left.append(min([point[index] for point in self.points]))

        return tuple(bottom_left), tuple(upper_right)
