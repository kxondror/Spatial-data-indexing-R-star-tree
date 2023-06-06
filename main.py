import file_handler
from file_handler import Process_osm_file
from R_star_tree import RTree
from Node import Node
from Record import Record
from MBR import MBR
from Middle_entry import Middle_entry


if __name__ == '__main__':
    Tree = RTree()
    """file_handler.Empty_file("datafile.bin")

    handler = Process_osm_file("map.xml")
    df = handler.osm_to_dataframe()
    handler.df_to_bin(df)
    file_handler.file_read("datafile.bin")"""

    """node2 = Node(leaf=True)
    node2.add_entry(Record(2, 1, [1, 2]))

    entry = Middle_entry(node2, MBR([[1, 1], [1, 2], [2, 2], [2, 1]]))

    Tree.root = Node()
    Tree.root.add_entry(entry)

    print(entry.child_pointer.entries[0].cordinates)
    input()"""


    Tree.Insert_data(Record(1, 1, (1, 1)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(2, 1, (2, 1)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(3, 1, (3, 4)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(4, 2, (1, 2)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(4, 2, (10, 5)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(4, 2, (1, 5)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(4, 2, (1, 6)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(4, 2, (1, 7)))
    print("-----------")
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(4, 2, (1, 8)))
    print("-----------")
    print(Tree.total_levels)
    Tree.print_tree(Tree.root)
    input()
    Tree.Insert_data(Record(4, 2, (2, 2)))
    print("-----------")
    Tree.print_tree(Tree.root)


