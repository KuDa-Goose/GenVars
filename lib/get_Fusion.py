#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
from collections import defaultdict

def Get_Cancer(InTxt):
    
    InF = open(InTxt, 'r')
    Cancer = ""
   
    for Line in InF:
        if Line.startswith("癌种"):
            Lines = Line.strip().split("\t")
            if "肺" in Lines[1]:
                Cancer = "lung"
            else:
                Cancer = "CRC"
        else:
            continue
    return Cancer

def Analysis_Fusion(InFile, OutFile, InType):

    OutF = open(OutFile, 'w')
    IF = open(InFile, 'r')

    for line in IF:
        if line.startswith("Est_Type"):
            continue
        else:
            lines = line.strip().split("\t")
            #AF
            if lines[1] == "ALK":
                OutF.write("ALK" + "\t" + "融合突变" + "\t" + lines[1] + "-" + lines[2] + "\t" + " " + "\t" + lines[5] + "\t" + "alk_fusX" + "\t" + InType + "\n")
            elif lines[2] == "ALK":
                OutF.write("ALK" + "\t" + "融合突变" + "\t" + lines[1] + "-" + lines[2] + "\t" + " " + "\t" + lines[6] + "\t" + "alk_fusX" + "\t" + InType + "\n")
            else:
                continue

InputFile = sys.argv[1]
InputTxt = sys.argv[2]
OutputFile = sys.argv[3]
IType = Get_Cancer(InputTxt)
Analysis_Fusion(InputFile, OutputFile, IType)



