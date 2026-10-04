# -*- coding: UTF-8 -*-
from collections import defaultdict
import sys
import os
import re

def Get_Ras(InFile, InInfo, OutFile):

    InF = open(InFile, 'r')
    InI = open(InInfo, 'r')
    OutF = open(OutFile, 'w')
    Info = []
    Type = ''
    RAS = 0

    for Line in InI:
        if Line.startswith("检测癌种"):
            Lines = Line.strip().split("\t")
            if "肺" in Lines[1]:
                Type = "lung"
            else:
                Type = "CRC"
        else:
            continue
    for line in InF:
        if line.startswith("##"):
           Num = int(line.strip().split("##")[1])
        else:
            if Num == 0 and Type == "CRC":
                continue
                # = "RAS\t野生型\t不适用\t不适用\t不适用\tras_wt\tCRC\t1"
            elif int(Num) > 0 and Type == "CRC":
                lines = line.strip().split("\t")
                if (lines[0] == "KRAS" or lines[0] == "NRAS" or lines[0] == "BRAF" or lines[5] == "pik3ca_e21onc"):
                    RAS+=1
                else:
                    RAS+=0
                Info.append(line.strip())
            else:
                Info.append(line.strip())
                print("2")

    if Type == "CRC" and int(Num) == 0:
        OutF.write("##1\n")
        OutF.write("RAS\t野生型\t不适用\t不适用\t不适用\tras_wt\tCRC\t1\n")
    elif Type == "CRC" and int(Num) > 0 and RAS == 0:
        OutF.write("##" + str(int(Num) + 1) + "\n")
        OutF.write("RAS\t野生型\t不适用\t不适用\t不适用\tras_wt\tCRC\t1\n")
        for i in Info:
            Infos = i.strip().split("\t")
            OutF.write(Infos[0] + "\t" + Infos[1] + "\t" + Infos[2] + "\t" + Infos[3] + "\t" + Infos[4] + "\t" + Infos[5] + "\t" + Infos[6] + "\t" + str(int(Infos[7]) + 1) + "\n")
    else:
        OutF.write("##" + str(Num) + "\n")
        for i in Info:
            OutF.write(i + "\n")

InputFile = sys.argv[1]
InputInfo = sys.argv[2]
OutputFile = sys.argv[3]
Get_Ras(InputFile, InputInfo, OutputFile)
