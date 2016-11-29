import hashlib
from packet import Packet, EncryptedPacket
from rc4 import Rc4

class Receiver:

    #    Initially (S, i, j)B = (S, i, j)0 and SCB = 0. When receiving a new packet, B compares its
    # own SC value (SCB) with the SC value of the packet. If the difference of the SC value of
    # the packet and its own SC value (SCpacket - SCB) is 0, then (S, i, j)B is used as the RC4
    # state to decrypt the data segment and hash value of that incoming packet and then
    # increase the sequence counter by 1. Otherwise, calculate the right RC4 state from current
    # (S, i, j)B by applying certain rounds of PRGA or IPRGA, and then use the right RC4 state
    # to decrypt the data segment and hash value of that incoming packet and set the sequence
    # counter value of receiver by the SC value of the packet plus 1. B also needs to calculate
    # the hash value according to the decrypted data (SC and data segment) and then compare
    # it with the one directly get from decrypted packet. If they are not the same, B requests A
    # to resend the packet.

    def __init__(self, key):
        self.key = key;
        self.SCB = 0;
        self.rc4 = Rc4(self.key)

    def receive(self, encryptedPackets):
        err = []
        packets = []
        for c in encryptedPackets:
            p = self.calculateState(c)
            packets.append(p)

        for p in packets:
            md5 = hashlib.md5()
            md5.update(str(p.seqCount))
            md5.update(p.data)
            if p.hash != md5.digest():
                return p.seqCount, None

        packets.sort(key=lambda x: x.seqCount)
        self.RemovePadding(packets[-1])

        data = []
        for p in packets:
            data.append(str(p.data))
        return None, ''.join(data)

    def calculateState(self, packet):
        diff = self.SCB - packet.seqCount

        if diff == 0:
            p = self.generatePacket(packet)
            return p
            self.SCB += 1
        elif diff > 0:
            self.rc4.applyIPRGA();
            self.SCB -= 1
            return self.calculateState(packet)
        elif diff < 0:
            self.rc4.applyPRGA()
            self.SCB += 1
            return self.calculateState(packet)

    def generatePacket(self, encryptedPacket):
        p = Packet()

        p.seqCount = encryptedPacket.seqCount

        temp = self.rc4.crypt(encryptedPacket.data)
        for i in range(1, 253):
            p.data.append(temp[i])
        for i in range(253, 253+16):
            p.hash.append(temp[i])

        return p

    def RemovePadding(self, packet):
        index = packet.indexOf(0b10000000)
        packet.data = packet.data[:index]
