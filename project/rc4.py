from state import State

class Rc4:

    def __init__(self, key):
        self.key = bytearray(key)
        self.state = State(range(256))

    def crypt(self, data):
        S = self.ksa(self.key, self.state)

        out = []
        for char in data:
            S.i = (S.i + 1) % 256
            S.j = (S.j + S.body[S.i]) % 256
            S.body[S.i], S.body[S.j] = S.body[S.j], S.body[S.i]
            t = (S.body[S.i] + S.body[S.j]) % 256
            out.append(chr(ord(char) ^ S.body[t]))
        return "".join(out)

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

    @staticmethod
    def prga(S):
        for m in range(len(S.body)):
            S.i = (S.i + 1) % 256
            S.j = (S.j + S.body[S.i]) % 256
            S.body[S.i], S.body[S.j] = S.body[S.j], S.body[S.i]

    @staticmethod
    def iprga(S):
        for m in range(len(S.body)):
            S.body[S.i], S.body[S.j] = S.body[S.j], S.body[S.i]
            S.j = (S.j - S.body[S.i] + 256) % 256
            S.i = (S.i - 1) % 256
