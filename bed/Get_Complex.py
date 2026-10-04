#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
from collections import defaultdict

def Get_Complex(InFile, OutFile):

    InF = open(InFile, 'r')
    OutF = open(OutFile, 'w')
    
    for line in InF:
        lines = line.strip().split("\t")
        Ref_1 = lines[3][0]
        Ref_2 = lines[3][1]
        Mut_1 = lines[4][0]
        Mut_2 = lines[4][1]
        OutF.write("chr" + lines[0] + "," + lines[1] + "," + Ref_1 + "," + Mut_1 + "\t" + "chr" + lines[0] + "," + lines[2] + "," + Ref_2 + "," + Mut_2 + "\t" + lines[5] + "_" + lines[6] + "\t" + lines[5] + "_" + lines[6] + "\n")


    InF.close()
    OutF.close()



InputFile = sys.argv[1]
OutputFile = sys.argv[2]
Get_Complex(InputFile, OutputFile)
