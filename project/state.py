class State:

    def __init__(self, body=bytearray(range(256))):
        self.i = 0
        self.j = 0
        self.body = bytearray(body)

    def __str__(self):
        return "i = %s,\nj = %s,\nS = %s\n" % (self.i, self.j, repr(self.body))
