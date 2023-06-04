from MBR import MBR


class Split_group:
    def __init__(self, group):
        self.entries = group
        self.MBR = self.set_MBR()

    def set_MBR(self):
        total_points = []
        for point in self.entries:
            point1, point2 = point.MBR.get_points()
            total_points.append(point1)
            total_points.append(point2)

        return MBR(total_points)


"""
from hilbertcurve.hilbertcurve import HilbertCurve

# Create a Hilbert curve object
hilbert_curve = HilbertCurve(1, 2)
distances = hilbert_curve.distances_from_points([(1, 1)])
print(distances)
"""