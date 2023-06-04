import sys
import os
import re
import pandas as pd


def file_read(filename):
    with open(filename, "r") as file:

        next(file)
        for line in file:
            # print(sys.getsizeof(line) * 8)
            for word in line.split():

                if re.search('^Block+', word):
                    print(f'{word}: ')
                    continue

                word = float(word)
                print(word)
                input()


def file_write(element):
    with open('temp.bin', 'ab') as f:
        # Encode the text to bytes using UTF-8 encoding
        bytes_data = element.encode('utf-8')
        # Write the bytes to the file
        f.write(bytes_data)


def Empty_file(filename):
    file_to_delete = open(filename, 'w')
    file_to_delete.close()


def reformat_record(record):
    record = record.replace("[", "")
    record = record.replace("]", "")
    record = record.replace(",", "")
    record = record.replace("'", "")
    return record


class Process_osm_file:
    def __init__(self, file):
        self.BlockSize = 32768
        self.num_records = 0
        self.num_blocks = 0
        self.block_id = 0
        self.filename = file

    def osm_to_dataframe(self):
        df = pd.read_xml(self.filename)
        df = df.drop(
            ["minlat", "minlon", "maxlat", "maxlon", "visible", "version", "changeset", "timestamp", "user", "uid",
             "tag",
             "nd", "member"], axis=1)

        df = df.iloc[1:, :]
        df = df.dropna()
        df = df.applymap(lambda x: str(x))
        return df

    def df_to_bin(self, df):
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
                file_write("Block" + str(self.block_id) + " " + reformat_record(' '.join(map(str, Block))) + "\n",
                           "temp.bin")

                element = [row[1][0], row[1][1], row[1][2]]
                Block = [element]

        with open("temp.bin", "rb") as old, open("datafile.bin", "wb") as new:
            info_block = f"Block0 records: {self.num_records} blocks: {self.num_blocks} \n"

            new.write(info_block.encode('utf-8'))
            new.write(old.read())
        os.remove("temp.bin")
