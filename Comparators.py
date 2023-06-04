from functools import total_ordering


@total_ordering
class MinHeap_overlap:
    def __init__(self, node, entry, isgroup=False):
        self.node = node
        self.entry = entry
        self.distribution = None

        if isgroup:
            self.distribution = node
            self.node = node[0]
            self.entry = node[1]

    def __lt__(self, other):

        if self.node.MBR.calculate_overlap(self.entry) > other.node.MBR.calculate_overlap(self.entry):
            return True

        elif self.node.MBR.calculate_overlap(self.entry) == other.node.MBR.calculate_overlap(self.entry):
            if self.node.MBR.calculate_area_expansion(self.entry) >  other.node.MBR.calculate_area_expansion(self.entry):
                return True

            elif self.node.MBR.calculate_area_expansion(self.entry) == other.node.MBR.calculate_area_expansion(self.entry):
                if self.node.MBR.get_area() > other.node.MBR.get_area():
                    return True
        return False


@total_ordering
class MinHeap_areaExpansion:
    def __init__(self, node, entry):
        self.node = node
        self.entry = entry

    def __lt__(self, other):
        if self.node.MBR.calculate_area_expansion(self.entry) > other.node.MBR.calculate_area_expansion(self.entry):
            return True

        elif self.node.MBR.calculate_area_expansion(self.entry) == other.node.MBR.calculate_area_expansion(self.entry):
            if self.node.MBR.get_area() > other.node.MBR.get_area():
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