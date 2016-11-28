import sys, getopt
from sender import Sender
from packet import EncryptedPacket

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hk:f:",["key=", "filename="])
    except getopt.GetoptError:
        print 'main.py -k <key> -f <filename>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -k <key> -f <filename>'
            sys.exit()
        elif opt in ("-k", "--key"):
            key = str(arg)
        elif opt in ("-f", "--filename"):
            filename = str(arg)

    S = Sender('ABCDEF0123456789ABC2014200319344')
    C = S.send('Hello World ' * (80))
    print C
    for c in C:
        print c


    # rc4 = Rc4('ABCDEF0123456789ABC2014200319344')
    # c = rc4.crypt('Hello World')
    # print c
    # p = rc4.crypt(c)
    # print p

    # inVal = 0
    #
    # md5_a = hashlib.md5()
    # outVal = bytearray()
    # for i in range(4):
    #     outVal.insert(0, (inVal >> i*8) & 0xff)
    # md5_a.update(outVal)
    # md5_a.update('Hello')
    # print md5_a.hexdigest()
    #
    # md5_b = hashlib.md5()
    # md5_b.update(str(inVal))
    # md5_b.update('Hello')
    # print md5_b.hexdigest()

if __name__ == '__main__':
    main(sys.argv[1:])
