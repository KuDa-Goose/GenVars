#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
import sys

def Trans_SNV(InFile, OutFile):

    InF = open(InFile, 'r')
    OutF = open(OutFile, 'w')
    Info = defaultdict(dict)

    for Line in InF:
        Lines = Line.strip().split("\t")
        if Lines[0].endswith("Sample"):
            SNV_List = Lines[1:]
            SNV_Number = len(SNV_List)
        else:
            for i in range(1,SNV_Number + 1):
                Info[SNV_List[i-1]][Lines[0]] = Lines[i]

    Sample_List = defaultdict(dict)
    for SNV in SNV_List:
        for Sample in Info[SNV]:
            Sample_List[Sample] = 1

    Title = "SNV_Name" + "\t" + "Type"
    for i in Sample_List:
        Title += "\t" + i
    OutF.write(Title + "\n")

    for SNV in SNV_List:
        Type = SNV.split("_")[-1]
        Mut_List = SNV + "\t" + Type
        for Sample in Sample_List:
            Mut_List += "\t" + Info[SNV][Sample]
        OutF.write(Mut_List + "\n")


InputFile = sys.argv[1]
OutputFile = sys.argv[2]
Trans_SNV(InputFile, OutputFile)
