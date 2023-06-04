from functools import total_ordering


@total_ordering
class MinHeap_overlap:
    def __init__(self, entry, rectangle, isgroup=False):
        self.entry = entry
        self.rectangle = rectangle
        self.distribution = None

        if isgroup:
            self.distribution = entry
            self.entry = entry[0]
            self.rectangle = entry[1]

    def __lt__(self, other):

        if self.entry.MBR.calculate_overlap(self.rectangle) > other.rectangle.MBR.calculate_overlap(self.rectangle):
            return True

        elif self.entry.MBR.calculate_overlap(self.rectangle) == other.rectangle.MBR.calculate_overlap(self.rectangle):
            if self.entry.MBR.calculate_area_expansion(self.rectangle) >  other.rectangle.MBR.calculate_area_expansion(self.rectangle):
                return True

            elif self.entry.MBR.calculate_area_expansion(self.rectangle) == other.rectangle.MBR.calculate_area_expansion(self.rectangle):
                if self.entry.MBR.get_area() > other.rectangle.MBR.get_area():
                    return True
        return False


@total_ordering
class MinHeap_areaExpansion:
    def __init__(self, entry, rectangle):
        self.entry = entry
        self.rectangle = rectangle

    def __lt__(self, other):
        if self.entry.MBR.calculate_area_expansion(self.rectangle) > other.rectangle.MBR.calculate_area_expansion(self.rectangle):
            return True

        elif self.entry.MBR.calculate_area_expansion(self.rectangle) == other.rectangle.MBR.calculate_area_expansion(self.rectangle):
            if self.entry.MBR.get_area() > other.rectangle.MBR.get_area():
                return True
            
        return False

"""
node1 = Node(0)
node1.add_entry(Record(2, 1, [0, 2]))
node1.add_entry(Record(2, 1, [3, 4]))
node1.update_MBR()

node2 = Node(0)
node2.add_entry(Record(2, 1, [4, 2]))
node2.add_entry(Record(2, 1, [8, 4]))
node2.update_MBR()


maxHeap = []
heapq.heapify(maxHeap)

heapq.heappush(maxHeap, MinHeap_overlap(node1, MBR([[5, 3], [4, 2]])))
heapq.heappush(maxHeap, MinHeap_overlap(node2, MBR([[5, 3], [4, 2]])))

if len(maxHeap) > 1:
    heapq.heappop(maxHeap)

for i in maxHeap:
    print(i.node.MBR.get_points())
"""