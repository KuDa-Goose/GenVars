#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import sys
import linecache

def Arrt_Ontar(Ontar_File, Probe_File, OutFile):

    P = defaultdict(dict)
    SInfo = defaultdict(dict)
    InF = open(Ontar_File, 'r')
    OutF = open(OutFile, 'w')

    for Line in InF:
        if not Line.endswith("Reads"):
            Lines = Line.strip().split("\t")
            SInfo[Lines[0]][Lines[1]] = Lines[2]
            P[Lines[1]] = 0

    InF.close()


    InF2 = open(Probe_File, 'r')
    Total = defaultdict(dict)

    for line in InF2:
        if not line.startswith("Sample"):
            lines = line.strip().split("\t")
            SampleNumber = lines[0].split("S")[1]
            SampleName = "Sample" + SampleNumber
            Total[SampleName] = lines[1]
    
    InF2.close()

    Title = "Sample\tTotalReads"
    for Probes in P:
        Title += "\t" + Probes
    OutF.write(Title+ "\n")
    for Sample in SInfo:
        Total_Reads = Total[Sample]
        OutF.write(Sample + "\t" + str(Total_Reads))
        for Probe in P:
            OutF.write("\t" + SInfo[Sample][Probe])

        OutF.write("\n")



O_File = sys.argv[1]
P_File = sys.argv[2]
Out_File = sys.argv[3]
Arrt_Ontar(O_File, P_File, Out_File)

