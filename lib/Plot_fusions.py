#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__      = "KuDa Goose"
__copyright__   = "Copyright 2024, A Biotech"
__credits__     = [
    "KuDa Goose"]  # remember to add yourself
__license__     = "GPL"
__version__     = "0.1-dev, 20241028"
__maintainer__  = "KuDa Goose"
__email__       = "infozse@163.com"

import sys
import shutil
import os
import argparse
import subprocess

HELP = """USAGE: python {0} -i  sf1
                            -rd res_dir
                            -gs sf2 """.format(__file__)
           
S_Dir = os.path.dirname(__file__)
  
parser = argparse.ArgumentParser( description = HELP ) 
parser.add_argument("-i", "--FusionS_file", action='store', default=S_Dir + '/extract_separate_FusionSams.py' , help="script name of depth file calculation")  
parser.add_argument("-rd", "--inputRES",    action='store', required=True , help="dir name of fusion analysis results")  
parser.add_argument("-sn", "--SampleBar",    action='store', required=True , help="sample barcode")
parser.add_argument("-gs", "--plotScript",  action='store', default=S_Dir + "/plotFusion_breakPoints.R" , help="script name of sample fusion plotting") 
    
    
args        = parser.parse_args() 
#resultDir = "/thinker/net/gene/Projects/2018_analysis/20180412-72-SABEL/Fusion-reanalysis/result-Fusion/Fusion_analysis/"
resultDir   = args.inputRES
SampleBar   = args.SampleBar
#dep_script = "/home/software/python_scripts/extract_separate_FusionSams.py"
dep_script  = args.FusionS_file
#p_script =   "/home/software/python_scripts/testFusionPlots/plotFusion_breakPoints.R"
p_script    = args.plotScript 

#sampleS = [ "009",
#         ]


def Plot_sample(d_dir, pName, barcode):
    if not os.path.isdir(d_dir):
        sys.exit("Directory does not exist. Please check it.")
    T_files = []

    #name_s = pName.split("*")

    # barcode = pName.replace(name_s[0], "").replace(name_s[1],"")
            # if fr.endswith("Depth_Result.txt"):
            
            #barcode = fr.replace(name_s[0], "").replace(name_s[1],"")
            #if barcode in sampleS:
                #f_path = os.path.join(root, fr)
                #T_files.append(f_path)
                
                #shutil.copy(f_path, fr)
    #fusionTxt = os.path.join(d_dir, "EML4_fusion_" + barcode + ".txt")
    #fusionAP  = os.path.join(d_dir, "Aln_merged_"  + barcode + "_EML4_LE.sam")
    #print(fusionTxt, fusionAP)
    #shutil.copy(fusionTxt,  "EML4_fusion_" + barcode + ".txt")
    #shutil.copy(fusionAP ,  "Aln_merged_"  + barcode + "_EML4_LE.sam")
    Fus_file = d_dir + "/EML4_fusion_" + barcode + ".txt"
    if os.stat(Fus_file).st_size != 0:
        CallCalcDepCmd = "python %s -i %s -a %s -b %s -o %s"%(dep_script, d_dir + "/EML4_fusion_" + barcode + ".txt", d_dir + "/Aln_ALK_" + barcode + ".sam", d_dir + "/Aln_merged_" + barcode + "_EML4_LE.sam" , "Sample" + barcode + ".txt")

        retcode = subprocess.call(CallCalcDepCmd, shell=True)
        if retcode == 0:
            subprocess.call("Rscript %s %s"%(p_script, "Sample" + barcode + ".txt"), shell=True)

            print(CallCalcDepCmd)
            print("Rscript %s %s"%(p_script, "Sample" + barcode + ".txt"))
    else:
        print("No fusion")

    return T_files
# 
#
# test: python extract_separate_FusionSams.py -i test_FusionFiles/EML4_fusion_080.txt -a test_FusionFiles/Aln_ALK.fa_080.sam -b test_FusionFiles/AP_EML4_080.sam -o Sample080.txt

##
## Rscript plotFusion_breakPoints.R Sample080.txt

#z = Plot_sample(resultDir, "Aln_ALK.fa_*.sam")
z = Plot_sample(resultDir, "Aln_ALK_" + SampleBar + ".sam", SampleBar)



