#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import Counter
from collections import defaultdict
import numpy as np
import argparse
import os, re
import sys

def Read_ProbeBed(Probe, InFile):

    InF = open(InFile, 'r')

    for Line in InF:
        if not Line.startswith("Chr"):
            Lines = Line.strip().split("\t")
            if Lines[4] == Probe:
                if Lines[5] == "+":
                    Pos_1 = int(Lines[2]) + 10
                    Pos_2 = int(Lines[2]) + 15
                    Pos = Lines[0] + "\t" + str(Pos_1) + "\t" + str(Pos_2) + "\t" + Lines[3]
                else:
                    Pos_1 = int(Lines[1]) - 10
                    Pos_2 = int(Lines[1]) - 15
                    Pos = Lines[0] + "\t" + str(Pos_1) + "\t" + str(Pos_2) + "\t" + Lines[3]
            else:
                continue

    return Pos


def Calculation_Ontarget(Sample, Position, Deep, OutFile):

    InF2 = open(Deep, 'r')
    PosInfo = Position.split("\t")
    OutF = open(OutFile, 'w')

    O_Reads_1 = 0
    O_Reads_2 = 0
    for line in InF2:
        lines = line.strip().split("\t")
        if lines[0] == PosInfo[0] and int(lines[1]) == int(PosInfo[1]):
            O_Reads_1 = lines[2]
        elif lines[0] == PosInfo[0] and int(lines[1]) == int(PosInfo[2]) :
            O_Reads_2 = lines[2]
    Ontarget_R = (float(O_Reads_1) + float(O_Reads_2))/2
    OutF.write(Sample + "\t" + PosInfo[3] + "\t" + str(Ontarget_R) + "\n")



ProbeN = sys.argv[1]
ProbeI = sys.argv[2]
SampleN = sys.argv[3]
DeepFile = sys.argv[4]
OutputFile = sys.argv[5]
PosI = Read_ProbeBed(ProbeN, ProbeI)
Calculation_Ontarget(SampleN, PosI, DeepFile, OutputFile)



