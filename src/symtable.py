class SymTable:
    def __init__(self):
        self.predefSymbols = {'SP':   0,
                              'LCL':  1,
                              'ARG':  2,
                              'THIS': 3,
                              'THAT': 4,
                              'R0':   0,
                              'R1':   1,
                              'R2':   2,
                              'R3':   3,
                              'R4':   4,
                              'R5':   5,
                              'R6':   6,
                              'R7':   7,
                              'R8':   8,
                              'R9':   9,
                              'R10':  10,
                              'R11':  11,
                              'R12':  12,
                              'R13':  13,
                              'R14':  14,
                              'R15':  15,
                              'SCREEN': 16384,
                              'KBD': 24576}
        self.labelSymbols = {}
        self.varSymbols = {}
        self.data = None
        self.programCounter = 0
        self.ramOffset = 16
        return None

    def addData(self, data):
        self.data = data
        return None

    def findLabels(self):
        for line in self.data:
            line = line.strip()
            if ('(' in line or ')' in line):
                self.labelSymbols[line.strip('()')] = self.programCounter
            cond = ((('@' in line) or ('=' in line) or (';' in line))
                    and not (line.startswith('/')))
            if (cond):
                self.programCounter += 1
        return None

    def contains(self, s):
        cond = (s in self.predefSymbols or
                s in self.labelSymbols or
                s in self.varSymbols)
        return cond

    def addEntry(self, s):
        self.varSymbols[s] = self.ramOffset
        self.ramOffset += 1
        return self.varSymbols[s]

    def getAddress(self, s):
        addr = ''
        if (s in self.predefSymbols):
            addr = self.predefSymbols[s]
        if (s in self.labelSymbols):
            addr = self.labelSymbols[s]
        if (s in self.varSymbols):
            addr = self.varSymbols[s]
        return addr
