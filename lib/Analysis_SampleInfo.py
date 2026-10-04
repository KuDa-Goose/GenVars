#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
from collections import defaultdict


def Analysis_Methy(InFile, OutFile):

    IF = open(InFile, 'r')
    ScoreD = defaultdict(list)
    
    for line in IF:
        if line.startswith("样本编号"):
            continue 
        else:
            lines = line.strip().split("\t")
            SampleName = "Sample" + lines[20]
            if SampleName == OutFile:
                if lines[11] == "-":
                    report_year = "-"
                    report_month = "-"
                    report_day = "-"
                else:
                    report_year = lines[11].split("/")[0]
                    report_month = lines[11].split("/")[1]
                    report_day = lines[11].split("/")[2]
                if lines[16] == "-":
                    patient_year = "-"
                    patient_month = "-"
                    patient_day = "-"
                else:
                    patient_year = lines[16].split("/")[0]
                    patient_month = lines[16].split("/")[1]
                    patient_day = lines[16].split("/")[2]
                if lines[4] == "-":
                    collection_hospital_year = "-"
                    collection_hospital_month = "-"
                    collection_hospital_day = "-"
                else:
                    collection_hospital_year = lines[4].split("/")[0]
                    collection_hospital_month = lines[4].split("/")[1]
                    collection_hospital_day = lines[4].split("/")[2]
                if lines[5] == "-":
                    collection_company_year = "-"
                    collection_company_month = "-"
                    collection_company_day = "-"
                else:
                    collection_company_year = lines[5].split("/")[0]
                    collection_company_month = lines[5].split("/")[1]
                    collection_company_day = lines[5].split("/")[2]
                OutF = open("basic_information.txt", 'w')
                OutF.write("受检者姓名" + "\t" + lines[12] + "\t" + "PATIENT_NAME" + "\n")
                OutF.write("报告日期_年" + "\t" + report_year + "\t" + "REPORT_YEAR" + "\n")
                OutF.write("报告日期_月" + "\t" + report_month + "\t" + "REPORT_MONTH" + "\n")
                OutF.write("报告日期_日" + "\t" + report_day + "\t" + "REPORT_DATE" + "\n")
                OutF.write("检测机构" + "\t" + "上海臻迪基因科技有限公司" + "\t" + "COMPANY_NAME" + "\n")
                OutF.write("受检者性别" + "\t" + lines[13] + "\t" + "PATIENT_GENDER" + "\n")
                OutF.write("出生日期_年" + "\t" + patient_year + "\t" + "PATIENT_BIRTH_YEAR" + "\n")
                OutF.write("出生日期_月" + "\t" + patient_month + "\t" + "PATIENT_BIRTH_MONTH" + "\n")
                OutF.write("出生日期_日" + "\t" + patient_day + "\t" + "PATIENT_BIRTH_DATE" + "\n")
                OutF.write("检测编号" + "\t" + lines[21] + "\t" + "DETECTION_NUMBER" + "\n")
                OutF.write("癌种" + "\t" + lines[14] + "\t" + "CANCER_TYPE" + "\n")
                OutF.write("采样日期_年" + "\t" + collection_hospital_year + "\t" + "COLLECTION_HOSPITAL_YEAR" + "\n")
                OutF.write("采样日期_月" + "\t" + collection_hospital_month + "\t" + "COLLECTION_HOSPITAL_MONTH" + "\n")
                OutF.write("采样日期_日" + "\t" + collection_hospital_day + "\t" + "COLLECTION_HOSPITAL_DATE" + "\n")
                OutF.write("主治医师" + "\t" + lines[18] + "\t" + "PRINCIPLE_DOCTOR" + "\n")
                OutF.write("样本来源" + "\t" + lines[19] + "\t" + "SAMPLE_ORIGIN" + "\n")
                OutF.write("样本类型" + "\t" + lines[1] + "\t" + "SAMPLE_TYPE" + "\n")
                OutF.write("样本编号" + "\t" + lines[0] + "\t" + "SAMPLE_NUMBER" + "\n")
                OutF.write("亚型" + "\t" + lines[15] + "\t" + "CANCER_SUBTYPE" + "\n")
                OutF.write("收样日期_年" + "\t" + collection_company_year + "\t" + "COLLECTION_COMPANY_YEAR" + "\n")
                OutF.write("收样日期_月" + "\t" + collection_company_month + "\t" + "COLLECTION_COMPANY_MONTH" + "\n")
                OutF.write("收样日期_日" + "\t" + collection_company_day + "\t" + "COLLECTION_COMPANY_DATE" + "\n")
                OutF.write("参考基因组" + "\t" + "hg38" + "\t" + "GENOME_ASSEMBLY_VERSION" + "\n")
                OutF.write("送检日期_年" + "\t" + collection_hospital_year + "\t" + "COLLECTION_HOSPITAL_YEARA" + "\n")
                OutF.write("送检日期_月" + "\t" + collection_hospital_month + "\t" + "COLLECTION_HOSPITAL_MONTHA" + "\n")
                OutF.write("送检日期_日" + "\t" + collection_hospital_day + "\t" + "COLLECTION_HOSPITAL_DATEA" + "\n")
                OutF.write("检测日期_年" + "\t" + collection_hospital_year + "\t" + "COLLECTION_HOSPITAL_YEARB" + "\n")
                OutF.write("检测日期_月" + "\t" + collection_hospital_month + "\t" + "COLLECTION_HOSPITAL_MONTHB" + "\n")
                OutF.write("检测日期_日" + "\t" + collection_hospital_day + "\t" + "COLLECTION_HOSPITAL_DATEB" + "\n")
                OutF.write("质控" + "\t" + lines[3] + "\t" + "QUALITY_CONTROL" + "\n")
                OutF.write("检测癌种" + "\t" + lines[7] + "\t" + "DETECTION_OF_CANCER_SPECIES" + "\n")
                OutF.write("检测产品编号" + "\t" + lines[6] + "\t" + "NUMBER_OF_DETECTION_PRODUCT" + "\n")
    
    

InputFile = sys.argv[1]
OutputFile = sys.argv[2]

Analysis_Methy(InputFile, OutputFile)
