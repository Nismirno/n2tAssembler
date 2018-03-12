from src.parser import Parser
import sys
import os


def main():
    if (len(sys.argv) < 2):
        print("Enter assembler file name")
        print("Example: ")
        print(f"         {sys.argv[0]} file.asm")
    asmFile = open(sys.argv[1], 'r')
    asmFileName = os.path.splitext(sys.argv[1])[0]
    asmProg = asmFile.readlines()
    asmFile.close()
    myParser = Parser(asmFileName)
    myParser.addData(asmProg)
    myParser.parse()


if (__name__ == "__main__"):
    main()
