import os
import sys

def Get_UMI(InFile, OutFile):

    SeqID = dict()
    InF = open(InFile, 'r')
    OutF = open(OutFile, 'w')

    for line in InF:
        lines = line.strip().split("\t")
        Info = lines[0] + "\t" + lines[1] + "\t" + lines[2] + "\t" + lines[3] + "\t" + lines[4]
        SeqID[Info] = line

    for S in SeqID:
        OutF.write(SeqID[S])

InputFile = sys.argv[1]
OutputFile = sys.argv[2]
Get_UMI(InputFile, OutputFile)
