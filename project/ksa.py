from state import State

class KSA:
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
