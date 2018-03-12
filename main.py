#!/usr/bin/env python
from src.parser import Parser
import sys
import os


def main():
    if (len(sys.argv) < 2):
        print("Enter assembler file name")
        print("Example: ")
        print(f"{os.path.basename(sys.argv[0])} file.asm")
        input("Press Enter to exit...")
    asmFile = open(sys.argv[1], 'r')
    asmFileName = os.path.splitext(sys.argv[1])[0]
    asmProg = asmFile.readlines()
    asmFile.close()
    myParser = Parser(asmFileName)
    myParser.addData(asmProg)
    myParser.parse()


if (__name__ == "__main__"):
    main()
