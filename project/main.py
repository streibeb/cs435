import sys, argparse
from sender import Sender
from receiver import Receiver
from packet import EncryptedPacket

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--plaintext")
    group.add_argument("-f", "--filename")
    parser.add_argument("-t", '--test', action='store_true')
    args = parser.parse_args()

    key = args.key

    plaintext = ''
    if args.filename:
        filename = args.filename
        f = open(filename, 'r')
        plaintext = f.read()
        f.close()
    if args.plaintext:
        plaintext = args.plaintext

    test = False
    if args.test:
        test = args.test

    if test:
        result = []
        try:
            print '### TEST 1 [0,1,2,3] ###\n'
            result.append(test1(key, plaintext))
            print '### TEST 2 [1,0,3,2] ###\n'
            result.append(test2(key, plaintext))
            print '### TEST 3 [3,2,1,0] ###\n'
            result.append(test3(key, plaintext))
        except IndexError:
            print '\nWARNING: Message not long enough to perform all tests\n'

        print '#  | Success?'
        print '---+---------'
        for i in range(len(result)):
            print '%-2i | %s' % (i+1, result[i])
    else:
        test1(key, plaintext)

def test1(key, sent):
    S = Sender(key)
    R = Receiver(key)

    print '### SEND ###'
    print sent
    print '############'

    while True:
        C = S.send(sent)
        print '### ENCRYPTED PACKETS ###'
        for c in C:
            print repr(c)
        print '#########################'
        err, received = R.receive(C)
        if (err == None):
            break
        else:
            print 'Uh Oh'
            sys.exit(1)

    print '### RECEIVE ###'
    print received
    print '###############'
    test = sent == received
    print 'sent = received? ' + str(test)
    print '###############\n'

    return test

def test2(key, sent):
    S = Sender(key)
    R = Receiver(key)

    print '### SEND ###'
    print sent
    print '############'

    while True:
        C = S.send(sent)
        C = [C[1],C[0],C[3],C[2]]
        print '### ENCRYPTED PACKETS ###'
        for c in C:
            print c
        print '#########################'
        err, received = R.receive(C)
        if (err == None):
            break
        else:
            print 'Uh Oh'
            sys.exit(1)

    print '### RECEIVE ###'
    print received
    print '###############'
    test = sent == received
    print 'sent = received? ' + str(test)
    print '###############\n'

    return test

def test3(key, sent):
    S = Sender(key)
    R = Receiver(key)

    print '### SEND ###'
    print sent
    print '############'

    while True:
        C = S.send(sent)
        C = [C[3],C[2],C[1],C[0]]
        print '### ENCRYPTED PACKETS ###'
        for c in C:
            print c
        print '#########################'
        err, received = R.receive(C)
        if (err == None):
            break
        else:
            print 'Uh Oh'
            sys.exit(1)

    print '### RECEIVE ###'
    print received
    print '###############'
    test = sent == received
    print 'sent = received? ' + str(test)
    print '###############\n'

    return test

if __name__ == '__main__':
    main(sys.argv[1:])
