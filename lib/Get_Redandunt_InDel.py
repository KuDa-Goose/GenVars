# -*- coding: UTF-8 -*-

from collections import defaultdict
import sys

def Get_RefID(InFile):

    InF = open(InFile, 'r')
    RefID = defaultdict(dict)

    for Line in InF:
        if Line.startswith("Chrom"):
            continue
        else:
            Lines = Line.strip().split("\t")
            RefID[Lines[4]] = Lines[5]
    return RefID
    

def Analysis_SNV(InDB, OutFile, RefD):

    InD = open(InDB, 'r')
    OutF = open(OutFile, 'w')
    ReDanDict = dict()
    AFD = dict()

    for line in InD:
        lines = line.strip().split("\t")
        if float(lines[9].split("%")[0]) > 0.1:
            Trans = lines[2].split(",")
            if int(lines[3]) == 7 and int(lines[4]) == 55181299 and int(lines[5]) == 55181299 and "FQEA" in lines[2]:
                HGVS = "c.2290_2291ins12;p.A763_Y764insFQEA"
            else:
                HGVS = Trans[-2].split(":")[3] + ";" + Trans[-2].split(":")[4]
            ReDanDict[lines[8]] = HGVS + "," + ReDanDict.get(lines[8], "")
            AFD[lines[8]] = lines[9] + "," + AFD.get(lines[8], "")
            

    for MutN in ReDanDict:
        OutF.write(MutN + "\t" + RefD[MutN] + "\n" + ReDanDict[MutN] + "\t" + AFD[MutN] + "\n")


InputFile = sys.argv[1]
OutputFile = sys.argv[2]
InputFiles = sys.argv[3]
RefDict = Get_RefID(InputFiles)
Analysis_SNV(InputFile, OutputFile, RefDict)
