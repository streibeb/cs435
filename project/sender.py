import hashlib
from packet import Packet, EncryptedPacket
from rc4 import Rc4

class Sender:

    def __init__(self, key):
        self.key = key;
        self.SCA = 0;
        self.rc4 = Rc4(self.key)

    #
    # Description:
    #     Builds packets from a given plaintext and encrypts them
    # Input:
    #     plaintext: The plaintext to encrypt
    # Output:
    #     A list of encrypted packets
    #
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
            self.rc4.applyPRGA()
            seqCount = p.seqCount
            c = EncryptedPacket(seqCount, data)
            encryptedPackets.append(c)

        return encryptedPackets

    #
    # Description:
    #     Takes a plaintext and splits it into data segments of the correct size
    # Input:
    #     plaintext: The text to split into packets
    # Output:
    #     A list of packets
    #
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
        self.applyPadding(packets[-1])

        return packets

    #
    # Description:
    #     Appends a 1 and enough 0s to fill the packet
    # Input:
    #     packet: The packet to append data to
    # Output:
    #     N/A
    #
    def applyPadding(self, packet):
        length = len(packet.data)
        if length  == 252:
            return
        packet.append(0b10000000)
        for i in range(252 - length - 1):
            packet.append(0b00000000)
