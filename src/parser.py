
from enum import Enum
from src.translator import Translator
from src.symtable import SymTable

cType = Enum("cType", "A_COMMAND C_COMMAND L_COMMAND")


class Parser:
    def __init__(self, fileName):
        self.prog = None
        self.iProgLine = 0
        self.symCommand = ""
        self.binCommand = ""
        self.nCommand = 0
        self.isComment = False
        self.symCommandType = -1
        self.tranlator = Translator()
        self.symTable = SymTable()
        self.newFile = fileName + ".hack"
        return None

    def addData(self, data):
        self.prog = data
        return None

    def advance(self):
        # strip leading/trailing whitespaces, remove "/n" characters
        currentLine = self.prog[self.iProgLine].strip()
        self.iProgLine += 1
        # do not parse empty lines and comments
        if ('//' in currentLine):
            i = currentLine.find('/')
            currentLine = currentLine[:i].strip()
        if ('/*' in currentLine and '*/' in currentLine):
            i = currentLine.find('/')
            j = currentLine[i+1:].find('/')
            currentLine = (currentLine[:i] + currentLine[j+1:]).strip()
        if ('/*' in currentLine):
            self.isComment = True
            return False
        if ('*/' in currentLine):
            self.isComment = False
            return False
        if (self.isComment):
            return False
        if (not currentLine):
            return False
        if (currentLine.startswith("(")):
            return False
        self.symCommand = currentLine
        # select correct type of instruction
        if (currentLine.startswith("@")):
            self.symCommandType = cType.A_COMMAND
        else:
            self.symCommandType = cType.C_COMMAND
        self.nCommand += 1
        return True

    def symbol(self):
        value = ""
        if (self.symCommandType == cType.A_COMMAND):
            value = self.symCommand.strip("@")
        if (not value.isdigit()):
            if (self.symTable.contains(value)):
                value = self.symTable.getAddress(value)
            else:
                value = self.symTable.addEntry(value)
        return '{0:016b}'.format(int(value))

    def instructions(self):
        if (self.symCommandType != cType.C_COMMAND):
            return ("", "", "")
        i = self.symCommand.find('=')
        j = self.symCommand.find(';')
        if (i == -1 and j == -1):
            dest = 'null'
            comp = self.symCommand
            jump = 'null'
            return (dest, comp, jump)
        if (i == -1):
            dest = 'null'
            comp = self.symCommand[:j]
            jump = self.symCommand[j+1:]
            return (dest, comp, jump)
        if (j == -1):
            dest = self.symCommand[:i]
            comp = self.symCommand[i+1:]
            jump = 'null'
            return (dest, comp, jump)
        dest = self.symCommand[:i]
        comp = self.symCommand[i+1:j]
        jump = self.symCommand[j+1:]
        return (dest, comp, jump)

    def commandToBinary(self):
        if (self.symCommandType == cType.C_COMMAND):
            (dest, comp, jump) = self.instructions()
            cCommandBinary = self.tranlator.translate(dest, comp, jump)
            return '111' + cCommandBinary
        else:
            return self.symbol()

    def parse(self):
        self.symTable.addData(self.prog)
        self.symTable.findLabels()
        hackFile = open(self.newFile, 'w')
        while (self.iProgLine < len(self.prog)):
            if (self.advance()):
                binCommand = self.commandToBinary()
                hackFile.write(binCommand)
                hackFile.write("\n")
        return
