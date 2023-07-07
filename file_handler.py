import pandas as pd
import sys
import os
import re


def read_file(filename) -> float | str:
    """
    Reads a file and yields entries from it.

    :param filename: (str) The name of the file to be read.
    :return: (float | str) Yields entries from the file.
    """
    with open(filename, "r") as file:

        next(file)
        for line in file:
            for word in line.split():

                if re.search('^Block+', word):
                    yield word
                    continue

                word = float(word)
                yield word


def file_write(element) -> None:
    """
    Writes an element to file.(temporary use)

    :param element: (str) Data we want to write
    :return: (None)
    """
    with open('temp.bin', 'ab') as file:
        bytes_data = element.encode('utf-8')
        file.write(bytes_data)


def Empty_file(filename) -> None:
    """
    Clears the data from a file.

    :param filename: (str) Path to the file
    :return: (None)
    """
    file_to_delete = open(filename, 'w')
    file_to_delete.close()


def reformat_record(record) -> str:
    """
    Re-formats a record by removing unwanted characters.

    :param record: (str) The record to be reformatted.
    :return: (str)The reformatted record.
    """
    record = record.replace("[", "")
    record = record.replace("]", "")
    record = record.replace(",", "")
    record = record.replace("'", "")
    return record


class Process_xml_file:
    """
    This class processes the raw file from 'OpenStreetMap' and saves it into blocks with a size of 32kb in the datafile.
    """

    def __init__(self, file):
        self.BlockSize = 32768
        self.num_records = 0
        self.num_blocks = 0
        self.block_id = 0
        self.filename = file

    def xml_to_dataframe(self) -> pd.DataFrame:
        """
        Reads the raw xml file, drops all the unwanted columns and stores all the records into a temporary dataframe.

        :return: (pd.DataFrame) The processed dataframe.
        """
        df = pd.read_xml(self.filename)
        df = df.drop(
            ["minlat", "minlon", "maxlat", "maxlon", "visible", "version", "changeset", "timestamp", "user", "uid",
             "tag",
             "nd", "member"], axis=1)

        df = df.iloc[1:, :]
        df = df.dropna()
        df = df.applymap(lambda x: str(x))
        return df

    def df_to_bin(self, df) -> None:
        """
        Reads the dataframe and stores the data into the final datafile divided into 32kb blocks.

        :param df: (pd.DataFrame) The dataframe with the data
        :return: (None)
        """
        Block = []
        for row in df.iterrows():
            element = [row[1][0], row[1][1], row[1][2]]

            block_as_string = reformat_record(' '.join(map(str, Block)) + str(element))
            current_block_size = sys.getsizeof(block_as_string) * 8

            if current_block_size <= self.BlockSize:
                Block.append(element)

                self.num_records += 1
            else:
                self.num_blocks += 1
                self.block_id += 1
                file_write("Block" + str(self.block_id) + " " + reformat_record(' '.join(map(str, Block))) + "\n")

                element = [row[1][0], row[1][1], row[1][2]]
                Block = [element]

        with open("temp.bin", "rb") as old, open("secondary memory files/datafile.bin", "wb") as new:
            info_block = f"Block0 records: {self.num_records} blocks: {self.num_blocks} \n"

            new.write(info_block.encode('utf-8'))
            new.write(old.read())
        os.remove("temp.bin")


# Below are some unused functions from our failed attempt to externalize the entire process.
"""
def replace_line(ID, obj):
    # Create temp file
    flag = True
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open("secondary memory files/external_dict.txt") as old_file:
            for line in old_file:
                if line.startswith(ID):
                    flag = False
                    new_file.write(f"{ID} : {obj_to_txt(obj)}\n")
                else:
                    new_file.write(line)

    if flag:
        raise "file dindt change"
    copymode("secondary memory files/external_dict.txt", abs_path)
    remove("secondary memory files/external_dict.txt")
    move(abs_path, "secondary memory files/external_dict.txt")




def read_obj(ID) -> Node | None:
    with open('secondary memory files/external_dict.txt', 'r') as file:
        for line in file:
            if line.startswith(f"{ID}"):
                res = line.split(":")[1].strip()
                return txt_to_obj(res)
    return None



def save_object(obj) -> None:
    with open('secondary memory files/external_dict.txt', 'a') as file:
        file.write(f"{obj.ID} : {obj_to_txt(obj)}\n")


# De-serialize an object from a plain text
def txt_to_obj(txt):
    base64_bytes = txt.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    obj = pickle.loads(message_bytes)
    return obj




# Serialize an object into a plain text
def obj_to_txt(obj) -> str:
    message_bytes = pickle.dumps(obj)
    base64_bytes = base64.b64encode(message_bytes)
    txt = base64_bytes.decode('ascii')
    return txt


"""
