from MBR import MBR

class Record:
    def __init__(self, slot, block, cordinates):
        self.record_slot = slot
        self.block_id = block
        self.cordinates = cordinates
        self.MBR = MBR(self.get_record_mbr())

    def get_record_mbr(self):
        return tuple([cord for cord in self.cordinates]), tuple([cord for cord in self.cordinates])
