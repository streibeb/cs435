class Packet:
    def __init__(self):
        self.seqCount = 0
        self.data = bytearray()
        self.hash = bytearray()

    def append(self, data):
        self.data.append(data)

    def length(self):
        return len(self.data)

    def __str__(self):
        return "%s%s%s" % (self.seqCount, self.data, self.hash)
        #return "seqCount = %s\ndata = %s\nhash = %s\n" % (self.seqCount, self.data, self.hash)

class EncryptedPacket:
    def __init__(self, seqCount, data):
        self.seqCount = seqCount
        self.data = data

    def __str__(self):
        return "%s%s" % (self.seqCount, self.data)
        #return "seqCount = %s\ndata = %s\n" % (self.seqCount, self.data)
