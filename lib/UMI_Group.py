import os
import sys
from Bio import SeqIO

def Get_UMI(InFastq):

    SeqID = dict()

    for rec in SeqIO.parse(InFastq, "fastq"):
        ID = str(rec.id).split("/")[0]
        UMI = ID.split(":")[-1]
        Fasta = str(rec.id) + "," + str(rec.seq)
        SeqID[UMI] = Fasta + "\t" + SeqID.get(UMI, "")

    return SeqID


InputFastq = sys.argv[1]
OutputFasta = sys.argv[2]
UMI_dict = Get_UMI(InputFastq)
for UMISeq in UMI_dict:
    #print (UMISeq + "\t" + str(UMI_dict[UMISeq]))
    OutFa = OutputFasta + "_" + UMISeq + ".R2.fasta"
    OutF = open(OutFa, 'w')
    SeqList = UMI_dict[UMISeq].strip().split("\t")
    for i in SeqList:
        FaInfo = i.split(",")
        OutF.write(">" + FaInfo[0] + "\n" + FaInfo[1] + "\n")


