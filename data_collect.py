#!/usr/bin/env python

from import_tool import *

def main():
    linesCount()

def linesCount():
    convos = importConvos()
    for convo in convos:
        print convo["lines1"] if convo["lines1"] else 0 +\
              convo["lines2"] if convo["lines2"] else 0


if __name__ == "__main__":
    main()
