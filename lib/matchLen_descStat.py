#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Title: matchLen_descStat.py
# Description: --------
# Author: KuDa Goose
# Date: 2017-08-30
# Version: 0.1

# notes: --------------
# python_version: 

from collections import Counter
from collections import defaultdict
import numpy as np
import argparse
import os, re
import sys

pat = re.compile("(\d+)[M|D]")

#def matchDescriptive(sam,  out_dat, breakP_info):
def matchDescriptive(sam, gene_info, data_sample):

    d_reads = defaultdict(list)

    samH = open(sam, "r")
    for line in samH:

        if line.startswith("@"):
            continue
        else:
            # split each line as spLine
            spLine = line.strip().split("\t")

            breakP = spLine[3]
            matchInfo = spLine[5]

            # get match length from CIGAR infomation
            P1_searchAll = pat.findall(matchInfo)
            MatchL = sum([int(i) for i in P1_searchAll])

            d_reads[breakP].append(MatchL)

    samH.close()
   
    dataForGraph = open(gene_info +"_" + data_sample + ".tsv" , "w")   ## gene name
    dataForGraph.write("breakPoints\teachRead_Length\n")
    
    matchP_info =  "matchStat_" + gene_info + "_" + data_sample + ".xls"                                  ## gene name
    bp_handle = open( matchP_info, "w")

    bp_handle.write("match_points\tReads_number\tMode\tMode_num\tmin\tmax\tlengthNum\tmean\tmedian\tstd\tone_quat\tthree_quat\n")

    for bp in d_reads:
        reads = d_reads[bp]
        for read in reads:
            dataForGraph.write(gene_info + "_" + bp +"\t" + str(read) + "\n")    ### gene name replace 'P_'

        bp_handle.write(bp + "\t" + str(len(reads)) + "\t" )
        cnt = Counter(reads)
        length_set = set(reads)
        length_num = len(length_set)
        mostcnt = cnt.most_common(15)[0]
        
        bp_handle.write("{0}\t{1}\t".format(mostcnt[0], mostcnt[1] ))
        arrayBP = np.array(reads)
        p_min  = arrayBP.min()
        p_max  = arrayBP.max() 
        p_mean = arrayBP.mean()
        p_median = np.median(arrayBP)
        p_sd   = arrayBP.std()

        ps = np.percentile(arrayBP, [25, 75])
        bp_handle.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\n".format(p_min, p_max,length_num, p_mean,p_median, p_sd, ps[0], ps[1]))

    bp_handle.close()
    dataForGraph.close()

if __name__ == "__main__":
    
    HELP = """USAGE: python {0} -i sf
                                -o op """.format(__file__)
             
    parser = argparse.ArgumentParser( description = HELP ) 

    parser.add_argument("-i", "--inputS", action='store', dest='inFile' , help="file name of input raw list")  
 
    parser.add_argument("-o", "--outGene", action='store' , default="EML4", help="output gene name") 
    parser.add_argument("-s", "--sample", default="exampleA" , help="prefix of sample name") 
    #parser.add_argument("-gn", "--geneName", default="EML4" , help="prefix of sample list filename") 

    
    args = parser.parse_args() 
    matchDescriptive(args.inFile, args.outGene, args.sample)
    

    #matchDescriptive(sys.argv[1], sys.argv[2], "93")



