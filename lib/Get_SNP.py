#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
from collections import defaultdict


def Analysis_MSI(InFile):

    IF = open(InFile, 'r')
    Type_Info = ""

    for line in IF:
        if line.startswith("检测癌种"):
            lines = line.strip().split("\t")
            if lines[1] == "肺癌":
                Type_Info = "非小细胞肺癌"
            else:
                Type_Info = "结直肠癌"

    return Type_Info


def SNP_Var(InSNP):

    InS = open(InSNP, 'r')
    SNPDict = defaultdict(dict)

    for Line in InS:
        Lines = Line.strip().split("\t")
        SNPName = Lines[4] + "\t" + Lines[5]
        if Lines[7] == "非小细胞肺癌":
            SNPDict["非小细胞肺癌"][SNPName] = Lines[0] + "\t" + Lines[1] + "\t" + Lines[3] + "\t" + Lines[8] + "\t" + Lines[6]
        elif Lines[7] == "结直肠癌":
            SNPDict["结直肠癌"][SNPName] = Lines[0] + "\t" + Lines[1] + "\t" + Lines[3] + "\t" + Lines[8] + "\t" + Lines[6]
        else:
            SNPDict["非小细胞肺癌"][SNPName] = Lines[0] + "\t" + Lines[1] + "\t" + Lines[3] + "\t" + Lines[8] + "\t" + Lines[6]
            SNPDict["结直肠癌"][SNPName] = Lines[0] + "\t" + Lines[1] + "\t" + Lines[3] + "\t" + Lines[8] + "\t" + Lines[6]

    return SNPDict


def Analysis_SNP(InVCF, TInfo, SNPdict, OutFile):

    InV = open(InVCF, 'r')
    OutF = open(OutFile, 'w')

    for SNP in SNPdict[TInfo]:
        SNPInfo = SNPdict[TInfo][SNP].split("\t")
        AFList = []
        for line in InV:
            if line.startswith("Chrom") or line.startswith("#"):
                continue
            else:
                lines = line.strip().split("\t")
                AF = float(lines[6].strip("%"))
                if lines[0] == SNPInfo[0] and lines[1] == SNPInfo[1] and AF >= 10.0:
                    AFList.append(str(AF) + "\t" + lines[2] + "\t" + lines[3])
                else:
                    continue
        InV.seek(0)
        if SNPInfo[3] == "N" and len(AFList) > 0:
            AFInfo = AFList[0].split("\t")
            RefBase = DNA_complement(SNPInfo[2])
            RBase = DNA_complement(AFInfo[1])
            MutBase = DNA_complement(AFInfo[2])
        elif SNPInfo[3] == "P" and len(AFList) > 0:
            AFInfo = AFList[0].split("\t")
            RefBase = SNPInfo[2]
            RBase = AFInfo[1]
            MutBase = AFInfo[2]
        elif SNPInfo[3] == "X" and len(AFList) > 0:##G71R比较特殊，报告需要将名字改成*6
            RefBase = "*1"
            RBase = "*1"
            MutBase = "*6"
        elif SNPInfo[3] == "N" and len(AFList) == 0:
            RefBase = DNA_complement(SNPInfo[2])
            RBase = ""
            MutBase = ""
        elif SNPInfo[3] == "P" and len(AFList) == 0:
            RefBase = SNPInfo[2]
            RBase = ""
            MutBase = ""
        else:
            RefBase = "*1"
            RBase = ""
            MutBase = ""
        if len(AFList) >= 2:
            OutF.write(SNP + "\t" + "尚不明确" + "\t" + SNPInfo[4] + "\n")
        elif len(AFList) > 0 and len(AFList) < 2:
            if float(AFInfo[0]) <= 10.0:
                OutF.write(SNP + "\t" + RefBase + "/" + RefBase + "纯合子" + "\t" + SNPInfo[4] + "\n")
            elif float(AFInfo[0]) > 10.0 and float(AFInfo[0]) < 90.0:
                OutF.write(SNP + "\t" + RBase + "/" + MutBase + "杂合子" + "\t" + SNPInfo[4] + "\n")
            elif float(AFInfo[0]) >= 90.0:
                OutF.write(SNP + "\t" + MutBase + "/" + MutBase + "纯合子" + "\t" + SNPInfo[4] + "\n")
            else:
                OutF.write(SNP + "\t" + "尚不明确" + "\t" + SNPInfo[4] + "\n")
        else:
            OutF.write(SNP + "\t" + RefBase + "/" + RefBase + "纯合子" + "\t" + SNPInfo[4] + "\n")

def DNA_complement(sequence):
    sequence = sequence.upper()
    sequence = sequence.replace('A', 't')
    sequence = sequence.replace('T', 'a')
    sequence = sequence.replace('C', 'g')
    sequence = sequence.replace('G', 'c')
    return sequence.upper()

def Analysis_SNP_InDel(InIVCF, TyInfo, OutInDelFile):

    InSIV = open(InIVCF, 'r')
    OutFI = open(OutInDelFile, 'a')

    if TyInfo == "非小细胞肺癌":
        AFPList = []
        AFNList = []
        for Line in InSIV:
            if Line.startswith("Chrom"):
                continue
            else:
                Lines = Line.strip().split("\t")
                AFI = float(Lines[6].strip("%"))
                Base = Lines[3].split("/")[0]
                Str = Base[0]
                Seq = Base[1:]
                if Lines[0] == "chr18" and int(Lines[1]) >= int(673441) and int(Lines[1]) <= int(673459) and AFI >= 1.0 and Seq == "TTAAAG":
                    if Str == "+":
                        AFPList.append(float(AFI))
                    else:
                        AFNList.append(float(AFI))
        InSIV.seek(0)
        if len(AFPList) == 1:
            OutFI.write("TYMS\t3'UTR c.1494" + "\t" + "尚不明确" + "\t" + "tyms_3utr" + "\n")
        elif len(AFNList) == 1 and float(AFNList[0]) >= 10.0 and float(AFNList[0] <= 90.0):
            OutFI.write("TYMS\t3'UTR c.1494" + "\t" + "+6/-6杂合子" + "\t" + "tyms_3utr" + "\n")
        elif len(AFNList) == 1 and float(AFNList[0]) > 90.0:
            OutFI.write("TYMS\t3'UTR c.1494" + "\t" + "-6/-6纯合子" + "\t" + "tyms_3utr" + "\n")
        elif len(AFPList) == 0 or len(AFNList) == 0:
            OutFI.write("TYMS\t3'UTR c.1494" + "\t" + "+6/+6纯合子" + "\t" + "tyms_3utr" + "\n")
        else:
            OutFI.write("TYMS\t3'UTR c.1494" + "\t" + "尚不明确" + "\t" + "tyms_3utr" + "\n")
    else:
        AFIList = []
        for Line in InSIV:
            if Line.startswith("Chrom"):
                continue
            else:
                Lines = Line.strip().split("\t")
                AFI = float(Lines[6].strip("%"))
                Base = Lines[3].split("/")[0]
                Str = Base[0]
                Seq = Base[1:]
                SeqList = ["TA", "TATA", "TATATA", "TATATATA", "TATATATATA", "TATATATATATA", "TATATATATATATA", "TATATATATATATATA"]
                if Lines[0] == "chr2" and int(Lines[1]) >= int(233760230) and int(Lines[1]) <= int(233760264) and AFI >= 10.0 and Seq in SeqList:
                    AFIList.append(str(AF))
        InSIV.seek(0)
        if len(AFIList) >= 2:
            OutFI.write("UTG1A1\tTATA box" + "\t" + "尚不明确" + "\t" + "ugt1a1_28" + "\n")
        elif len(AFIList) == 1:
            if float(AFIList[0]) > 10.0 and float(AFIList[0]) < 90.0:
                OutFI.write("UTG1A1\tTATA box" + "\t" + "*1/*28杂合子" + "\t" + "ugt1a1_28" + "\n" )
            elif float(AFIList[0]) >= 90.0:
                OutFI.write("UTG1A1\tTATA box" + "\t" + "*28/*28杂合子" + "\t" + "ugt1a1_28" + "\n")
            else:
                OutFI.write("UTG1A1\tTATA box" + "\t" + "尚不明确" + "\t" + "ugt1a1_28" + "\n")
        else:
            OutFI.write("UTG1A1\tTATA box" + "\t" + "*1/*1纯合子" + "\t" + "ugt1a1_28" + "\n")

InputSampleInfo = sys.argv[1]
InputSNPBed = sys.argv[2]
InputSNPVcf = sys.argv[3]
OutputFile = sys.argv[4]
InputSNPInDelVcf = sys.argv[5]

SNPType = Analysis_MSI(InputSampleInfo)
SNP_Dict = SNP_Var(InputSNPBed)
Analysis_SNP(InputSNPVcf, SNPType, SNP_Dict, OutputFile)
Analysis_SNP_InDel(InputSNPInDelVcf, SNPType, OutputFile)

