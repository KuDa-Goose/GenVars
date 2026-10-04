#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import sys

def Analysis_SNV(InDB, InDvcf, OutFile):

    InD = open(InDB, 'r')
    InDelInfo = defaultdict(dict)

    for line in InD:
        if line.startswith("Chrom"):
            continue
        else:
            lines = line.strip().split("\t")
            InDelInfo[lines[4]] = lines[0] + "\t" + lines[1] + "\t" + lines[2] + "\t" + lines[3]

    
    OutF = open(OutFile, 'w')
    InV = open(InDvcf, 'r')

    for Line in InV:
        if Line.startswith("Chrom"):
            continue
        else:
            Lines = Line.strip().split("\t")
            InDel_Type = Lines[18][:1]
            MutBase = Lines[18][1:]
            for MutName in InDelInfo:
                MutInfo = InDelInfo[MutName].split("\t")
                if Lines[0] == MutInfo[0] and Lines[1] >= MutInfo[1] and Lines[1] <= MutInfo[2] and InDel_Type == MutInfo[3]:
                    if InDel_Type == "+":
                        OutF.write(Lines[0][3:] + "\t" + Lines[1] + "\t" + Lines[1] + "\t" + "-" + "\t" + MutBase + "\t" + MutName + "\t" + Lines[6] + "\n")
                    else:
                        start = int(Lines[1]) + 1
                        end = int(Lines[1]) + len(MutBase)
                        OutF.write(Lines[0][3:] + "\t" + str(start) + "\t" + str(end) + "\t" + MutBase + "\t" + "-" + "\t" + MutName + "\t" + Lines[6] + "\n")


InputDatabase = sys.argv[1]
InputVCF = sys.argv[2]
OutputFile = sys.argv[3]
Analysis_SNV(InputDatabase, InputVCF, OutputFile)
