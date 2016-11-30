from state import State

class Rc4:

    def __init__(self, key):
        self.key = bytearray(key)
        self.state = self.ksa(self.key, State(range(256)))
        self.applyPRGA()

    def crypt(self, data):
        S = self.state
        out = []
        for char in data:
            t = (S.body[S.i] + S.body[S.j]) % 256
            out.append(chr(ord(char) ^ S.body[t]))

        return "".join(out)

    def applyPRGA(self):
        #print 'Apply PRGA'
        S = self.state
        for m in range(len(S.body)):
            S.i = (S.i + 1) % 256
            S.j = (S.j + S.body[S.i]) % 256
            S.body[S.i], S.body[S.j] = S.body[S.j], S.body[S.i]

    def applyIPRGA(self):
        #print 'Apply IPRGA'
        S = self.state
        for m in range(len(S.body)):
            S.body[S.i], S.body[S.j] = S.body[S.j], S.body[S.i]
            S.j = (S.j - S.body[S.i] + 256) % 256
            S.i = (S.i - 1) % 256

    @staticmethod
    def ksa(key, Sin):
        s = Sin.body[:]
        k = key;

        j = 0
        for i in range(256):
            j = (j + s[i] + k[i % len(k)]) % 256
            s[i], s[j] = s[j], s[i]

        Sout = State(s)
        Sout.i = i
        Sout.j = j
        return Sout
