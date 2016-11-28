from state import State;

#
# PRGA algorithm given by the notes
#
class PRGA:
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
