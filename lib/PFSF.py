#!/usr/bin/env python
# -*- coding: UTF-8 -*-

## This is a Program For Single-end reads Fusion scanning (PFSF)

__author__      = "KuDa Goose"
__copyright__   = "Copyright 2024, A Biotech"
__credits__     = [
    "KuDa Goose"]  # remember to add yourself
__license__     = "GPL"
__version__     = "0.2-dev, 20241028"
__maintainer__  = "KuDa Goose"
__email__       = "infozse@163.com"

from collections import OrderedDict
from time import time, localtime, strftime
from glob import glob
import argparse
import os, sys, re
import shutil
import shlex
import subprocess
import yaml

dbase = {"A":"T", "C":"G", "T":"A", "G":"C"}

def load_cNew(config_f):

    with open(config_f, encoding="utf-8") as in_handle:
        config = yaml.safe_load(in_handle)
    return (config["cutFQ"], config["softwares"], config["customScriptLib"], config["geneFus"])

def revComp(seq, qua):
    x = ""
    for i in seq:
        x   += dbase[i]
    #    rx   = x[::-1]
    rx   = x[::-1]
    rq = qua[::-1]
    return rx, rq

def aln_to_fusGene( SoftW, FQ_in, sampleN, genea, genea_Index, c_bool = False):
    outFile = "R_" + sampleN + ".fq"

    if not os.path.exists("log"):
        os.mkdir("log")

    if not os.path.exists(outFile):
        if c_bool == True:
            cut_command = shlex.split(SoftW["curr_python"] + " " + SoftW["cutadapt"]+ " -g CGCAGTAGACCTCATTCCT "+ FQ_in + " -o " +outFile + " 1>./log/cutadapt_log.txt 2>&1")
            subprocess.call(cut_command)
        else:
            shutil.copy(FQ_in, outFile)
    ## aligning with bwa, mapping to ALK and generating out_1.bam , /results/Probe_fusion/ref_index/ALK_gene.fa

    alnSam = "Aln_{0}_{1}.sam".format(genea, sampleN)
    if not os.path.exists(alnSam):
        print("Start Fusion analysis %s at %s, fastq will be aligned to /results/Probe_fusion/ref_index/ALK_gene.fa\n"%(sampleN, strftime("%b %d %Y %H:%M:%S",localtime(time())) ))

        alnCmd = "%s mem -R \"@RG\\tID:FusionA\\tSM:NGS\\tPL:Proton\" -p -t 4 -O 4,4 -B 3 -T 20 %s %s > Out_%s_%s.sam 2> ./log/%s_bwa.err\n"%( SoftW["bwa"], genea_Index, outFile, genea, sampleN, sampleN)
        retcode = subprocess.call(alnCmd, shell=True)
        filterSamCmd = "%s view -h -f 16 Out_%s_%s.sam > Aln_%s_%s.sam\n"%(SoftW["samtools"], genea, sampleN, genea, sampleN )
        if retcode == 0:
            subprocess.call(filterSamCmd, shell=True)
    else:
        pass
    return alnSam

def splitSam(sam):
    ## split out_1.bam and trim 3' end fragments which mapped to ALK gene
    
    Pat1 =  re.compile("^\d+M.*?(\d+)S$")
    Pat2 =  re.compile("^1S\d+M.*?(\d+)S$")
    Pat3 =  re.compile("^2S\d+M.*?(\d+)S$")
    Pat4 =  re.compile("^\d+M.*?(\d+)H$")

    ## Output fastq Name: aligned reads and split softclipping fragments to Fus_*_split.fq
    sn = sam.split("_")[2].split(".")[0]
    OQ = "Fus_" + sn + "_split.fq"

    if not os.path.exists(OQ):
        sam_Handle = open(sam, "r")
        fq_h = open(OQ, "w")

        for line in sam_Handle:
            FS = line.strip().split("\t")
            if line.startswith("@"):
                continue
            else:
                ID            = FS[0]
                Quality       = FS[10]
                seq           = FS[9]

                revCseq, revQ = revComp(seq, Quality)

                match1 = Pat1.match(FS[5])
                match2 = Pat2.match(FS[5])
                match3 = Pat3.match(FS[5])
                match4 = Pat4.match(FS[5])

                if FS[1] == "16" and match1:
                    Len = int(match1.group(1))
                    fq_h.write("@{0}\n{1}\n+\n{2}\n".format(ID, revCseq[0:Len], revQ[0:Len]))

                elif FS[1] == "16" and match2:
                    Len2 = int(match2.group(1))
                    fq_h.write("@{0}\n{1}\n+\n{2}\n".format(ID, revCseq[0:Len2], revQ[0:Len2]))

                elif FS[1] == "16" and match3:
                    Len3 = int(match3.group(1))
                    fq_h.write("@{0}\n{1}\n+\n{2}\n".format(ID, revCseq[0:Len3], revQ[0:Len3]))
                elif match4 and (FS[1] == "2064" or FS[1] == "16"):
                    Len4 = int(match4.group(1))
                    fq_h.write("@{0}\n{1}\n+\n{2}\n".format(ID, revCseq[0:Len4], revQ[0:Len4]))
        fq_h.close()
        sam_Handle.close()

    return OQ

def SepAln_diffReads(softW, fq, geneNFus, bt1Lib, bt2Lib):
    sn = fq.split("_")[1]
    aln_paras = [ "4_10_bowtie1_v0",
                  "10_20_bowtie1_v1",
                  "20_40_bowtie1_v2",
                  "40_50_bowtie1_v3",
                  "50_2000_bowtie2_N0" ]
    for z in aln_paras:
        zp = z.split("_")
        handle = open(fq, "r")
        outHandle = open("T_" + sn + "_" + zp[0] + "_" + zp[1] + ".fq", "w") 
        while True:
            idline = handle.readline()
            seq    = handle.readline().strip()
            spacer = handle.readline()
            quals  = handle.readline()
            lenS   = len(seq)
            if not idline:
                break
            if lenS <= int(zp[1]) and lenS > int(zp[0]):
                outHandle.write("{0}{1}\n{2}{3}".format(idline, seq, spacer, quals))
        outHandle.close()
        handle.close()        

        ## zp[0]  read Length minimal
        ## zp[1]  read Length maximal
        ## geneNFus is parter gene Name

        if zp[2] == "bowtie1" and not os.path.exists("Aln_{0}_{1}_{2}_{3}_DR.bam".format(geneNFus, sn, zp[0], zp[1])):
            bowtieV = zp[3].replace("v", "")
              
            alnCmd = "%s -p 16 -l 5 --chunkmbs 512 -a -v %s %s T_%s_%s_%s.fq -S Aln_%s_%s_%s_%s_DiffReads.sam 1>>./log/%s_bowtie_%s.log 2>&1"%(softW["bowtie1"],bowtieV,  bt1Lib, sn, zp[0], zp[1], geneNFus , sn, zp[0], zp[1], sn, zp[0])
            retcode = subprocess.call(alnCmd, shell=True)
            filterSamCmd = "%s view -h -F 4 Aln_%s_%s_%s_%s_DiffReads.sam | samtools sort -@ 4 - -T /tmp/aln_%s_%s.sorted -o AE_%s_%s_%s_%s_DR.bam"%( softW["samtools"], geneNFus, sn, zp[0], zp[1], sn, zp[0], geneNFus, sn, zp[0], zp[1])
            if retcode == 0:
                subprocess.call(filterSamCmd, shell=True)

        elif zp[2] == "bowtie2" and not os.path.exists("Aln_{0}_{1}_{2}_{3}_DR.bam".format(geneNFus, sn, zp[0], zp[1])):
            alnCmd = "%s -p 8 -N 0 -L 24 --mp 7,3 -a -x %s -q T_%s_%s_%s.fq -S Aln_%s_%s_%s_%s_DiffReads.sam 1>>./log/%s_bt2_%s_N1.log 2>&1"%( softW["bowtie2"], bt2Lib, sn, zp[0], zp[1],geneNFus, sn, zp[0], zp[1], sn, zp[0])
            retcode = subprocess.call(alnCmd, shell=True)
            filterSamCmd = "%s view -h -F 4 Aln_%s_%s_%s_%s_DiffReads.sam | samtools sort -@ 4 - -T /tmp/aln_%s_%s.sorted -o AE_%s_%s_%s_%s_DR.bam"%( softW["samtools"], geneNFus, sn, zp[0], zp[1], sn, zp[0], geneNFus, sn, zp[0], zp[1])
            if retcode == 0:
                subprocess.call(filterSamCmd, shell=True)
    WildC_Name = "AE_" + geneNFus + "_*_DR.bam"

    ## WildC_Name is bam names with wild card.
    return WildC_Name

def Comm_fusgene2validate(in_bams, softwares, geneF,  S_Dir,  shellAname ):
    infiles      = glob(in_bams)
    exampleF     = infiles[0]

    splitExam    = exampleF.split("_")
    genename_Fus = splitExam[1]
    sn           = splitExam[2]

    shFile = open(shellAname, "w")
    ## merge all sorted bam
    shFile.write("echo Start merge bams at `date`\n\n")
    shFile.write("%s merge -f %s_merged_%s.bam %s\n"%( softwares["samtools"], genename_Fus, sn, in_bams))
    shFile.write("rm Aln_%s_%s_*_DiffReads.sam\n\n"%(genename_Fus, sn))

    mergedF = "%s_merged_%s.bam"%(genename_Fus, sn)
    shFile.write("%s view -h -f 16 %s > Aln_merged_%s_%s.sam\n"%( softwares["samtools"], mergedF, sn, genename_Fus) )
    shFile.write("%s %s/Bioinfo_Tool.py Aln_merged_%s_%s.sam Aln_merged_%s_%s_LE.sam > py_prog.log 2>py_prog.err\n\n"%( softwares["curr_python"], S_Dir, sn, genename_Fus, sn, genename_Fus))
    shFile.write("\n\n####extract break points of fusion for current gene####\n\n")

    shFile.write("%s %s/BreakPointsFilter.py -i Aln_merged_%s_%s_LE.sam -o %s -s %s\n"%( softwares["curr_python"], S_Dir,  sn, genename_Fus, genename_Fus, sn))
    bp_fileout = "%s_fusion_%s.txt"%(genename_Fus, sn)
    shFile.write("echo Finish Fusion analysis %s at `date`\n"%(genename_Fus))
    shFile.close()
    #shFile.write("samtools view -u alignment.sam | samtools sort -@ 4 - output_prefix")
    return bp_fileout

if __name__ == "__main__":
    
    HELP = """USAGE: python {0} -i [fastq_file]
                                -s [sample_name]
                                -c [config file] """.format(__file__)
             
    parser = argparse.ArgumentParser( description = HELP ) 
    parser.add_argument("-c", "--config", action="store", required = True, help="config file of this pipeline") 
    parser.add_argument("-i", "--input", action='store', dest='fq_f' , help="file name of input fastq")  
    parser.add_argument("-s", "--sample",  help="sample name of fastq") 
    
    args        = parser.parse_args() 
    ## SettingF is configure file of this pipeline 
    SettingF    = args.config

    if not os.path.exists(SettingF):
        sys.exit(HELP)
    else:
        boolCut, mySW , libDir, FusIndexes = load_cNew(SettingF)
    ## make analysis directory for current sample
    if not os.path.exists("Fusion_Analysis_" + args.sample):
        os.mkdir("Fusion_Analysis_" + args.sample)

    fq_In = os.path.abspath(args.fq_f)

    os.chdir("Fusion_Analysis_" + args.sample)
          
    for FusNameA in FusIndexes:
        for ParterGene in FusIndexes[FusNameA]:
            AS          = FusNameA.split("--")
            FusName     = AS[0]
            Aindex      = AS[1]
            ## FIRST Function ----------- aln_to_fusGene ----------------
            asam        = aln_to_fusGene( mySW, fq_In, args.sample, FusName, Aindex )

            ## SECOND Function ---------- splitSam ----------------------
            afastq      = splitSam(asam)

            geneLibList = ParterGene.split("--")            
            # geneLibList [0] is partner gene Name
            # geneLibList [1] is index of bowtie1 for parter gene
            # geneLibList [2] is index of bowtie2 for parter gene

            ## THIRD Function ----------- SepAln_diffReads ---------------
            bams        = SepAln_diffReads( mySW,afastq, geneLibList[0], geneLibList[1], geneLibList[2] )

            ## bp file is files containing break points of Fusin genes
            sh_filename = "Common_" + FusName + "_" + geneLibList[0] + "_bp.sh"
            partnerGenes= FusName + "_" + geneLibList[0]

            ## FOURTH Function ---------- Comm_fusgene2validate -----------
            bpfile      = Comm_fusgene2validate(bams, mySW, FusName, libDir, sh_filename )
            Prog_s  = "bash %s 1> aln_%s_%s.log 2> aln_%s_%s.err"%(sh_filename, args.sample, partnerGenes, args.sample, partnerGenes)
            if not os.path.exists(bpfile):
                subprocess.call(Prog_s, shell=True)

    ## summary all possible fusion points
    summ_All = "cat *fusion*txt > All_points.txt"
    res_command = subprocess.Popen(summ_All, shell=True, stdout = subprocess.PIPE)

