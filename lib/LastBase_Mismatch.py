#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import sys
import re

Pat = re.compile("(\d+)[M|D]")
Sat = re.compile("(\d+)S")

def Get_Pos(InPos):

    InP = open(InPos, 'r')
    PosD = defaultdict(dict)

    for line in InP:
        lines = line.strip().split("\t")
        PosD[lines[0] + "\t" + lines[1]] = lines[2]

    return PosD


def Filter_LastBase(InSam, BaseD, Chain, InRef, OutSam, OutFile):

    InS = open(InSam, 'r')
    InR = open(InRef, 'r')
    OutF = open(OutFile, 'w')
    OutS = open(OutSam, 'w')
    IDDict = defaultdict(dict)
    PosD = []
    #OF = open("Error.sam", 'w')

    for Line in InS:
        if Line.startswith("@"):
            continue
            #OF.write(Line)
        else:
            Lines = Line.strip().split("\t")
            LastPos = ''
            LastBase = ''
            Seq = ''
            P1_searchAll = Pat.findall(Lines[5])
            MatchL = sum([int(i) for i in P1_searchAll])
            P2_searchAll = Sat.findall(Lines[5])
            SoftC = sum([int(i) for i in P2_searchAll])
            if Lines[5].endswith("S") and re.match(Sat, Lines[5]):
                Seq = Lines[9][0:int(len(Lines[9]))-int(P2_searchAll[-1])]
                Seq = Seq[int(P2_searchAll[0]):]
            elif Lines[5].endswith("S") and not re.match(Sat, Lines[5]):
                Seq = Lines[9][0:int(len(Lines[9]))-int(SoftC)]
            elif Lines[5] == "*":
                continue
            else:
                Seq = Lines[9][int(SoftC):]
            if Chain == "+":
                LastPos = int(Lines[3]) + int(MatchL) - 1
                LastBase = Seq[-1]
            else:
                LastPos = int(Lines[3])
                LastBase = Seq[0]
            if BaseD[Lines[2] + "\t" + str(LastPos)] == LastBase:
                IDDict[Lines[0]] = 1
            else:
                OutF.write(Lines[2] + "\t" + str(LastPos) + "\t" + LastBase + "\n")
                #OF.write(Line)

    for sam in InR:
        if sam.startswith("@"):
            OutS.write(sam)
        else:
            sams = sam.strip().split("\t")
            if sams[0] in IDDict:
                OutS.write(sam)
            else:
                #continue
                OutS.write(sam)


InputPos = sys.argv[1]
InputSam = sys.argv[2]
InputCha = sys.argv[3]
InputRef = sys.argv[4]
OutputSam = sys.argv[5]
OutputFile = sys.argv[6]

PosDict = Get_Pos(InputPos)
Filter_LastBase(InputSam, PosDict, InputCha, InputRef, OutputSam, OutputFile)








