#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import defaultdict
from Bio import SeqIO
import sys

def Get_Base(InBed, InFasta, OutFile):

    InB = open(InBed, 'r')
    InF = open(InFasta, 'r')
    OutF = open(OutFile, 'w')
    PosD = defaultdict(dict)

    for line in InB:
        lines = line.strip().split("\t")
        PosD[lines[3]] = lines[0] + "\t" + lines[1] + "\t" + lines[2]
        

    for rec in SeqIO.parse(InFasta, "fasta"):
        ID = str(rec.id)
        Seq = str(rec.seq)
        Pos = str(PosD[ID]).split("\t")
        for i in range(len(Seq)):
            Position = int(i) + int(Pos[1]) + 1
            OutF.write(Pos[0] + "\t" + str(Position) + "\t" + Seq[i].upper() + "\n")

InputBed = sys.argv[1]
InputFasta = sys.argv[2]
OutputFile = sys.argv[3]
Get_Base(InputBed, InputFasta, OutputFile)
