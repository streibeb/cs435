import hashlib
from packet import Packet, EncryptedPacket
from rc4 import Rc4

class Sender:

    def __init__(self, key):
        self.key = key;
        self.SCA = 0;
        self.rc4 = Rc4(self.key)

    def send(self, plaintext):
        # 1. The sender divides the input plaintext message into contiguous 252-byte data
        #    segments and assigns SC to each of them. The sequence counter (SC) value is
        #    increased by 1 in increased order (initially SCA = 0). If there are not enough data in
        #    the data segment of the last data packet, pad a 1 followed by as many 0 as necessary.
        packets = self.generatePackets(plaintext)

        # 2. The sender calculates the hash value for that data packet by inputting SC and the
        #    unencrypted data segment, and then places the 128-bit hash value into the data
        #    packet.
        for p in packets:
            md5 = hashlib.md5()
            md5.update(str(p.seqCount))
            md5.update(p.data)
            p.hash = md5.digest()

        # 3. The sender produces the encrypted data packets by only encrypting data segment and
        #    hash value (do not encrypt SC value). The sender updates its SCA and (S, i, j)A after
        #    the encryption.
        encryptedPackets = []
        for p in packets:
            data = self.rc4.crypt(str(p))
            seqCount = p.seqCount
            c = EncryptedPacket(seqCount, data)
            encryptedPackets.append(c)

        return encryptedPackets

    def generatePackets(self, plaintext):
        pt = bytearray(plaintext)

        packets = []
        for i in range(len(pt)):
            if i % 252 == 0:
                packet = Packet()
                packets.append(packet)
                packet.seqCount = self.SCA;
                self.SCA = self.SCA + 1
            packet.append(pt[i])
        self.pad(packets[-1])

        return packets

    def pad(self, packet):
        length = len(packet.data)
        if length  == 252:
            return
        packet.append(0b10000000)
        for i in range(252 - length - 1):
            packet.append(0b00000000)
