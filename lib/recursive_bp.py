#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from collections import Counter
import sys

#def virtual_p(sam,  out_dat, breakP_info):
def virtual_p(sam):
    
    breakP_sam = sam.rstrip(".sam") + "_final_Fetched.sam" 
    bp_handle = open(breakP_sam, "w")

    d_AR = {}
    d_reads = []

    samH = open(sam, "r")
    for line in samH:

        if line.startswith("@"):
            continue
        else:
            spLine = line.strip().split("\t")
            ID = spLine[0]
            matchP = spLine[3]
            #matchL = int(spLine[5].strip("M"))
            d_AR[ID+ "_" + matchP] = 0
            d_reads.append(matchP)

    samH.close()

    cnt = Counter(d_reads)
    mostcnt = cnt.most_common()
    #print (list(cnt.elements()))    
    #print (mostcnt[0])

    Set_VR1 = set()
    
    for i in d_AR:
        bp = i.split("_")[1]
        #print(bp)
        if bp ==  mostcnt[0][0]:
            Set_VR1.add(i.split("_")[0])

    #print(len(Set_VR1))

    ###########################################################
    d_AR1 = {}
    d_reads1 = []

    VR1_handle = open(sam, "r")
    for line1 in VR1_handle:

        if line1.startswith("@"):
            bp_handle.write(line1)
        else:
            spLine = line1.strip().split("\t")
            ID = spLine[0]
            matchP = spLine[3]
            if ID not in Set_VR1:
                #matchL = int(spLine[5].strip("M"))
                d_AR1[ID+ "_" + matchP] = 0
                d_reads1.append(matchP)
            if matchP == mostcnt[0][0]:
 
                bp_handle.write("{0}".format(line1))

    VR1_handle.close()
    
    if d_reads1 != []:
        cnt_Sec = Counter(d_reads1)
        mostcnt_Sec = cnt_Sec.most_common()

        #print (mostcnt_Sec[0])
        #print (mostcnt_Sec)
        ############################################################
        Set_VR2 = set()
        for j in d_AR1:
            bp = j.split("_")[1]
            if bp == mostcnt_Sec[0][0]:
                Set_VR2.add(j.split("_")[0])
     
        #print(len(Set_VR2))
        #print(Set_VR2)
        ############################################################
        d_AR2 = {}
        d_reads2 = []

        VR2_handle = open(sam, "r")
        for line2 in VR2_handle:

            if line2.startswith("@"):
                continue
            else:
                spLine2 = line2.strip().split("\t")
                ID = spLine2[0]
                matchP = spLine2[3]
                if ID not in Set_VR2 and ID not in Set_VR1:
                    #matchL = int(spLine[5].strip("M"))
                    d_AR2[ID+ "_" + matchP] = 0
                    d_reads2.append(matchP)
                if matchP == mostcnt_Sec[0][0]:
 
                    bp_handle.write("{0}".format(line2))

        VR2_handle.close()
        #print (d_AR2)


        if d_reads2 != []:

            Ext_Pre = sam.rstrip(".sam") + "_extra_pre.sam"
            Ext_Handle = open(Ext_Pre, "w")

            points_L = []

            cnt_Third = Counter(d_reads2)
            mostcnt_Third = cnt_Third.most_common()
            ThirdP =  [i[0] for i in mostcnt_Third[1:]]
            #print (ThirdP)
            VR3_handle = open(sam, "r")
            for line3 in VR3_handle:

                if line3.startswith("@"):
                    continue
                else:
                    spLine3 = line3.strip().split("\t")                    

                    matchP = spLine3[3]

                    if matchP in ThirdP:
                        points_L.append(line3.rstrip())

                    if matchP == mostcnt_Third[0][0]:
                        bp_handle.write("{0}".format(line3))

            VR3_handle.close()

            for tP in ThirdP:
                for PL in points_L:
                    x3 = PL.split("\t")[3]
                    if x3 == tP:
                        Ext_Handle.write(PL + "\n")

            Ext_Handle.close()
            #print(points_L[:3])            
            Final_List = []
            Final_s = open(sam.rstrip(".sam") + "_extraF.sam", "w")

            A_pre = open(Ext_Pre, "r")

            for a in A_pre:
                sa = a.rstrip().split("\t")
                ID = sa[0]

                if ID not in Final_List:
                    Final_s.write(a)
                    Final_List.append(ID)
            Final_s.close()
            A_pre.close()

    bp_handle.close()
    
virtual_p(sys.argv[1])


