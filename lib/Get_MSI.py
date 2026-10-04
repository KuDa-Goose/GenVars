#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
from collections import defaultdict


def Analysis_MSI(InFile):

    IF = open(InFile, 'r')
    MSIDict = defaultdict(dict)

    for line in IF:
        lines = line.strip().split("\t")
        MSIDict[lines[4]] = lines[0] + "\t" + lines[1] + "\t" + lines[2] + "\t" + lines[3]


    return MSIDict

def Analysis_Database(InInfo, InData):

    InI = open(InInfo, 'r')

    for line in InI:
        if line.startswith("癌种"):
            lines = line.strip().split("\t")
            Type = lines[1]

    InD = open(InData, 'r')
    Research = dict()

    for Line in InD:
        if Line.startswith("RefID"):
            continue
        else:
            Lines = Line.strip().split("\t")
            if Type == "肺癌" and Lines[7] != "/":
                Research[Lines[0]][]##############################
            else:


def Get_MSI(msiDict, InDel, OutFile):

    InF = open(InDel, 'r')
    OutF = open(OutFile, 'w')
    MSI = dict()

    for Line in InF:
        if Line.startswith("Chrom"):
            continue
        else:
            Lines = Line.strip().split("\t")
            MutBase = Lines[18][1:]
            AF = float(Lines[6].split("%")[0])
            for Mut in msiDict:
                MutInfo = msiDict[Mut].split("\t")
                if Lines[0] == MutInfo[0] and Lines[1] >= MutInfo[1] and Lines[1] <= MutInfo[2] and len(MutBase) > 2 and AF >= 0.1:
                    MSI[Mut] = MSI.get(Mut, 0) + 1
                else:
                    MSI[Mut] = MSI.get(Mut, 0) + 0

    MSI_Deg = 0
    for Gene in MSI:
        if int(MSI[Gene]) > 0:
            MSI_Deg += 1
    if MSI_Deg == 0:
        OutF.write("微卫星稳定(MSS)" + "\t" + "mss")
    elif MSI_Deg > 0 and MSI_Deg < 2:
        OutF.write("微卫星不稳定(MSI-L)" + "\t" + "msi-l")
    else:
        OutF.write("微卫星高度不稳定(MSI-H)" + "\t" + "msi-h")




InputMSI = sys.argv[1]
InputDel = sys.argv[2]
InputDa = sys.argv[3]
InputInfo = sys.argv[4]
OutputFile = sys.argv[5]
MDict = Analysis_MSI(InputMSI)
Get_MSI(MDict, InputDel, OutputFile)
