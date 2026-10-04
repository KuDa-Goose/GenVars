#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__      = "KuDa Goose"
__copyright__   = "Copyright 2024, A Biotech"
__credits__     = [
    "KuDa Goose", "Zongyun Qiao"]  # remember to add yourself
__license__     = "GPL"
__version__     = "0.2-dev, 20241028"
__maintainer__  = "KuDa Goose"
__email__       = "infozse@163.com"


from collections import defaultdict
from collections import Counter
import itertools
import pprint
import argparse
import os,re
import numpy as np


d1 = defaultdict(list)
pat = re.compile("(\d+)[M|D]")

parser = argparse.ArgumentParser( description = "USAGE" ) 
 
parser.add_argument("-i", "--in_Sam",  action='store', help = "input file of breakpoints") 
parser.add_argument("-o", "--gene",  action='store', default="EML4", help = "output gene name")
parser.add_argument("-s", "--sample", default="exampleA" , help="prefix of sample name")

args = parser.parse_args()

out_tsv = open(args.gene + "_" + args.sample + ".tsv" , "w")
out_tsv.write("breakPoints\teachRead_Length\n")

d_reads = defaultdict(list)
d_len = {}
opSam = open(args.in_Sam, "r")
for line in opSam:
    if line.startswith("@"):
        continue
    else:
       ssLine = line.strip().split("\t")
       readsId = ssLine[0]

       P1_search = pat.findall(ssLine[5])
       MatchL = sum([int(i)for i in P1_search])
       d_len[readsId] = MatchL
       pos  = int(ssLine[3])
       d1[readsId].append(pos)
       d_reads[pos].append(MatchL)
opSam.close()

tsv_arr =[]
for bp in d_reads:
        reads = d_reads[bp]
        for read in reads:
            out_tsv.write(args.gene + "_" + str(bp) + "\t" + str(read) + "\n") 
            tsv_arr.append(args.gene + "_" + str(bp) + "\t" + str(read) + "\n")
out_tsv.close()

all_sites = list(itertools.chain.from_iterable(d1.values()))


stat_raw = {}
Pos_num = {}
Pos = []
stat_pos = []

out_name_stat = "matchStat_" + args.gene + "_" + args.sample + ".xls"
out = open(out_name_stat,"w")
out.write("match_points\tReads_number\tMode\tMode_num\tmin\tmax\tlengthNum\tmean\tmedian\tstd\tone_quat\tthree_quat\n")

while True:
    mc = Counter(all_sites).most_common()
    ma = filter(lambda x : mc[0][0] in d1[x], d1.keys())
    m_remain = filter(lambda x : mc[0][0] not in d1[x], d1.keys())
    if mc == []:
        break

    M_pos = mc[0][0]
    Reads_num = mc[0][1]

    Len_reads =[]
    for i in ma:
        Len_reads.append(d_len[i])

    mode = Counter(Len_reads).most_common()
    Length = Counter(Len_reads)
    
    arr_Len = np.array(Len_reads)
    Mode = mode[0][0]
    Mode_num = mode[0][1]
    Reads_min = min(mode)[0]
    Reads_max = max(mode)[0]
    length_num = len(Length)
    Reads_mean = arr_Len.mean()
    Reads_median = np.median(arr_Len)
    Reads_std = arr_Len.std()
    ps = np.percentile(arr_Len,[25,75])
    Reads_25 = ps[0]
    Reads_75 = ps[1]
    out.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n".format(M_pos, Reads_num, Mode, Mode_num, Reads_min, Reads_max, length_num, Reads_mean, Reads_median, Reads_std, Reads_25, Reads_75))
    d1 = dict([(k, d1[k]) for k in m_remain ])
    all_sites = list(itertools.chain.from_iterable(d1.values()))

    values = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}\n".format(M_pos, Reads_num, Mode, Mode_num, Reads_min, Reads_max, length_num, Reads_mean, Reads_median, Reads_std, Reads_25, Reads_75)
    stat_raw[M_pos] = values
    stat_pos.append(M_pos)
    if float(Mode_num)/Reads_num < 0.7 and Reads_num >= 15 and Reads_max >= 55 and Reads_mean >= 10:
        Pos_num[M_pos] = Reads_num
        Pos.append(str(M_pos))
out.close()

maxInd = 0
sort_readsL = sorted(Pos_num.values(), reverse=True)
for i in Pos_num:
    if Pos_num[i] == sort_readsL[0]:
        maxInd = int(i)
# matchStat_EML4_093.xls
if sort_readsL != []:
    tmpLarge = sort_readsL[0]
else:
    tmpLarge = 0
tmpMaxD = {}
cr =0

out_fusion = args.gene + "_fusion_" + args.sample + ".txt"
out_F = open(out_fusion,"w")

for line in stat_pos:
    reSplit = stat_raw[line].strip().split("\t")
    rrn = int(reSplit[1])
#    print(line)
    matchInd = int(reSplit[0])
    if reSplit[0] in Pos_num and (matchInd > maxInd +5 or matchInd < maxInd -5):
        out_F.write(args.sample + "_" + args.gene + "_" + "\t")
        out_F.write(args.gene + "_" + line.strip())
        
    elif matchInd < maxInd+5 and matchInd >maxInd -5 and rrn != sort_readsL[0]:
        tmpLarge += rrn
    elif rrn == tmpLarge:
        cr = rrn
        tmpMaxD[rrn] = "\t".join(reSplit[2:])
if tmpLarge != 0:
    out_F.write(args.sample + "_" + args.gene + "_" + "\t")
    out_F.write(args.gene + "_" + str(maxInd) + "\t" + str(tmpLarge) + "\t" + tmpMaxD[cr] + "\n")
out_F.close()

filtered_A = open("Z_" + args.gene + "_" + args.sample + ".tsv", "w")
for line in tsv_arr:
    asP = line.strip("\n").split("\t")[0].split("_")[1]
    if asP in Pos:
        filtered_A.write(line)
filtered_A.close()

