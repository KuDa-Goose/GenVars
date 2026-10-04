#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__      = "KuDa Goose"
__copyright__   = "Copyright 2024, A Biotech"
__credits__     = [
    "KuDa Goose", "Zongyun Qiao"]  # remember to add yourself
__license__     = "GPL"
__version__     = "0.1-dev, 20241028"
__maintainer__  = "KuDa Goose"
__email__       = "infozse@163.com"


from subprocess import Popen
from subprocess import PIPE
import subprocess
import argparse
import sys

class Solution(object):

    def __init__(self):
        self.sortsam = "/thinker/storage/Software/picard-tools-1.119/SortSam.jar"
    #java -jar /thinker/storage/Software/picard-tools-1.119/SortSam.jar INPUT=/results/python_tools/Sam_test/Sample_fus_test/example_Sams/break_point/$i.sam  OUTPUT=./$i.sorted.sam SORT_ORDER=coordinate
        self.samtools = "/thinker/storage/Software/samtools-1.5/samtools"
    #samtools view -bS $i.sorted.sam >$i.sorted.bam
    #samtools depth $i.sorted.bam >$i.deep

    def getReadsID(self, fq):

        allReadsId = []

        fqHandle = open(fq, "r")
        for num,line in enumerate(fqHandle):
            if num % 4 == 0:
                Rid = line.strip()
                allReadsId.append(Rid[1:])
        sReadsId = set(allReadsId)

        return sReadsId 
            

    def getFP(self, fpFile):
        p = []      # p is list containing break points of fusion

        fpHandle = open(fpFile, "r")

        for line in fpHandle:
            z = line.strip().split("\t")
            bp = z[1].split("_")[1]
            p.append(bp)

        return p
        
    def getCommon(self , fusionPoints,  samB):

        extPoints = []

        for i in fusionPoints:
            baseNum = int(i)
            for n in range(-5,6):
                x = baseNum + n
                extPoints.append(x)
        
        ReadsEML4 = []

        OE = open(samB, "r")    ## OE is file handle of EML4 sam
        for line in OE:
            if not line.startswith("@"):
                ces = line.strip().split("\t")
                if int(ces[3]) in extPoints:
                    ReadsEML4.append(ces[0])
        sr = set(ReadsEML4)

        OE.close()
        return sr


    def writeFiles(self, readsSet, samA, samB, outSamA, outSamB):

        wA = open(outSamA, "w")
        wB = open(outSamB, "w")

        O_ALK_H = open(samA, "r")
        for line in O_ALK_H:
            if line.startswith("@"):
                wA.write(line)
            else:
                AS = line.strip().split("\t")
                if AS[0] in readsSet:
                    wA.write(line)

        wA.close()
        O_B_H   = open(samB, "r")

        for line in O_B_H:
            if line.startswith("@"):
                wB.write(line)
            else:

                BS = line.strip().split("\t")
                if BS[0] in readsSet:
                    wB.write(line)

        print("Sam extracting Done!")

    def getDeep(self, sam1, sam2):

        ## analysis for sam1
        p1Sort    = sam1.replace(".sam", "_sorted.sam")
        p1Deep    = sam1.replace(".sam", "_pre.deep")

        p1        = Popen("java -jar %s INPUT=%s OUTPUT=%s SORT_ORDER=coordinate 1>/dev/null 2>&1" %(self.sortsam, sam1, p1Sort), stdout=PIPE, shell=True)
        (output, err) = p1.communicate() 
        p1_status = p1.wait()

        p1_to_Bam = Popen("%s view -bS %s > %s"%(self.samtools, p1Sort, p1Sort.replace(".sam", ".bam")), stdout=PIPE, shell=True )
        (output, err) = p1_to_Bam.communicate()
        p1_status = p1_to_Bam.wait()

        p1_depth  = Popen("%s depth %s > %s"%(self.samtools, p1Sort.replace(".sam", ".bam"), p1Deep), stdout=PIPE, shell=True)
        (output, err) = p1_depth.communicate()
        p1_status = p1_depth.wait()

        #subprocess.call("awk -F '\t' '{{if($2>31890 && $2<=32010){{print;}}}}' {0} > {1}".format(p1Deep, sam1.replace(".sam", ".deep")), shell=True)
        subprocess.call("awk -F '\t' '{{if($2>32373 && $2<=32453){{print;}}}}' {0} > {1}".format(p1Deep, sam1.replace(".sam", ".deep")), shell=True)
        ## analysis for sam2
        p2Sort    = sam2.replace(".sam", "_sorted.sam")
        p2Deep    = sam2.replace(".sam", ".deep")

        p2        = Popen("java -jar %s INPUT=%s OUTPUT=%s SORT_ORDER=coordinate 1>/dev/null 2>&1" %(self.sortsam, sam2, p2Sort), stdout=PIPE, shell=True)
        (output, err) = p2.communicate()
        p2_status = p2.wait()

        p2_to_Bam = Popen("%s view -bS %s > %s"%(self.samtools, p2Sort, p2Sort.replace(".sam", ".bam")), stdout=PIPE, shell=True )
        (output, err) = p2_to_Bam.communicate()
        p2_status = p2_to_Bam.wait()

        p2_depth  = Popen("%s depth %s > %s"%(self.samtools, p2Sort.replace(".sam", ".bam"), p2Deep), stdout=PIPE, shell=True)
        (output, err) = p2_depth.communicate()
        p2_status = p2_depth.wait()

    def generate_GraphData(self, num, deep1, deep2, out):

        resultData = open(out, "w")
        depD1 = {}

        depD2 = {}

        Aop = open(deep1, "r")
        for line in Aop:
            ZA = line.strip().split("\t")
            depD1[int(ZA[1])] = int(ZA[2])

        Aop.close()

        Bop = open(deep2, "r")
        for line in Bop:
            ZB = line.strip().split("\t")

            depD2[int(ZB[1])]= int(ZB[2])

        Bop.close()

        # HighestD = max(depD2.values())

        kB = depD2.keys()
        kA = depD1.keys()

        startN = 260
        numA = 85 - len(kA)

        resultData.write("position\tSampleX\n")
        for i in range(numA):
            resultData.write("{0}\t{1}\n".format(startN, 0))
            startN -= 1

        for k in sorted(kA, reverse = False ):

            resultData.write("{0}\t{1}\n".format(startN, depD1[k]))
            startN -= 1

        numB = 0
        for k in sorted(kB, reverse = False ):

            if k >= num:
                resultData.write("{0}\t{1}\n".format(startN, depD2[k]))
                startN -= 1

        for i in range(startN):
            resultData.write("{0}\t{1}\n".format(startN, 0))
            startN -= 1

        resultData.close()

if __name__ == "__main__":

    HELP = """USAGE: python {0} -i fusion_points
                                -a samA
                                -b samB
                                -A samOA
                                -B samOB
              """.format(__file__)
             
    parser = argparse.ArgumentParser( description = HELP ) 
 
    parser.add_argument("-i", "--in_fp",  action='store', help = "input file of breakpoints") 
    parser.add_argument("-a", "--geneA",   action='store', help = "file name of sam for geneA") 
    parser.add_argument("-b", "--geneB",   action="store", help = "file name of sam for geneB")
    parser.add_argument("-A", "--outSam1", action="store", dest = 's_A', default = "testA.sam" , help = "out A ")
    parser.add_argument("-B", "--outSam2", action='store', dest = 's_B', default = "testB.sam" , help = "out B ")  
    parser.add_argument("-o", "--result", action='store' , default = "SampleX.txt" , help = "result file with Depth")  
    
    args = parser.parse_args()

    if args.geneA == None or args.geneB == None:
        print(HELP) 
        sys.exit()

    processPipe    = Solution()

    breakpoints    = processPipe.getFP(args.in_fp)
    cr             = processPipe.getCommon(breakpoints, args.geneB)
    processPipe.writeFiles(cr, args.geneA, args.geneB, args.s_A, args.s_B)
   
    processPipe.getDeep(args.s_A, args.s_B)
    for i in breakpoints:
        ka = int(i)
        processPipe.generate_GraphData(ka , args.s_A.replace(".sam", ".deep"), args.s_B.replace(".sam", ".deep"), args.result)


