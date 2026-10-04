#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from collections import defaultdict

def Filter_reads (Input_file, Output_file):
    File_I = open(Input_file, 'r')
    File_O = open(Output_file, "w")
    File = File_I.read()
    File_A = File.split("\n")
    Length = len(File_A)

    File_dict = defaultdict(list)

    for Line in range(Length):
        if File_A[Line] != "":
            if File_A[Line].startswith("@"):
                File_O.write(File_A[Line] + "\n")
                continue
            else:
                Lines = File_A[Line].strip().split("\t")
                File_dict[Lines[3]].append(len(Lines[9]))
                
    Array = []
    for i in File_dict:
        Values = File_dict[i]
        T_reads = len(Values)
        F_reads = 0
        for j in Values:
            if j >= 20:
                F_reads += 1
        if float(F_reads)/float(T_reads) > 0.2:
            Array.append(i)

    for line in range(Length):
        if File_A[line] != "":
            if File_A[line].startswith("@"):
                continue
            else:
                lines = File_A[line].strip().split("\t")
                if lines[3] in Array:
                    File_O.write(File_A[line] + "\n")

    File_I.close()
    File_O.close()



Filter_reads(sys.argv[1],sys.argv[2])

