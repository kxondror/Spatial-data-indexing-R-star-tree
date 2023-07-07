from R_star_tree import RTree
from Record import Record
import file_handler
import sys
import re


def read_location(tree, number_of_entries) -> None:
    """
    Reads, constructs, and inserts entries into the R-tree from the saved data in the datafile.bin.

    :param tree: (RTree) An instance of the R-tree.
    :param number_of_entries: (int) The number of entries to be inserted into the structure.
    :return: (None)
    """
    current_block = "Block0"
    current_location = []
    for counter, location in enumerate(file_handler.read_file("secondary memory files/datafile.bin")):

        if number_of_entries is not None and counter >= number_of_entries: break
        if re.search('^Block+', str(location)):
            current_block = location
            continue
        else:
            current_location.append(location)

            if len(current_location) == 3:
                tree.Insert_data(Record(current_location[0], current_block, (current_location[1], current_location[2])))
                current_location.clear()


if __name__ == '__main__':

    if len(sys.argv) > 2:
        raise ValueError("Too many arguments!")
    elif len(sys.argv) == 1:
        raise ValueError("Νo dimension number entered!")

    Tree = RTree()
    # read_location(Tree, None)

    # Example with step-by-step tree insertions and a subsequent deletion.
    data = [(1, 1), (2, 1), (3, 4), (4, 3), (1, 2), (10, 5), (1, 5), (1, 6), (1, 7), (1, 8), (2, 2)]
    for record in data:
        Tree.Insert_data(Record(1, 1, (record[0], record[1])))
        Tree.print_tree(Tree.root)
        input("\n<Press Enter>\n")
    Tree.print_tree(Tree.root)

    print("\n------Deletion------\n")
    Tree.delete_record(Record(1, 1, (1, 5)))
    Tree.print_tree(Tree.root)
    print("\n------End of deletion------\n")
