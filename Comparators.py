from functools import total_ordering


@total_ordering
class MinHeap_overlap:
    """
    A wrapper class used in a minimum heap structure to keep the entry with the least overlap enlargement in the
    first place when a rectangle is about to get added.
    """

    def __init__(self, entry, rectangle, is_group=False) -> None:
        self.entry = entry
        self.rectangle = rectangle
        self.distribution = None

        # is_group is a boolean value that tells us if the structure is used for calculating the distributions of the
        # entries if a node is about to split.
        if is_group:
            self.distribution = entry
            self.entry = entry[0]
            self.rectangle = entry[1]

    def __lt__(self, other) -> bool:
        """
        Overrides the less than operator to compare the inserted objects first by their overlap, then by their area
        expansion, and lastly by their total area.

        :param other: (MinHeap_overlap) The entry we comparing it to.
        :return: (Boolean)
        """
        if self.entry.MBR.calculate_overlap(self.rectangle) > other.rectangle.MBR.calculate_overlap(self.rectangle):
            return True

        elif self.entry.MBR.calculate_overlap(self.rectangle) == other.rectangle.MBR.calculate_overlap(self.rectangle):
            if self.entry.MBR.calculate_area_expansion(self.rectangle) > other.rectangle.MBR.calculate_area_expansion(
                    self.rectangle):
                return True

            elif self.entry.MBR.calculate_area_expansion(
                    self.rectangle) == other.rectangle.MBR.calculate_area_expansion(self.rectangle):
                if self.entry.MBR.get_area() > other.rectangle.MBR.get_area():
                    return True
        return False


@total_ordering
class MinHeap_areaExpansion:
    """
    A wrapper class used in a minimum heap structure to keep the entry with the least overlap enlargement in the
    first place when a rectangle is about to get added.
    """
    def __init__(self, entry, rectangle) -> None:
        self.entry = entry
        self.rectangle = rectangle

    def __lt__(self, other) -> float:
        """
        Overrides the less than operator to compare the inserted objects first by their area expansion and after by
        their total area.

        :param other: (MinHeap_areaExpansion) The entry we comparing it to.
        :return: (Boolean)
        """
        if self.entry.MBR.calculate_area_expansion(self.rectangle) > other.rectangle.MBR.calculate_area_expansion(
                self.rectangle):
            return True

        elif self.entry.MBR.calculate_area_expansion(self.rectangle) == other.rectangle.MBR.calculate_area_expansion(
                self.rectangle):
            if self.entry.MBR.get_area() > other.rectangle.MBR.get_area():
                return True

        return False
