#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
#def call_pos(stats, sam):

def call_pos( stats , lastLen):

    bps = []

    bpD = {}
    geneName = lastLen.split("_")[0]
    inStats = open( stats, "r" )

    maxInd = 0

    for num,i in enumerate(inStats):
        if i.startswith("match_points"):
            continue

        else:
            desc = i.strip().split("\t")

            rn = int(desc[1])
            mode = float(int(desc[3])) 
            maxLen = int(desc[5])

            if mode/rn < 0.7 and rn >= 20 and maxLen >= 75 and float(desc[7]) >= 15:
                bpD[desc[0]] = rn

                bps.append(desc[0])

    inStats.close()
        
    sort_readsL = sorted(bpD.values(), reverse=True)
    for i in bpD:
        if bpD[i] == sort_readsL[0]:
            maxInd = int(i)
    # matchStat_EML4_093.xls
    if sort_readsL != []:
        tmpLarge = sort_readsL[0]
    else:
        tmpLarge = 0
    tmpMaxD = {}
    cr =0

    re_inStat = open(stats, "r")
    for line in re_inStat:
        if line.startswith("match_points"):
            continue
        else:
           reSplit = line.strip().split("\t")
           rrn = int(reSplit[1])
           matchInd = int(reSplit[0])
           #print(matchInd)
           #if (reSplit[0] in bpD and (matchInd > maxInd +5 or matchInd < maxInd -5)) or (matchInd < maxInd+5 and matchInd >maxInd -5 and rrn >= sort_readsL[0] * 0.01):
           if reSplit[0] in bpD and (matchInd > maxInd +5 or matchInd < maxInd -5):
               print("_".join(stats.strip(".xls").split("_")[-1:0:-1]) , end="\t")
               print(geneName + "_" +line.strip())
           elif matchInd < maxInd+5 and matchInd >maxInd -5 and rrn != sort_readsL[0]:
               tmpLarge += rrn
           elif rrn == tmpLarge:
               cr = rrn
               tmpMaxD[rrn] = "\t".join(reSplit[2:])

    if tmpLarge != 0:
        print("_".join(stats.strip(".xls").split("_")[-1:0:-1]) , end="\t")
        print(geneName + "_" + str(maxInd) + "\t" + str(tmpLarge) + "\t" + tmpMaxD[cr] )

    re_inStat.close()


    dA = open( lastLen , 'r' )
    filtered_A = open("Z_" + lastLen, "w")

    for line in dA:
        if line.startswith("breakPoints"):
            filtered_A.write(line)
        else:
            asP = line.strip().split("\t")[0].split("_")[1]
            if asP in bps:
                filtered_A.write(line)

    filtered_A.close()
    dA.close()

#call_pos( "out_*_dat.xls"  ,"Dat_*.tsv" )
call_pos( sys.argv[1]  , sys.argv[2] )




