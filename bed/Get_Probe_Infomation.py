#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
import sys
from collections import defaultdict

def Get_ProbeInfo(ProbeInfo):

    Info = open(ProbeInfo, 'r')
    PInfo = defaultdict(dict)
    OInfo = defaultdict(dict)

    for P in Info:
        if P.startswith("Probe"):
            continue
        else:
            Ps = P.strip().split("\t")
            if Ps[7] == "+":
                Hotspot = int(Ps[6]) + 10
                TarPosStart = int(Ps[5]) - 10
                TarPosEnd = int(Ps[6]) + 300
                OntargetPos = str(TarPosStart) + "-" + str(TarPosEnd)
                PInfo[Ps[0]] = str(Ps[4]) + "\t" + str(Ps[5]) + "\t" + str(Ps[6]) + "\t" + Ps[0] + "\t" + Ps[8] + "\t" + Ps[7] + "\t" + str(Hotspot) + "\t" + str(Hotspot) + "\t" + Ps[3] + "\t" + OntargetPos + "\t" + Ps[9]
                OInfo[Ps[0]] = str(Ps[4]) + "\t" + str(TarPosStart) + "\t" + str(TarPosEnd) + "\t" + Ps[0]
            elif Ps[7] == "-":
                Hotspot = int(Ps[5]) - 10
                TarPosStart = int(Ps[5]) - 300
                TarPosEnd = int(Ps[6]) + 10
                OntargetPos = str(TarPosStart) + "-" + str(TarPosEnd)
                PInfo[Ps[0]] = str(Ps[4]) + "\t" + str(Ps[5]) + "\t" + str(Ps[6]) + "\t" + Ps[0] + "\t" + Ps[8] + "\t" + Ps[7] + "\t" + str(Hotspot) + "\t" + str(Hotspot) + "\t" + Ps[3] + "\t" + OntargetPos + "\t" + Ps[9]
                OInfo[Ps[0]] = str(Ps[4]) + "\t" + str(TarPosStart) + "\t" + str(TarPosEnd) + "\t" + Ps[0]

    return PInfo, OInfo


def Get_ProbeList(ProbeList, OutFile, PDict, OutFile2, ODict):

    List = open(ProbeList, 'r')
    OutF = open(OutFile, 'w')
    OutF2 = open(OutFile2, 'w')
    OutF.write("Chr\tstart\tend\tpaobe-name\tprobe\tstrand\thotspot1\thotspot2\tsequence\tontar_position\tPrimerAdd5\n")

    for line in List:
        Line = line.strip()
        if Line in PDict:
            OutF.write(PDict[Line] + "\n")
        else:
            OutF.write("None\n")

    List = open(ProbeList, 'r')
    for line in List:
        Line = line.strip()
        if Line in ODict:
            OutF2.write(ODict[Line] + "\n")
        else:
            OutF2.write("None\n")



InputInfo = sys.argv[1]
InputList = sys.argv[2]
OutputFile = sys.argv[3]
OutPutFile = sys.argv[4]

ProbeDict, OntarDict = Get_ProbeInfo(InputInfo)
Get_ProbeList(InputList, OutputFile, ProbeDict, OutPutFile, OntarDict)
