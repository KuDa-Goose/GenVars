#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import Counter
from collections import defaultdict
from Bio import SeqIO
import argparse
import os
import sys

def Analysis_Fastq(In1Fastq, In2Fastq, OutFastq):
 
    FastqID = []

    for rec in SeqIO.parse(In1Fastq, "fastq"):
       #FastqID.append(str(rec.id))
        FastqID.append(str(rec.id).split("/")[0])

    r1 = (Rec for Rec in \
        SeqIO.parse(In2Fastq, "fastq") \
        if str(Rec.id).split("/")[0] in FastqID)
        #if str(Rec.id) in FastqID) 
    SeqIO.write(r1, OutFastq, "fastq")



InputFastq_1 = sys.argv[1]
InputFastq_2 = sys.argv[2]
OutputFastq = sys.argv[3]
Analysis_Fastq(InputFastq_1, InputFastq_2, OutputFastq)
