#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import Counter
from collections import defaultdict
import argparse
import os


def create_gnu_conf( dat, col_num, sample_Num):

    data_o = open(dat, "r")
    for line in data_o:
        if line.startswith("#"):
            headers = line.strip().split("\t")[1:]
            break
    data_o.close()


    gnu_handle = open("scatter_plot.conf" ,"w")
    gnu_handle.write("""set terminal png  xC9C9C9\n \
                        set output "Line_ReadsNum_image_{0}.png"\n \
                        set xlabel "Match Length"\n \
                        set ylabel "reads number"\n \
                        set grid\n \
                        set autoscale\n \
                        set title "Test Fusion point EML4 length"\n \
                        file = "{1}"\n """.format(sample_Num, dat))

    gnu_handle.write("plot ")
    for i in range(col_num-1):
        gnu_handle.write("file using 1:{0} with linespoint title \"{1}\", ".format(i+2, headers[i]))
    gnu_handle.write("file using 1:{0} with linespoint title \"{1}\"".format(col_num+1, headers[col_num - 1]))
    gnu_handle.write("\n")    
        
    gnu_handle.close()


def matchPoints_filter(sam,  out_dat, breakP_info):

    d_posCount = defaultdict(list)
    d_reads = []

    samH = open(sam, "r")
    for line in samH:
        
        if line.startswith("@"):
            continue
        else:
            spLine = line.strip().split("\t")
            
            matchP = spLine[3]
            matchL = int(spLine[5].strip("M"))

            d_reads.append(matchP)
            d_posCount[matchP].append(matchL) 


    samH.close()

    cnt = Counter(d_reads)
    mostcnt = cnt.most_common(15)

    bp_handle = open(breakP_info, "w")
    for i in mostcnt:
        bp_handle.write("{0}\t{1}\n".format(i[0], i[1]))
    bp_handle.close()
    
    datN = 0

    ## get max len of first breakpoint
    firstP = max(d_posCount[mostcnt[0][0]])

    length_All = defaultdict(list)

    A_mostP = [i[0] for i in mostcnt]
    D_info = defaultdict(list)
    samHB = open(sam , "r")

    for line in samHB:
        if line.startswith("@"):
                continue
        else:
            apLine = line.strip().split("\t")

            ID = apLine[0]

            matchP = apLine[3]
            if matchP in A_mostP:
                D_info[ID].append(matchP)

    samHB.close()

    outInfo = open(out_dat + "_INFO.txt", "w")
    for ap in D_info:
        outInfo.write("{0}\t{1}\n".format(ap, ",".join(D_info[ap])))
    outInfo.close() 
    
    ##################################    

    #for p in (i[0] for i in mostcnt):
    for p in A_mostP:
        
        datN += 1

        OutDat = open(out_dat + str(datN) + ".dat" ,"w")
        cntP = Counter(d_posCount[p])
        KP = cntP.keys()
        ##maxLen = max(KP)
        ##for x in range(5, maxLen + 1):

        for x in range(5, firstP + 1):
            if x not in KP:
                OutDat.write("{0}\t0\n".format(x))
                length_All[p].append(0)
            else:
                OutDat.write("{0}\t{1}\n".format(x, cntP[x]))
                length_All[p].append(cntP[x])
        OutDat.close()

    DatAll = open( out_dat + "_All.dat", "w")
    DatAll.write("#length")
    for bp in A_mostP:
        DatAll.write("\tP_{0}".format(bp))
    DatAll.write("\n")

    for j in range(5, firstP + 1):
        DatAll.write(str(j))
        for bp in A_mostP:
            DatAll.write("\t{0}".format(length_All[bp][j-5]))
        DatAll.write("\n")

    DatAll.close()

if __name__ == "__main__":
    
    HELP = """USAGE: python {0} -i sf
                                -s outDat """.format(__file__)
             
    parser = argparse.ArgumentParser( description = HELP ) 

    parser.add_argument("-i", "--inputS", action='store', dest='samFile' , help="file name of input sam")   
    parser.add_argument("-o", "--outS", default="dat_reads" , help="prefix of data filename for plotting") 
    parser.add_argument("-b", "--breakP", default="reads_breakpoints_EML4.xls", help="break points number")

    args = parser.parse_args() 

    matchPoints_filter(args.samFile , args.outS, args.breakP)

    create_gnu_conf(args.outS + "_All.dat", 15, args.outS)
    os.system("cat scatter_plot.conf | gnuplot")
