import sys, argparse
from sender import Sender
from receiver import Receiver
from packet import EncryptedPacket

def main(argv):
    
    # Command Line Argument Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--plaintext")
    group.add_argument("-f", "--filename")
    parser.add_argument("-t", '--test', action='store_true')
    args = parser.parse_args()

    # Specify key to use
    key = args.key

    # Specify file or plaintext to use
    plaintext = ''
    if args.filename:
        filename = args.filename
        f = open(filename, 'r')
        plaintext = f.read()
        f.close()
    if args.plaintext:
        plaintext = args.plaintext

    # Set flag if all three tests should be performed
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

#
# Description:
#     Sends packets in the order [0,1,2,3] from Sender to Receiver
# Input:
#     key:  Key for use in RC4
#     sent: Text to send
# Output:
#     Boolean indicating whether or not the decrypted plaintext
#     matches the input plaintext
#
def test1(key, sent):
    # Initialize Sender and Receiver with key
    S = Sender(key)
    R = Receiver(key)

    print '### SEND ###'
    print sent
    print '############'

    # Loops if there is an error with the transfer
    while True:
        # Builds & encrypts packets to send
        C = S.send(sent)
        print '### ENCRYPTED PACKETS ###'
        for c in C:
            print repr(c)
        print '#########################'
        # Decrypts & rebuilds packets in correct order
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

#
# Description:
#     Sends packets in the order [1,0,3,2] from Sender to Receiver
# Input:
#     key:  Key for use in RC4
#     sent: Text to send
# Output:
#     Boolean indicating whether or not the decrypted plaintext
#     matches the input plaintext
#
def test2(key, sent):
    # Initialize Sender and Receiver with key
    S = Sender(key)
    R = Receiver(key)

    print '### SEND ###'
    print sent
    print '############'

    # Loops if there is an error with the transfer
    while True:
        # Builds & encrypts packets to send
        C = S.send(sent)
        C = [C[1],C[0],C[3],C[2]]
        print '### ENCRYPTED PACKETS ###'
        for c in C:
            print c
        print '#########################'
        # Decrypts & rebuilds packets in correct order
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

#
# Description:
#     Sends packets in the order [3,2,1,0] from Sender to Receiver
# Input:
#     key:  Key for use in RC4
#     sent: Text to send
# Output:
#     Boolean indicating whether or not the decrypted plaintext
#     matches the input plaintext
#
def test3(key, sent):
    # Initialize Sender and Receiver with key
    S = Sender(key)
    R = Receiver(key)

    print '### SEND ###'
    print sent
    print '############'

    # Loops if there is an error with the transfer
    while True:
        # Builds & encrypts packets to send
        C = S.send(sent)
        C = [C[3],C[2],C[1],C[0]]
        print '### ENCRYPTED PACKETS ###'
        for c in C:
            print c
        print '#########################'
        # Decrypts & rebuilds packets in correct order
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
