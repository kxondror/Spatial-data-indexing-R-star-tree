import file_handler
from file_handler import Process_osm_file
from R_star_tree import RTree
from Node import Node
from Record import Record
from MBR import MBR
from Middle_entry import Middle_entry
from skyline import skyline


if __name__ == '__main__':
    Tree = RTree()
    """file_handler.Empty_file("datafile.bin")

    handler = Process_osm_file("map.xml")
    df = handler.osm_to_dataframe()
    handler.df_to_bin(df)
    file_handler.file_read("datafile.bin")"""

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



