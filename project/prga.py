#!/usr/bin/python

class State:
    i = 0
    j = 0
    S = []

    def __init__(self):
        self.i = 0
        self.j = 0
        self.S = range(256)[::1]

    def __str__(self):
        return "i = %s,\nj = %s,\nS = %s\n" % (self.i, self.j, self.S)

#
# PRGA algorithm given by the notes
#
def prga(state):
    for m in range(len(state.S)):
        state.i = (state.i + 1) % 256
        state.j = (state.j + state.S[state.i]) % 256
        state.S[state.i], state.S[state.j] = state.S[state.j], state.S[state.i]

def iprga(state):
    for m in range(len(state.S)):
        state.S[state.i], state.S[state.j] = state.S[state.j], state.S[state.i]
        state.j = (state.j - state.S[state.i] + 256) % 256
        state.i = (state.i - 1) % 256

def main(argv):
    num_rounds = 3
    global verbose
    verbose = False

    try:
        opts, args = getopt.getopt(argv,"hn:v",["num=", "verbose"])
    except getopt.GetoptError:
        print 'prga.py -n <num_rounds> -v'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'prga.py -n <num_rounds> -v'
            sys.exit()
        elif opt in ("-n", "--num"):
            num_rounds = int(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True

    if (verbose):
        print("Number of rounds: %i" % num_rounds)
        print("")

    S = State()

    print("=== Initial state ===")
    print(S)

    if (verbose):
        print("=== Start PRGA ===")
    for n in range(0, num_rounds):
        prga(S)
        if (verbose):
            print("=== After round %s ===" % str(n+1))
            print(S)

    if (verbose):
        print("=== End PRGA ===")
        print("=== After %i round PRGA ===" % num_rounds)
        print(S)

    if (verbose):
        print("=== Start IPRGA ===")
    for n in range (0, num_rounds):
        iprga(S)
        if (verbose):
            print("After round %s: " % str(n+1))
            print(S)

    if (verbose):
        print("=== End IPRGA ===")
        print("=== After %i round IPRGA ===" % num_rounds)
        print(S)

    print("=== Final state ===")
    print(S)

if __name__ == '__main__':
    import sys, getopt

    main(sys.argv[1:])
