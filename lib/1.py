#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import sys

def Analysis_SNV(InDB):

    InD = open(InDB, 'r')
    SNVInfo = defaultdict(dict)
    CancerT = defaultdict(dict)
    RefID = defaultdict(dict)
    RASID = defaultdict(dict)
    
    for line in InD:
        if line.startswith("Gene"):
            continue
        else:
            lines = line.strip().split("\t")
            SNVInfo[lines[0] + "_" + lines[1]] = lines[0] + "_" + lines[2] + "\t" + lines[5] + ";" + lines[6]
            RefID[lines[0] + "_" + lines[2]] = lines[4]
            RASID[lines[0] + "_" + lines[1]] = lines[4]
            CancerT[lines[0]] = 0
            #SNVInfo[lines[1] + "_" + lines[2]] = lines[1] + "_" + lines[3] + "\t" + lines[6] + ";" + lines[7]
            #CancerT[lines[1] + "_" + lines[2]] = lines[13]

    return SNVInfo, RefID, CancerT, RASID




def Trans_SNV(InFile, InDict, RefIDDict, InInFo, GList, OutFile, RasDict):

    InF = open(InFile, 'r')
    InInfo = open(InInFo, 'r')
    Info = defaultdict(dict)
    MutL = []
    IT = ""

    for Line in InInfo:
        if Line.startswith("检测癌种"):
            Lines = Line.strip().split("\t")
            if "肺" in Lines[1]:
                IT = "lung"
            else:
                IT = "CRC"
        else:
            continue

    for line in InF:
        lines = line.strip().split("\t")
        if lines[0].endswith("Sample"):
            MutL = lines[1:]
        else:
            for i in range(0, len(lines)-1, 3):
                MutName = MutL[i].rsplit("_", 1)[0] 
                #Info[lines[0]][MutName] = lines[i] + "\t" + lines[i+1] + "\t" + lines[i+2]
                Info[lines[0]][MutName] = lines[i+3]


    for Sample in Info:
        OutF = open(OutFile, 'w')
        MutDictC = dict()
        MutDictP = dict()
        AFDict = dict()
        RAS = 0
        for Mut in Info[Sample]:
            if Info[Sample][Mut] == "0":
                AF = 0
            else:
                AF = float('%.1f' % float(Info[Sample][Mut].strip("%")))
            Gene = Mut.split("_")[0]
            if (Gene == "KRAS" or Gene == "NRAS" or Gene == "BRAF" or RasDict[Mut] == "pik3ca_e21onc" ) and AF > 0:
                RAS+=1
            else:
                RAS+=0
            if AF >= 0.01:
                MutN = str(InDict[Mut]).split("\t")[0]
                HGVS = str(InDict[Mut]).split("\t")[1]
                HGVSC = HGVS.split(";")[0]
                HGVSP = HGVS.split(";")[1]
                MutDictC[MutN] = HGVSC + "," + MutDictC.get(MutN, "")
                MutDictP[MutN] = HGVSP + "," + MutDictP.get(MutN, "")
                MutAF = str(AF) + "%"
                AFDict[MutN] = MutAF + "," + AFDict.get(MutN, "")
                #OutF.write(str(MutN) + "\t" + "NA" + "\n" + str(HGVS) + "\t" + str(Info[Sample][Mut]) + "\n")
            else:
                continue
        G_AFDict = list()
        #for G in GList:
            #AAAADict = dict()
            #for M in AFDict:
            #    if M.split("_", 1)[0] == G:
            #        AAAADict[M] = AFDict[M]
            #S_A = sorted(AAAADict.items(), key=lambda items:items[1], reverse=True)
            #G_AFDict = G_AFDict + S_A
        S_AFDict = sorted(AFDict.items(), key=lambda items:items[1], reverse=True)
        GD = defaultdict(dict)
        #for MName in G_AFDict:
        if RAS == 0 and IT == "CRC":
            OutF.write("RAS野生型" + "\t" + " " + "\t" + "不适用" + "\t" + "不适用" + "\t" + "不适用"  + "\t" + "ras_wt" + "\t" + IT + "\n")
        for MName in S_AFDict:
            HGVSsC = MutDictC[MName[0]].rsplit(",", 1)[0]
            HGVSsP = MutDictP[MName[0]].rsplit(",", 1)[0]
            AFs = AFDict[MName[0]].rsplit(",", 1)[0]
            OutF.write(MName[0].split("_", 1)[0] + "\t" + MName[0].split("_", 1)[1] + "\t" + HGVSsC + "\t" + HGVSsP + "\t" + AFs + "\t" + RefIDDict[MName[0]] + "\t" + str(IT) + "\n")
            GD[MName[0].split("_", 1)[0]] = 1
        #s = 1
        #for g in GD:
        #    OF.write(str(s) + "\t" + g + "\t" + str(InType[Sample]) + "\n")
        #    s+=1
    

InputDatabase = sys.argv[1]
InputSNV = sys.argv[2]
InputFile = sys.argv[3]
OutputFile = sys.argv[4]

SNVDict, RefDict, GeneDict, RASDict = Analysis_SNV(InputDatabase)
GeneL = GeneDict.keys()
GeneList = sorted(GeneL)
Trans_SNV(InputSNV, SNVDict, RefDict, InputFile, GeneList, OutputFile, RASDict)
