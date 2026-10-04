# -*- coding: UTF-8 -*-
import sys
import linecache
import io
import os
import re
from pprint import pprint
import numpy  #非内置，安装方法：pip install numpy
from docxtpl import DocxTemplate, RichText  #非内置，需要在python3下安装，安装方法：pip install docxtpl
import xlrd ##非内置，安装方法：pip install xlrd

#print(os.getcwd())  #输出当前目录
#os.getcwd()  #输出当前目录,os.chdir能识别的格式
#os.chdir('C:\\Users\\ThinkPad\\Desktop\\YM基因检测报告20190909\\20191224_template')
#os.listdir()  #列出当前目录下的文件
#

###定义需要读入的数据库文件
db_file="S001报告生成数据库_20200117v1.9.6.xlsx"
##############################################################################################################################################################################

##############################################################################################################################################################################


###读入country_name.txt文件，并把国家英文名字和中文名字作为键值对存到字典country_dict里，其中国家的英文名字为键，每个国家的英文名字对应的值为中文名字。
country_dict = { }
#country = io.open('country_name.txt', mode="r", encoding="gbk")#encoding有时候为gbk,有时候为utf-8需注意
country = io.open('country_name.txt', mode="r", encoding="utf-8")
for each_country in country:
    country_name = each_country.rstrip().split('\t')
    #print(country_name)
    country_dict[country_name[0]]  =  country_name[1]
    
country.close()
##############################################################################################################################################################################


##########################################读入basic_information.txt文件(用于生成“一、基本信息”的表格），并存入一个字典basic_information_dict中，字典的键为basic_information.txt每一行的第三列，字典的值为basic_information.txt每一行的第二列

basic_information_dict = { }
basic_information = io.open('basic_information.txt', mode="r", encoding="utf-8")

for line in basic_information:
    ss = line.rstrip().split('\t')
    #print(ss)
    basic_information_dict[ss[2]]  =  ss[1]
    
basic_information.close()
context = basic_information_dict
#print(basic_information_dict['PATIENT_NAME'])
#print(basic_information_dict['SAMPLE_NUMBER'])
##############################################################################################################################################################################


###通过命令行输入的参数读入模板文件名字存到变量sys.argv[1]
#tmplt_file = sys.argv[1]

#通过检测产品编号来决定读入的模板文件名字
#如果是肺癌有msi的产品
if basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81001-111" or basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81001-211":
    tmplt_file="template_NSCLC_with_msi_v0.5.docx"
#如果是肺癌没有msi的产品
elif basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81001-101" or basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81001-201":
    tmplt_file="template_NSCLC_without_msi_v0.5.docx"
#如果是结直肠癌没有msi的产品    
elif basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81002-101" or basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81002-201" :
    tmplt_file="template_CRC_without_msi_v0.5.docx"
#如果是结直肠癌有msi的产品
elif basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81002-111" or basic_information_dict['NUMBER_OF_DETECTION_PRODUCT'] == "APG-81002-211":
    tmplt_file="template_CRC_with_msi_v0.5.docx"
else:
    print("The template file does not exit")
#print(tmplt_file)
##############################################################################################################################################################################

###读入基因检测模板
doc = DocxTemplate(tmplt_file)


##############################################################################################################################################################################

###根据样本信息里basic_information.txt文件里的第三列为SAMPLE_NUMBER那一行的第二列值来定义生成报告所需的输入文件名的前缀

prefix="C_"+basic_information_dict['SAMPLE_NUMBER']
uniq_snp_chemo_file=prefix+"_uniq_snp_chemo.txt"
#print(uniq_snp_chemo_file)
snp_chemo_file=prefix+"_snp_chemo.txt"
#print(snp_chemo_file)
mutation_uniq_gene_list_file=prefix+"_mutation_uniq_gene_list.txt"
#print(mutation_uniq_gene_list_file)
mutation_del3_file=prefix+"_mutation_del3.txt"
#print(mutation_del3_file)
msi_result_file=prefix+"_msi_result.txt"
#print(msi_result_file)


##############################################################################################################################################################################

##########################################生成“二、基因靶向突变表格”,和“三、相关靶向药物”列表的字典，通过test_GetMutation函数读入mutation_del3_file（例如：C_0101200320001_mutation_del3.txt）和db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现

#Gene_Mutation_Table_Dict = {
#    'Gene_Mutation_Table' : [
#        {'Gene_Mutation_Name' : 'EGFR T790M错义突变', 'Gene_CDS_AA' : [{'c2369;pT790M':'30%'},{'c2369;p19del':'20%'},], },
#        {'Gene_Mutation_Name' : 'EGFR L858R错义突变', 'Gene_CDS_AA' : [{'c2369;pL858R':'30%'},], },
#         ],
#}

def test_GetMutation(filein,db_name):
    #line_N = int(linecache.getline(filein, 1,encoding="gb2312").rstrip().replace('##', ''))
    #定义一个字典d1,键名为Gene_Mutation_Table，值为一个空列表[],这个字典的键名Gene_Mutation_Table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：{%tr for a in Gene_Mutation_Table %}里的Gene_Mutation_Table即为此处定义而来。
    
    d1 = { 'Gene_Mutation_Table' : [] }
    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #f1用于接收打开filein=mutation_del3_file，例如：C_0101200320001_mutation_del3.txt
    f1 = open(filein, "r", encoding ='utf-8')
    line_N = int(f1.readline().rstrip().replace('##', ''))#将这个样本检测出靶向突变的个数存在line_N里
    #print(line_N)
    mutations_n = 0#用于计数已经处理了多少个靶向突变
    
    #用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table = data.sheet_by_index(3)#数据库文件的第4个工作表Drugs(NSCLC)的内容存到table里
    nrows = table.nrows#数据库文件的第4个工作表的行数存到nrows里
    NSCLC_refid_list=[]
    NSCLC_refid=''
    for f in range(1,nrows):
        NSCLC_refid=table.row(f)[0].value
        NSCLC_refid_list.append(NSCLC_refid)
    #print(k[5] in NSCLC_refid_list)
    #print(type(table.row(16)[7].value))   
    
    
    

    table_CRC = data.sheet_by_index(9)#数据库文件的第10个工作表Drugs(CRC)的内容存到table_CRC里
    nrows_CRC = table_CRC.nrows#数据库文件的第10个工作表的行数存到nrows_CRC里
    CRC_refid_list=[]
    CRC_refid=''
    for f in range(1,nrows_CRC):
        CRC_refid=table_CRC.row(f)[0].value
        CRC_refid_list.append(CRC_refid)
        #print(f)
    #print(len(CRC_refid_list))
    #print('pik3ca_onc' in CRC_refid_list)
    
    #定义后面会用到的列表名字，表格里最后一行和非最后一行的突变分别处理
    drug_list = []
    evidence_list = [] 
    drug_list_bottom = []
    evidence_list_bottom = []

    #从第二行开始循环遍历靶向突变结果（例如：C_0101200320001_mutation_del3.txt）里的每一行结果，每一行结果代表一条突变信息
    for line in f1:
        #当检出靶向突变个数为零的情况，RefID=no_mutation, 因为只有一行，所以处理方法类似最后一行突变 mutations_n == line_N-1的处理方法
        if line_N == 0:
            #定义一个空字典add_d_new
            add_d_new = {}
            #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
            k= line.rstrip().split("\t")
          
            #第三列k[2]里的CDS和第四列k[3]里AA可能有多条信息用“,”分隔开，第三列k[2]里的CDS的第n个逗号和第四列k[3]里的AA的第n个逗号分隔的内容是一一对应的，通过zip将各CDS与AA连起来，并转化为列表
            good=zip(k[2].split(','), k[3].split(','))
            good1=list(good)
            #定义空的字符变量
            good2=" "
            drug = ''
            evidence_level = ''
            #向字典里添加键为"Gene_Mutation_AF"，值为突变频率RichText(k[4].replace(",","\n"))的键值对,如果k[4]里有逗号，则用回车"\n"替换
            add_d_new["Gene_Mutation_AF"] = RichText(k[4].replace(",","\n"))
            #如果为肺癌的情况，遍历数据库第四个工作表Drugs(NSCLC)的所有行
            
            if k[6]=="lung":
                for i in range(1,nrows):
                    RefID = table.row(i)[0].value
                    if RefID == k[5]:
                        drug_bottom = table.row(i)[5].value
                        if table.row(i)[7].ctype == 2:
                            evidence_level_bottom = str(int(table.row(i)[7].value))
                        else:
                            evidence_level_bottom = str(table.row(i)[7].value)

                        drug_list_bottom.append(drug_bottom)
                        evidence_list_bottom.append(evidence_level_bottom)
            #如果为结直肠癌CRC需要遍历另外一个工作表Drugs(CRC)          
            elif k[6]=="CRC":
                for i in range(1,nrows_CRC):
                    RefID = table_CRC.row(i)[0].value
                    if RefID == k[5]:
                        drug_bottom = table_CRC.row(i)[5].value
                        if table_CRC.row(i)[7].ctype == 2:
                            evidence_level_bottom = str(int(table_CRC.row(i)[7].value))
                        else:
                            evidence_level_bottom = str(table_CRC.row(i)[7].value)
                        #evidence_level_bottom = str(table_CRC.row(i)[7].value)
                        #if "R" in evidence_level_bottom:
                        #    evidence_level_bottom=RichText(evidence_level_bottom,color='ff0000')
                        #else:
                        #    evidence_level_bottom=RichText(evidence_level_bottom)
                        drug_list_bottom.append(drug_bottom)
                        evidence_list_bottom.append(evidence_level_bottom)
                
                
            #最后一行突变的结果，如果evidence_list_bottom和drug_list_bottom里有多条结果则以回车分隔，用于生成“三、相关靶向药物”最后一行突变的结果
            #将evidence_drug及drug_list里的各个元素合并并用回车分隔开存到一个新的变量new_evidence_list及new_drug_list里，此时new_evidence_list及new_drug_list已经不是列表，而是字符，这样在输出的表格里是作为一个字符输出在一个格子里，行与行之间有回车，但没有边框线
            #new_evidence_list_bottom="\n".join(evidence_list_bottom)
            new_evidence_list_bottom=RichText()
            num=len(evidence_list_bottom)
            for q in range(num-1):
                if "R" in evidence_list_bottom[q]:
                    new_evidence_list_bottom.add(evidence_list_bottom[q]+'\n',color='ff0000')
                else:
                    new_evidence_list_bottom.add(evidence_list_bottom[q]+'\n')

            if "R" in evidence_list_bottom[len(evidence_list_bottom)-1]:
                new_evidence_list_bottom.add(evidence_list_bottom[num-1],color='ff0000')
            else:
                new_evidence_list_bottom.add(evidence_list_bottom[num-1])            
            
            
            new_drug_list_bottom="\n".join(drug_list_bottom)
            
            #最后一行突变的结果存到字典d_bottom里
            d_bottom = {'Mutation_Gene_Name_Bottom':RichText(k[0]+' ',italic=True),'Gene_Mutation_Name_Bottom':RichText(k[1],italic=False),'Gene_Mutation_CDS_AA_Bottom': good2,'Zero_Gene_Mutation_AF_Bottom':RichText(k[4].replace(",","\n")),'Target_Drugs_Bottom':RichText(new_drug_list_bottom),'Evidence_level_Bottom':new_evidence_list_bottom}
         
        #当检出靶向突变个数大于0的时候，除了最后一行的所有行进行处理
        elif mutations_n < line_N-1:
            #定义一个空字典add_d_new
            add_d_new = {}
            #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
            k= line.rstrip().split("\t")
            #print(k[5])
            #if (k[5]  not in CRC_refid_list):
            #    print("yes")
            #向字典里添加键为"Mutation_Gene_Name"，值为基因名字RichText(k[0]+' ',italic=True)的键值对
            add_d_new["Mutation_Gene_Name"] = RichText(k[0]+' ',italic=True)
            #向字典里添加键为"Gene_Mutation_Name"，值为突变类型RichText(k[1],italic=False)的键值对
            add_d_new["Gene_Mutation_Name"] = RichText(k[1],italic=False)
            #第三列k[2]里的CDS和第四列k[3]里AA可能有多条信息用“,”分隔开，第三列k[2]里的CDS的第n个逗号和第四列k[3]里的AA的第n个逗号分隔的内容是一一对应的，通过zip将各CDS与AA连起来，并转化为列表
            good=zip(k[2].split(','), k[3].split(','))
            good1=list(good)
            #向字典里添加键为"Gene_Mutation_CDS_AA"，值为将各个对应的CDS和AA合并并用；连接后以回车分开"\n".join([";".join(list(i)) for i in good1])的键值对
            add_d_new["Gene_Mutation_CDS_AA"]="\n".join(["; ".join(list(i)) for i in good1])
            #定义空的字符变量
            drug = ''
            evidence_level = ''
            RefID=''
            #定义空的列表
            drug_list = []
            evidence_list = []
            new_evidence_list = []
            new_drug_list = []
            #k[2].split(',')[0]+k[3].split(',')[0]+'\n'+k[2].split(',')[1]+k[3].split(',')[1]
            #向字典里添加键为"Gene_Mutation_AF"，值为突变频率RichText(k[4].replace(",","\n"))的键值对,如果k[4]里有逗号，则用回车"\n"替换
            add_d_new["Gene_Mutation_AF"] = RichText(k[4].replace(",","\n"))
            
            
            #如果为肺癌的情况，遍历数据库第四个工作表Drugs(NSCLC)的所有行
            
            if k[6]=="lung" and (k[5] in NSCLC_refid_list):
                for i in range(1,nrows):
                    RefID = table.row(i)[0].value

                    if RefID == k[5]:
                        drug = table.row(i)[5].value
                        if table.row(i)[7].ctype == 2:
                            evidence_level = str(int(table.row(i)[7].value))
                        else:
                            evidence_level = str(table.row(i)[7].value)
                        #evidence_level = str(table.row(i)[7].value)
                        #if "R" in evidence_level:
                        #    evidence_level=RichText(evidence_level,color='ff0000')
                        #else:
                        #    evidence_level=RichText(evidence_level)
                        drug_list.append(drug)
                        evidence_list.append(evidence_level)
                        
            elif k[6]=="lung" and (k[5] not in NSCLC_refid_list):
                drug="无相关推荐用药"
                drug_list.append(drug)
                evidence_level = '/'
                evidence_list.append(evidence_level)
            #如果为结直肠癌CRC需要遍历另外一个工作表Drugs(CRC)          
            elif k[6]=="CRC" and (k[5] in CRC_refid_list):
                for i in range(1,nrows_CRC):
                    RefID = table_CRC.row(i)[0].value

                    if RefID == k[5]:
                        drug = table_CRC.row(i)[5].value
                        if table_CRC.row(i)[7].ctype == 2:
                            evidence_level = str(int(table_CRC.row(i)[7].value))
                        else:
                            evidence_level = str(table_CRC.row(i)[7].value)
                        #evidence_level = str(table_CRC.row(i)[7].value)
                        #if "R" in evidence_level:
                        #    evidence_level=RichText(evidence_level,color='ff0000')
                        #else:
                        #    evidence_level=RichText(evidence_level)
                        drug_list.append(drug)
                        evidence_list.append(evidence_level)
            elif k[6]=="CRC" and (k[5] not in CRC_refid_list):
                #print(k[5])
                drug="无相关推荐用药"
                drug_list.append(drug)
                evidence_level = '/'
                evidence_list.append(evidence_level)
                            
            
            #将evidence_drug及drug_list里的各个元素合并并用回车分隔开存到一个新的变量new_evidence_list及new_drug_list里，此时new_evidence_list及new_drug_list已经不是列表，而是字符，这样在输出的表格里是作为一个字符输出在一个格子里，行与行之间有回车，但没有边框线
            #new_evidence_list="\n".join(evidence_list)
            new_evidence_list=RichText()
            num=len(evidence_list)
            for q in range(num-1):
                if "R" in evidence_list[q]:
                    new_evidence_list.add(evidence_list[q]+'\n',color='ff0000')
                else:
                    new_evidence_list.add(evidence_list[q]+'\n')

            if "R" in evidence_list[len(evidence_list)-1]:
                new_evidence_list.add(evidence_list[num-1],color='ff0000')
            else:
                new_evidence_list.add(evidence_list[num-1])            
            
            
            
            
            
            
            
            
            new_drug_list="\n".join(drug_list)
            #print(type(new_drug_list))
            #向字典里添加键为"Detected_Gene_Mutation_Name"，值为RefID:RichText(RefID)的键值对
            add_d_new["Detected_Gene_Mutation_Name"] = RichText(RefID)
            #向字典里添加键为"Detected_Gene_Mutation_Target_Drugs"，值为用药列表RichText(new_drug_list)的键值对
            add_d_new["Detected_Gene_Mutation_Target_Drugs"] = RichText(new_drug_list)
            #向字典里添加键为"Evidence_level"，值为依据等级：RichText(new_evidence_list)的键值对
            add_d_new["Evidence_level"] = new_evidence_list
            #add_d_new["test"] = drug_list
            #将前面生成的字典add_d_new加到字典d1的键为'Gene_Mutation_Table'原来值为空列表[]的列表里
            d1['Gene_Mutation_Table'].append(add_d_new)
            
        #当检出靶向突变个数大于0的时候，对最后一行进行处理    
        elif mutations_n == line_N-1:
            #定义一个空字典add_d_new
            add_d_new = {}
            #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
            k= line.rstrip().split("\t")
            #第三列k[2]里的CDS和第四列k[3]里AA可能有多条信息用“,”分隔开，第三列k[2]里的CDS的第n个逗号和第四列k[3]里的AA的第n个逗号分隔的内容是一一对应的，通过zip将各CDS与AA连起来，并转化为列表存到good1里
            good=zip(k[2].split(','), k[3].split(','))
            good1=list(good)
            #将good1各个对应的CDS和AA合并，并用"； "连接后以回车分开存到列表good2里
            good2="\n".join(["; ".join(list(i)) for i in good1])
            #定义空的字符变量
            drug = ''
            evidence_level = ''
            #k[2].split(',')[0]+k[3].split(',')[0]+'\n'+k[2].split(',')[1]+k[3].split(',')[1]
            #向字典里添加键为"Gene_Mutation_AF"，值为突变频率RichText(k[4].replace(",","\n"))的键值对,如果k[4]里有逗号，则用回车"\n"替换
            add_d_new["Gene_Mutation_AF"] = RichText(k[4].replace(",","\n"))
            
            
            
            
            #如果为肺癌的情况，遍历数据库第四个工作表Drugs(NSCLC)的所有行
            
            if k[6]=="lung" and (k[5] in NSCLC_refid_list):
                for i in range(1,nrows):
                    RefID = table.row(i)[0].value
                    #数据库第四个工作表Drugs(NSCLC)第一列的refid(存在RefID = table.row(i)[0].value)如果和mutation_del3.txt文件里第6列的refid（k[5]）值一样
                      
                    
                    if RefID == k[5]:
                        drug_bottom = table.row(i)[5].value
                        if table.row(i)[7].ctype == 2:
                            evidence_level_bottom = str(int(table.row(i)[7].value))
                        else:
                            evidence_level_bottom = str(table.row(i)[7].value)
                        #evidence_level_bottom = str(table.row(i)[7].value)
                        #if "R" in evidence_level_bottom:
                        #    evidence_level_bottom=RichText(evidence_level_bottom,color='ff0000')
                        #else:
                        #    evidence_level_bottom=RichText(evidence_level_bottom)
                        drug_list_bottom.append(drug_bottom)
                        evidence_list_bottom.append(evidence_level_bottom)
                        
            elif k[6]=="lung" and (k[5] not in NSCLC_refid_list):

                drug_bottom="无相关推荐用药"
                drug_list_bottom.append(drug_bottom)
                evidence_level_bottom = '/'
                evidence_list_bottom.append(evidence_level_bottom)
                
            #如果为结直肠癌CRC需要遍历另外一个工作表Drugs(CRC)          
            elif k[6]=="CRC" and (k[5] in CRC_refid_list):
                for i in range(1,nrows_CRC):
                    RefID = table_CRC.row(i)[0].value
                    

                    if RefID == k[5]:
                        drug_bottom = table_CRC.row(i)[5].value
                        if table_CRC.row(i)[7].ctype == 2:
                            evidence_level_bottom = str(int(table_CRC.row(i)[7].value))
                        else:
                            evidence_level_bottom = str(table_CRC.row(i)[7].value)
                        #evidence_level_bottom = str(table_CRC.row(i)[7].value)
                        #if "R" in evidence_level_bottom:
                        #    evidence_level_bottom=RichText(evidence_level_bottom,color='ff0000')
                        #else:
                        #    evidence_level_bottom=RichText(evidence_level_bottom)
                        drug_list_bottom.append(drug_bottom)
                        evidence_list_bottom.append(evidence_level_bottom)
            elif k[6]=="CRC" and (k[5] not in CRC_refid_list):
                drug_bottom="无相关推荐用药"
                drug_list_bottom.append(drug_bottom)
                evidence_level_bottom = '/'
                evidence_list_bottom.append(evidence_level_bottom)
                
            
            
            #print(evidence_list_bottom)
            #new_evidence_list_bottom="\n".join(evidence_list_bottom)
            
            new_evidence_list_bottom=RichText()
            num=len(evidence_list_bottom)
            for q in range(num-1):
                if "R" in evidence_list_bottom[q]:
                    new_evidence_list_bottom.add(evidence_list_bottom[q]+'\n',color='ff0000')
                else:
                    new_evidence_list_bottom.add(evidence_list_bottom[q]+'\n')

            if "R" in evidence_list_bottom[len(evidence_list_bottom)-1]:
                new_evidence_list_bottom.add(evidence_list_bottom[num-1],color='ff0000')
            else:
                new_evidence_list_bottom.add(evidence_list_bottom[num-1])            
            
            
            
            
            
            new_drug_list_bottom="\n".join(drug_list_bottom)
            
            #最后一行突变的结果存到字典d_bottom里
            d_bottom = {'Mutation_Gene_Name_Bottom':RichText(k[0]+' ',italic=True),'Gene_Mutation_Name_Bottom':RichText(k[1],italic=False),'Gene_Mutation_CDS_AA_Bottom':good2,'Gene_Mutation_AF_Bottom':RichText(k[4].replace(",","\n")),'Target_Drugs_Bottom':RichText(new_drug_list_bottom),'Evidence_level_Bottom':new_evidence_list_bottom}
        ##已经处理的靶向突变计数+1    
        mutations_n +=1

    f1.close()
    return d1,d_bottom #除了最后一行的所有行处理的结果存到字典d1里，最后一行的结果存到字典d_bottom里

#调用函数test_GetMutation，返回值Gene_Mutation_Table_Dict=d1,Gene_Mutation_Table_Dict_bottom=d_bottom
Gene_Mutation_Table_Dict,Gene_Mutation_Table_Dict_bottom = test_GetMutation(mutation_del3_file,db_file)

#print(Gene_Mutation_Table_Dict)
#更新字典context内容,添加Gene_Mutation_Table_Dict,Gene_Mutation_Table_Dict_bottom两个字典到context字典里
context.update(Gene_Mutation_Table_Dict) 
context.update(Gene_Mutation_Table_Dict_bottom) 
############################################################################################################################################################################## 

#########################################生成二、基因多态性表格的字典，通过test_snp函数读入snp_chemo_file（例如：C_0101200320001_snp_chemo.txt）和db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现
#Gene_SNP_Table_Dict = {
#    'Gene_SNP_Table' : [
#        {'Gene_SNP_Name' : 'TYMS 3’UTR c.1494', 'Gene_SNP_Type' : '+6/-6杂合子', },
#        {'Gene_SNP_Name' : 'TYMS 5’UTR VNTR', 'Gene_SNP_Type' : '2R/3R杂合子', },
#         ],
#    }
 

def test_snp(filein):
    #定义一个字典d1,键名为Gene_SNP_Table，值为一个空列表[],这个字典的键名Gene_SNP_Table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：{%tr for a in Gene_SNP_Table %}里的Gene_SNP_Table即为此处定义而来。
    
    d1 = { 'Gene_SNP_Table' : [] }
    #f1用于接收打开filein=snp_chemo_file，例如：C_0101200320001_snp_chemo.txt
    f1 = open(filein, "r", encoding ='utf-8')
    #将这个样本检测出SNP的个数存在line_N里
    line_N = int(f1.readline().rstrip().replace('##', ''))
    #用于计数已经处理了多少个SNP突变
    mutations_n = 0
    #循环SNP结果（例如：C_0101200320001_snp_chemo.txt）里的每一行结果，每一行结果代表一条SNP信息
    for line in f1:
        #当检出SNP个数大于0的时候，除了最后一行的所有行进行处理,注：SNP不可能存在检不出来的情况，即SNP个数永远大于0
        if mutations_n < line_N-1:
            #定义一个空字典add_d_new
            add_d_new = {}
            #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
            k= line.rstrip().split("\t")
            #print(k)
            k_j = k[0].split('__')
            add_d_new["Gene_Name"]=RichText(k_j[0]+' ',italic=True) 
            add_d_new["SNP_AA_change"]=RichText(k_j[1]) 
            #向字典里添加键为"Gene_SNP_Name"，值为基因名字：k[0]的键值对
            add_d_new["Gene_SNP_Name"] = k[0]
            #向字典里添加键为"Gene_SNP_Type"，值为SNP类型：k[1]的键值对
            add_d_new["Gene_SNP_Type"] = k[1]
            #将前面生成的字典add_d_new加到字典d1的键为'Gene_SNP_Table'原来值为空列表[]的列表里
            d1['Gene_SNP_Table'].append(add_d_new)
        #当检出靶向突变个数大于0的时候，对最后一行进行处理    
        else:
            #定义一个空字典add_d_new
            add_d_new = {}
            #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
            k= line.rstrip().split("\t")
            k_j = k[0].split('__')
            #add_d_new["Gene_Name"]=RichText(k_j[0]+' ',italic=True) 
            #add_d_new["SNP_AA_change"]=RichText(k_j[1]) 
            #生成d_bottom这个字典：键分别为'Gene_SNP_Name_Bottom'，'Gene_SNP_Type_Bottom'，值分别为基因名字k[0],SNP类型k[1]的键值对
            d_bottom = {'Gene_SNP_Name_Bottom':RichText(k_j[0]+' ',italic=True),'Gene_SNP_AA_change_Bottom':RichText(k_j[1]),'Gene_SNP_Type_Bottom':k[1]}
        ##已经处理的靶向突变计数+1        
        mutations_n +=1

    f1.close()
    return d1,d_bottom#除了最后一行的所有行处理的结果存到字典d1里，最后一行的结果存到字典d_bottom里

#调用函数test_snp，返回值Gene_SNP_Table_Dict=d1,Gene_SNP_Table_Dict_Bottom=d_bottom
Gene_SNP_Table_Dict,Gene_SNP_Table_Dict_Bottom = test_snp(snp_chemo_file)


#更新字典context内容,添加Gene_SNP_Table_Dict,Gene_SNP_Table_Dict_Bottom两个字典到context字典里
context.update(Gene_SNP_Table_Dict) 
context.update(Gene_SNP_Table_Dict_Bottom) 

##############################################################################################################################################################################


#########################################生成三、基因多态性相关化疗药物列表：通过test_chemo函数读入snp_chemo_file（例如：C_0101200320001_snp_chemo.txt）和db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现

def test_chemo(filein,db_name):
    #定义一个字典d1,键名为Gene_SNP_Drug_Table，值为一个空列表[],这个字典的键名Gene_SNP_Drug_Table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：{%tr for a in Gene_SNP_Drug_Table %}里的Gene_SNP_Drug_Table即为此处定义而来。
    
    d1 = { 'Gene_SNP_Drug_Table' : [] }
    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #f1用于接收打开filein=snp_chemo_file，例如：C_0101200320001_snp_chemo.txt
    f1 = open(filein, "r", encoding ='utf-8')
    #将这个样本检测出SNP的个数存在line_N里
    line_N = int(f1.readline().rstrip().replace('##', ''))
    
    
    #用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table = data.sheet_by_index(3)#数据库文件的第4个工作表Drugs(NSCLC)的内容存到table里
    nrows = table.nrows#数据库文件的第4个工作表的行数存到nrows里

    table_CRC = data.sheet_by_index(9)#数据库文件的第10个工作表Drugs(CRC)的内容存到table_CRC里
    nrows_CRC = table_CRC.nrows#数据库文件的第4个工作表的行数存到nrows_CRC里
    
    

    for line in f1:
        drug_list = []
        evidence_list = [] 
        drug_evidence_list=[]
        #定义一个空字典add_d_new
        add_d_new = {}
        k= line.rstrip().split("\t")
        k_j = k[0].split('__')
        add_d_new["Gene_Name"]=RichText(k_j[0]+' ',italic=True) 
        add_d_new["SNP_AA_change"]=RichText(k_j[1]) 
        #print(k)
        add_d_new["Gene_SNP_Name"] = k[0]
        add_d_new["Gene_SNP_Type"] = k[1]
        genotype_list=[]
        
        #如果basic_information.txt文件里的第三列为DETECTION_OF_CANCER_SPECIES那一行的第二列值为“肺癌”
            
        if basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="肺癌":
            #遍历数据库第四个工作表Drugs(NSCLC)的除第一行外的所有行
            for i in range(1,nrows):
                #读取数据库第四个工作表Drugs(NSCLC)里每行的SNP的RefID那一列值，例如：ercc2_d312n，存到变量RefID里
                RefID = table.row(i)[0].value
                #读取数据库第四个工作表Drugs(NSCLC)里每行的SNP的表型那一列值，例如：G/A杂合子，ercc2_d312n，存到变量genotype里
                genotype=table.row(i)[3].value
                #每循环一行基因SNP检测结果，将结果里每一行里RefID在数据库里存在的所有表型存到genotype_list里，每开始循环一个新行，先将上一行的genotype_list清空再存
                if RefID == k[2]:
                    genotype_list.append(genotype)
            #print(genotype_list)
            
            
            #遍历数据库第四个工作表Drugs(NSCLC)的除第一行外的所有行
            for i in range(1,nrows):
                #读取数据库第四个工作表Drugs(NSCLC)里每行的SNP的RefID那一列值，例如：ercc2_d312n，存到变量RefID里
                RefID = table.row(i)[0].value
                        
            
                #判断如果数据库第四个工作表Drugs(NSCLC)里的RefID和基因检测SNP结果里第三列的RefID值一样，并且基因检测SNP结果第二列的表型存在于数据库里找出的genotype_list里，并且基因检测SNP结果第二列的表型等于数据库第四个工作表Drugs(NSCLC)第四列的表型时，才进行如下处理：将用药和依据分别存到列表drug，evidence里然后存到drug_list，evidence_list，并将两者合并用"___##___"连接存到drug_evidence_list，原因是有可能有drug+evidence_level重复的情况，这样做为了以后去重
                
                if RefID == k[2] and k[1] in genotype_list and k[1]==table.row(i)[3].value:
                    #print("yes")
                    drug = table.row(i)[5].value
                    if table.row(i)[4].ctype == 2:
                        evidence_level = str(int(table.row(i)[4].value))
                    else:
                        evidence_level = str(table.row(i)[4].value)
                    #evidence_level = str(table.row(i)[4].value)
                    drug_list.append(drug)
                    evidence_list.append(evidence_level)
                    drug_evidence_list.append(drug+"___##___"+evidence_level)
                #判断如果数据库第四个工作表Drugs(NSCLC)里的RefID和基因检测SNP结果里第三列的RefID值一样，并且基因检测SNP结果第二列的表型不存在于数据库里找出的genotype_list里，进行如下处理：将数据库第四个工作表Drugs(NSCLC)里最后一行用药和依据分别存到列表drug，evidence里然后存到drug_list，evidence_list，并将两者合并用"___##___"连接存到drug_evidence_list，原因是有可能有drug+evidence_level重复的情况，这样做为了以后去重
                elif RefID == k[2] and k[1] not in genotype_list:
                    RefID="no_snp"
                    drug = table.row(-1)[5].value
                    evidence_level = str(table.row(-1)[4].value)
                    drug_list.append(drug)
                    evidence_list.append(evidence_level)
                    drug_evidence_list.append(drug+"___##___"+evidence_level)
       
        #如果为结直肠癌CRC需要遍历另外一个工作表Drugs(CRC)          
        elif basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="结直肠癌":        
            #遍历数据库第11个工作表Drugs(CRC)的除第一行外的所有行
            for i in range(1,nrows_CRC):
                #读取数据库第11个工作表Drugs(CRC)里每行的SNP的RefID那一列值，例如：ercc2_d312n，存到变量RefID里
                RefID = table_CRC.row(i)[0].value
                #读取数据库第11个工作表Drugs(CRC)里每行的SNP的表型那一列值，例如：G/A杂合子，ercc2_d312n，存到变量genotype里
                genotype=table_CRC.row(i)[3].value
                #每循环一行基因SNP检测结果，将结果里每一行里RefID在数据库里存在的所有表型存到genotype_list里，每开始循环一个新行，先将上一行的genotype_list清空再存
                if RefID == k[2]:
                    genotype_list.append(genotype)
            #print(genotype_list)
            
            
            #遍历数据库第11个工作表Drugs(CRC)的除第一行外的所有行
            for i in range(1,nrows_CRC):
                #读取数据库第11个工作表Drugs(CRC)里每行的SNP的RefID那一列值，例如：ercc2_d312n，存到变量RefID里
                RefID = table_CRC.row(i)[0].value
                        
            
                #判断如果数据库第11个工作表Drugs(CRC)里的RefID和基因检测SNP结果里第三列的RefID值一样，并且基因检测SNP结果第二列的表型存在于数据库里找出的genotype_list里，并且基因检测SNP结果第二列的表型等于数据库第11个工作表Drugs(CRC)第四列的表型时，才进行如下处理：将用药和依据分别存到列表drug，evidence里然后存到drug_list，evidence_list，并将两者合并用"___##___"连接存到drug_evidence_list，原因是有可能有drug+evidence_level重复的情况，这样做为了以后去重
                
                if RefID == k[2] and k[1] in genotype_list and k[1]==table_CRC.row(i)[3].value:
                    #print("yes")
                    drug = table_CRC.row(i)[5].value
                    evidence_level = str(table_CRC.row(i)[4].value)
                    drug_list.append(drug)
                    evidence_list.append(evidence_level)
                    drug_evidence_list.append(drug+"___##___"+evidence_level)
                #判断如果数据库第11个工作表Drugs(CRC)里的RefID和基因检测SNP结果里第三列的RefID值一样，并且基因检测SNP结果第二列的表型不存在于数据库里找出的genotype_list里，进行如下处理：将数据库第11个工作表Drugs(CRC)里最后一行用药和依据分别存到列表drug，evidence里然后存到drug_list，evidence_list，并将两者合并用"___##___"连接存到drug_evidence_list，原因是有可能有drug+evidence_level重复的情况，这样做为了以后去重
                elif RefID == k[2] and k[1] not in genotype_list:
                    RefID="no_snp"
                    drug = table_CRC.row(-1)[5].value
                    evidence_level = str(table_CRC.row(-1)[4].value)
                    drug_list.append(drug)
                    evidence_list.append(evidence_level)
                    drug_evidence_list.append(drug+"___##___"+evidence_level)
               
        
        
        
        
        #将前面生成的drug_evidence_list通过list(set(drug_evidence_list))去重，去重后重新生成drug_list，evidence_list
        drug_list = []
        evidence_list = []         
        for h in list(set(drug_evidence_list)):
            drug_list.append(h.split("___##___")[0])
            evidence_list.append(h.split("___##___")[1])
        #print(evidence_list)
        #向字典里添加键为"Detected_Gene_Mutation_Target_Drugs"，值为drug_list的键值对
        add_d_new["Detected_Gene_Mutation_Target_Drugs"] = drug_list
        #向字典里添加键为"Evidence_level"，值为evidence_list的键值对
        add_d_new["Evidence_level"] = evidence_list
        #向字典里添加键为"n_row_each_snp"，值为len(drug_list)即每种SNP表型对应的用药个数的键值对
        add_d_new["n_row_each_snp"] = len(drug_list)
        #将前面生成的字典add_d_new加到字典d1的键为'Gene_SNP_Drug_Table'原来值为空列表[]的列表里
        d1['Gene_SNP_Drug_Table'].append(add_d_new)    
        
       
    f1.close()
    return d1#返回字典d1的值
#调用函数test_chemo，返回值Gene_SNP_Drug_Table_Dict=d1
Gene_SNP_Drug_Table_Dict = test_chemo(snp_chemo_file,db_file)

#print(Gene_SNP_Drug_Table_Dict)
#更新字典context内容,添加Gene_SNP_Drug_Table_Dict字典到context字典里
context.update(Gene_SNP_Drug_Table_Dict) 
 

##############################################################################################################################################################################

##############################################################################微卫星分析，用于生成“二、检测结果总览的 msi表”以及“三、相关用药列表的 相关免疫药物列表”
#通过test_msi函数读入msi_result_file（例如：C_0101200320001_msi_result.txt）和db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现

def test_msi(filein,db_name):
    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #定义一个字典d1,键名为msi_Drug_Table，值为一个空列表[],这个字典的键名msi_Drug_Table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：“三、相关用药列表的 相关免疫药物列表”{%tr for a in msi_Drug_Table %}里的msi_Drug_Table即为此处定义而来。
    d1 = { 'msi_Drug_Table' : [] }
    #f1用于接收打开filein=msi_result_file，例如：C_0101200320001_msi_result.txt
    f1 = open(filein, "r", encoding ='utf-8')
    
    
    #用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table = data.sheet_by_index(3)#数据库文件的第4个工作表Drugs(NSCLC)的内容存到table里
    nrows = table.nrows#数据库文件的第4个工作表的行数存到nrows里

    table_CRC = data.sheet_by_index(9)#数据库文件的第10个工作表Drugs(CRC)的内容存到table_CRC里
    nrows_CRC = table_CRC.nrows#数据库文件的第10个工作表的行数存到nrows_CRC里


    #定义一个字典d2
    d2={}
    #遍历msi_result_file，例如：C_0101200320001_msi_result.txt中的每一行，实际上只有一行结果
    for line in f1:
        drug_list = []
        evidence_list = [] 
        #定义一个空字典add_d_new
        add_d_new = {}
        #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
        k= line.rstrip().split("\t")
        
        add_d_new["msi"] = k[0]
        #add_d2_new = k[0]
        
        #判断检测癌种是否为肺癌
        if basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="肺癌":
            #遍历数据库第四个工作表Drugs(NSCLC)的除第一行外的所有行
            for i in range(1,nrows):
                #读取数据库第四个工作表Drugs(NSCLC)里每行的RefID那一列值，例如：msi_h，存到变量RefID里
                RefID = table.row(i)[0].value
                if RefID == k[1]:
                    drug = table.row(i)[5].value
                    if table.row(i)[7].ctype == 2:
                        evidence_level = str(int(table.row(i)[7].value))
                    else:
                        evidence_level = str(table.row(i)[7].value)
                    #evidence_level = str(table.row(i)[7].value)
                    drug_list.append(drug)
                    evidence_list.append(evidence_level)
        #判断检测癌种是否为肺癌
        elif basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="结直肠癌":
            #遍历数据库第11个工作表Drugs(CRC)的除第一行外的所有行
            for i in range(1,nrows_CRC):
                #读取数据库第11个工作表Drugs(NSCLC)里每行的RefID那一列值，例如：msi_h，存到变量RefID里
                RefID = table_CRC.row(i)[0].value
                if RefID == k[1]:
                    drug = table_CRC.row(i)[5].value
                    if table_CRC.row(i)[7].ctype == 2:
                        evidence_level = str(int(table_CRC.row(i)[7].value))
                    else:
                        evidence_level = str(table_CRC.row(i)[7].value)
                    #evidence_level = str(table_CRC.row(i)[7].value)
                    drug_list.append(drug)
                    evidence_list.append(evidence_level)
                
                
                
                
        #将evidence_drug及drug_list里的各个元素合并并用回车分隔开存到一个新的变量new_evidence_list及new_drug_list里，此时new_evidence_list及new_drug_list已经不是列表，而是字符，这样在输出的表格里是作为一个字符输出在一个格子里，行与行之间有回车，但没有边框线
        new_evidence_list="\n".join(evidence_list)
        new_drug_list="\n".join(drug_list)
        #向字典里添加键为"Detected_Gene_Mutation_Target_Drugs"，值为RichText(new_drug_list) 的键值对   ，如果不加RichText()则\n不能自动回车
        add_d_new["Detected_Gene_Mutation_Target_Drugs"] = RichText(new_drug_list)     
        #向字典里添加键为"Evidence_level"，值为RichText(new_evidence_list) 的键值对   ，如果不加RichText()则\n不能自动回车
        add_d_new["Evidence_level"] = RichText(new_evidence_list)
        #向字典里添加键为"n_row_each_snp"，值为len(drug_list)及药物个数 的键值对 
        add_d_new["n_row_each_snp"] = len(drug_list)
        #将前面生成的字典add_d_new加到字典d1的键为'msi_Drug_Table'原来值为空列表[]的列表里
        d1['msi_Drug_Table'].append(add_d_new)   
        #向字典里添加键为"msi"，值为k[0] （即报告里“二、检测结果总览：msi表格里”的内容）键值对 
        d2={'msi':k[0]}
    f1.close()
    return d1,d2#返回字典d1,d2的值
#调用函数test_msi，返回值Msi_Dict=d1,msi_table_dict=d2
Msi_Dict,msi_table_dict = test_msi(msi_result_file,db_file)
#更新字典context内容,添加Msi_Dict,msi_table_dict字典到context字典里
context.update(Msi_Dict) 
context.update(msi_table_dict)
#print(Msi_Dict)
 ##############################################################################
##############################################################################################################################################################################

##############################################################################ClinicalTrials表格，目前只有靶向突变有相关临床实验，SNP及msi检测结果没有临床试验
#############################################通过函数test_Clinical(mutation_uniq_gene_list_file,db_file)实现，目前按照mutation_uniq_gene_list_file(例如：C_0101200320001_mutation_uniq_gene_list.txt）第二列基因名字和"S001报告生成数据库_20200117v1.xlsx"里的第7个工作表ClinicalTrials表格里的第一列来匹配
def test_Clinical(filein,db_name):
    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #定义一个字典d1,键名为ClinicalTrials_Table，值为一个空列表[],这个字典的键名ClinicalTrials_Table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：“四、相关临床研究”{%tr for a in ClinicalTrials_Table %}里的ClinicalTrials_Table即为此处定义而来。
    d1 = { 'ClinicalTrials_Table' : [] }
    #f1用于接收打开filein=mutation_uniq_gene_list_file，例如：C_0101200320001_mutation_uniq_gene_list.txt
    f1 = open(filein, "r", encoding ='utf-8')
    #line_N = int(f1.readline().rstrip().replace('##', ''))
    
    
    #用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table = data.sheet_by_index(6)#数据库文件的第7个工作表ClinicalTrials的内容存到table里
    nrows = table.nrows#数据库文件的第7个工作表的行数存到nrows里
    genename_list_lung=[]
    genename_list_CRC=[]
    for v in range(1,nrows):
        if table.row(v)[4].value=="NSCLC":
            genename_list_lung.append(table.row(v)[0].value)
        elif table.row(v)[4].value=="CRC":
            genename_list_CRC.append(table.row(v)[0].value)
        
    #print(len(genename_list_lung))
    #print(len(genename_list_CRC))
    #genename_list=table.col_values(0, start_rowx=0, end_rowx=None)
    
    #print(genename_list)
    #遍历mutation_uniq_gene_list_file(例如：C_0101200320001_mutation_uniq_gene_list.txt）里的每一行，此文件为基因名字去重后的结果，所以每一行为一个基因的结果
    for line in f1:
        #定义一个空字典add_d_new
        add_d_new = {}
        #定义一些空列表
        Title_list = []
        Phase_list = [] 
        Locations_list = [] 
        Indication_list = [] 
        RefNCT_list = [] 
        combined_list=[]
        #遍历mutation_uniq_gene_list_file(例如：C_0101200320001_mutation_uniq_gene_list.txt）每一行的结果存在k里
        #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
        k= line.rstrip().split("\t")
        Bytes_k=bytes(k[0],encoding="gbk")
        #向字典里添加键为"Mutation_Gene_Name"，值为RichText(k[1]+' ',italic=True) 即基因名字的键值对 
        add_d_new["Mutation_Gene_Name"] = RichText(k[1]+' ',italic=True)
        #add_d_new["Gene_Mutation_Name"] = RichText(k[1],italic=False)
        #遍历数据库第7个工作表ClinicalTrials的除第一行外的所有行
        for i in range(1,nrows):
            #读取数据库第7个工作表ClinicalTrials第一列基因名字并存到GeneName里
            GeneName = table.row(i)[0].value
            bytes_GeneName=bytes(GeneName,encoding="gbk")
            #判断如果mutation_uniq_gene_list_file(例如：C_0101200320001_mutation_uniq_gene_list.txt）里的基因名k[1]与数据库第7个工作表ClinicalTrials的第一列基因名一样时：
            if GeneName == k[1] and k[2]=="lung" and table.row(i)[4].value=="NSCLC":
                #print(k[0])
                #读取临床试验Title并存到Title变量里
                Title = table.row(i)[1].value
                #如果临床试验的Phase的ctype为2则取整数int处理，否则保持不变，例如Phase=2,则int(2)，如果Phase=2|3就保留原样不取整
                if table.row(i)[2].ctype == 2:
                    Phase = int(table.row(i)[2].value)
                else:
                    Phase = table.row(i)[2].value
                #临床实验地点英文
                Location = table.row(i)[3].value.replace(' ','')
                #临床试验地点中文，根据前面提供的country.txt那个文件读入后存入的字典来获得
                Location_Chinese=country_dict[Location]
                #适应症
                Indication = table.row(i)[4].value
                #NCT编号
                RefNCT = table.row(i)[5].value     
                #将前面生成的一些值存到各自的列表里
                Title_list.append(Title)
                Phase_list.append(Phase)
                Locations_list.append(Location_Chinese)
                Indication_list.append(Indication)
                RefNCT_list.append(RefNCT)
                #combined_list.append(str(Title)+"___"+str(Phase)+"___"+str(Location_Chinese)+"___"+str(Indication)+"___"+str(RefNCT))
            elif GeneName == k[1] and k[2]=="CRC" and table.row(i)[4].value=="CRC":     
                #print(k[0])
                #读取临床试验Title并存到Title变量里
                Title = table.row(i)[1].value
                #如果临床试验的Phase的ctype为2则取整数int处理，否则保持不变，例如Phase=2,则int(2)，如果Phase=2|3就保留原样不取整
                if table.row(i)[2].ctype == 2:
                    Phase = int(table.row(i)[2].value)
                else:
                    Phase = table.row(i)[2].value
                #临床实验地点英文
                Location = table.row(i)[3].value.replace(' ','')
                #print(Location)
                #临床试验地点中文，根据前面提供的country.txt那个文件读入后存入的字典来获得
                Location_Chinese=country_dict[Location]
                #适应症
                Indication = table.row(i)[4].value
                #NCT编号
                RefNCT = table.row(i)[5].value     
                #将前面生成的一些值存到各自的列表里
                Title_list.append(Title)
                Phase_list.append(Phase)
                Locations_list.append(Location_Chinese)
                Indication_list.append(Indication)
                RefNCT_list.append(RefNCT)
                #combined_list.append(str(Title)+"___"+str(Phase)+"___"+str(Location_Chinese)+"___"+str(Indication)+"___"+str(RefNCT))
            elif k[2]=="lung" and k[1] not in genename_list_lung:
                #print(k[1])
                #读取临床试验Title并存到Title变量里
                Title = "未有搜索到相关临床研究"
                Phase = "/"
                Location = "/"
                #临床试验地点中文，根据前面提供的country.txt那个文件读入后存入的字典来获得
                Location_Chinese= "/"
                Indication="/"
                RefNCT = "/"
                #将前面生成的一些值存到各自的列表里
                #Title_list.append(Title)
                #Phase_list.append(Phase)
                #Locations_list.append(Location_Chinese)
                #Indication_list.append(Indication)
                #RefNCT_list.append(RefNCT)
                combined_list.append(str(Title)+"___"+str(Phase)+"___"+str(Location_Chinese)+"___"+str(Indication)+"___"+str(RefNCT))
            elif k[2]=="CRC" and k[1] not in genename_list_CRC:
                #print(k[1])
                #读取临床试验Title并存到Title变量里
                Title = "未有搜索到相关临床研究"
                Phase = "/"
                Location = "/"
                #临床试验地点中文，根据前面提供的country.txt那个文件读入后存入的字典来获得
                Location_Chinese= "/"
                Indication="/"
                RefNCT = "/"
                #将前面生成的一些值存到各自的列表里
                #Title_list.append(Title)
                #Phase_list.append(Phase)
                #Locations_list.append(Location_Chinese)
                #Indication_list.append(Indication)
                #RefNCT_list.append(RefNCT)
                combined_list.append(str(Title)+"___"+str(Phase)+"___"+str(Location_Chinese)+"___"+str(Indication)+"___"+str(RefNCT))
                    
         
        
        
        #将前面生成的drug_evidence_list通过list(set(drug_evidence_list))去重，去重后重新生成drug_list，evidence_list
        U_Title_list = []
        U_Phase_list = []     
        U_Locations_list=[]
        U_Indication_list=[]
        U_RefNCT_list=[]
        for h in list(set(combined_list)):
            U_Title_list.append(h.split("___")[0])
            U_Phase_list.append(h.split("___")[1])  
            U_Locations_list.append(h.split("___")[2])
            U_Indication_list.append(h.split("___")[3])    
            U_RefNCT_list.append(h.split("___")[4])    
        #向字典里添加键值对 
        add_d_new["ClinicalTrials_Title"] = Title_list+U_Title_list
        add_d_new["ClinicalTrials_Phase"] = Phase_list+U_Phase_list
        add_d_new["ClinicalTrials_Locations"] = Locations_list+U_Locations_list
        add_d_new["ClinicalTrials_Indication"] = Indication_list+U_Indication_list
        add_d_new["ClinicalTrials_RefNCT"] = RefNCT_list+U_RefNCT_list     
        add_d_new["n_row_each_gene"] = len(Title_list)
        #将前面生成的字典add_d_new加到字典d1的键为'ClinicalTrials_Table'原来值为空列表[]的列表里
        d1['ClinicalTrials_Table'].append(add_d_new)    
    f1.close()
    return d1
#调用函数test_Clinical，返回值ClinicalTrials_Dict=d1
ClinicalTrials_Dict = test_Clinical(mutation_uniq_gene_list_file,db_file)
#print(ClinicalTrials_Dict)
#更新字典context内容,添加ClinicalTrials_Dict字典到context字典里
context.update(ClinicalTrials_Dict) 
##############################################################################################################################################################################


###################五、相关用药信息 ：  靶向药物相关的基因
#通过test_drug函数读入mutation_uniq_gene_list_file（例如：C_0101200320001_mutation_uniq_gene_list.txt）,mutation_del3_file(例如：C_0101200320001_mutation_del3.txt)和db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现

def test_drug(filein1,filein2,db_name):
    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #定义一个字典d1,键名为Fifth_Target_Drug_Table，值为一个空列表[],这个字典的键名Fifth_Target_Drug_Table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：“五、相关用药信息 ：  靶向药物相关的基因”{%p for a in Fifth_Target_Drug_Table %}里的Fifth_Target_Drug_Table即为此处定义而来。
    d1 = { 'Fifth_Target_Drug_Table' : [] }
    #f2用于接收打开filein2=mutation_del3_file(例如：C_0101200320001_mutation_del3.txt)
    f2 = open(filein2,'r',encoding ='utf-8')
    #将这个样本检测出靶向突变的个数存在line_N里
    line_N = int(f2.readline().rstrip().replace('##', ''))
    #将mutation_del3_file(例如：C_0101200320001_mutation_del3.txt)每一行的内容读入并存到data_mut里
    data_mut = f2.readlines()
    f2.close()
    #print(line_N)
    #print(data_mut)
    
    #f1用于接收打开filein1=mutation_uniq_gene_list_file（例如：C_0101200320001_mutation_uniq_gene_list.txt）,即去重后的有靶向突变的基因名字文件
    f1 = open(filein1, "r", encoding ='utf-8')
    #定义空列表，用于后面生成6.3的参考引文
    Part_author_list = []
    Part_PMID_list = []

    ##用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table = data.sheet_by_index(8)   #基因介绍  #数据库文件的第10个工作表gene_intro的内容存到table里
    table_target = data.sheet_by_index(4)   #药物未去重  #数据库文件的第5个工作表Targeted的内容存到table_target里
    table_drug = data.sheet_by_index(3)     #药物已去重  #数据库文件的第4个工作表Drugs(NSCLC)的内容存到table_drug里
    table_CRC=data.sheet_by_index(9)#数据库文件的第10个工作表Drugs(CRC)的内容存到table_CRC里
    #print(table_CRC.row(1)[0].value)
    nrows = table.nrows  #数据库文件的第10个工作表的行数存到nrows里
    nrows_target = table_target.nrows #数据库文件的第5个工作表的行数存到nrows_target里
    nrows_drug = table_drug.nrows #数据库文件的第4个工作表的行数存到nrows_drug里
    nrows_CRC=table_CRC.nrows#数据库文件的第10个工作表的行数存到nrows_drug里
    
    NSCLC_refid_list=[]
    NSCLC_refid=''
    for f in range(1,nrows_drug):
        NSCLC_refid=table_drug.row(f)[0].value
        NSCLC_refid_list.append(NSCLC_refid)
        
    CRC_refid_list=[]
    CRC_refid=''
    for f in range(1,nrows_CRC):
        CRC_refid=table_CRC.row(f)[0].value
        CRC_refid_list.append(CRC_refid)
    
    
    
    #print(nrows_CRC)
    #定义空字符变量，用于后面存放基因简介信息
    gene_intro = ''
    
    
    
    
    #遍历mutation_uniq_gene_list_file（例如：C_0101200320001_mutation_uniq_gene_list.txt）每一行
    for line in f1:
        #定义一个空字典add_d_new
        add_d_new = {}
        #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
        k= line.rstrip().split("\t")
        #print(k)
        #向字典里添加键值对
        add_d_new["Gene_Name"] = k[1]
        add_d_new["Gene_Number"] = RichText(k[0],italic=False)
        
            
        mutation_type = ''
        mutation_type_list = []

        #遍历数据库第10个工作表gene_intro的除第一行外的所有行
        for i in range(1,nrows):
            cancer_type_eng = table.row(i)[1].value
            #print(cancer_type_eng)
            gene = table.row(i)[2].value
            #判断数据库第10个工作表gene_intro第二列与mutation_uniq_gene_list_file第三列癌种一致并且数据库第10个工作表gene_intro第三列与mutation_uniq_gene_list_file第二列基因名是否一致
            if cancer_type_eng == k[2] and gene == k[1] :
                #print(cancer_type_eng)
                #print(k[2])
                #print(gene)
                #print(k[1])
                #print("yes")
                gene_intro = table.row(i)[4].value.replace("\\n","\n")
                #print(gene_intro)
                #分两种情况判断：mutation_uniq_gene_list_file第一列为空（当没有检测出靶向突变时此处为空）和不为空（靶向突变个数不为零）的情况
                if k[0] == ' ':
                    add_d_new["Mutation_Gene_Name"] = RichText(' ',italic=True)
                else:
                    add_d_new["Mutation_Gene_Name"] = RichText(table.row(i)[3].value+' ',italic=True)
                    #print(table.row(i)[3].value)
        #向字典里添加键值对
        add_d_new["Gene_introduction"] = RichText(gene_intro)   
        #向字典里添加键值对
        add_d_new["ClinicalDescrip"] = { 'ClinicalDescription_Table' : [] }

        #定义一个空列表
        d_mutation=[]
        #循环mutation_del3_file（基因未去重的靶向突变结果）里的每一行                
        for m in data_mut:
            
            mutation_type = ''
            mutation_type_list = []      
            #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到z里，z是个列表
            z = m.rstrip().split("\t")
            #判断mutation_uniq_gene_list_file第二列的值与mutation_del3_file第一列的值（基因名字）是否一致
            if k[1] == z[0]:
                mutation_refid = z[5]
                #定义一个空字典add_new
                add_new = {}
                #如果mutation_del3_file第6列refid的值（存在mutation_refid变量里）为no_mutation,则mutation_type = "没有检出突变"；否则mutation_type赋值为mutation_del3_file里的第二列的值
                if mutation_refid == "no_mutation":  
                    mutation_type = "没有检出突变"
                else:
                    mutation_type = z[1]
                mutation_type_list.append(mutation_type)
                
                drug = ''
                drug_list = []
                d_drug = []
                #如果样本癌种为肺癌
                if z[6] == "lung" and (z[5] in NSCLC_refid_list):
                
                    ##遍历数据库第4个工作表Drugs(NSCLC)的除第一行外的所有行
                    for i in range(1,nrows_drug):
                    
                        RefID = table_drug.row(i)[0].value
                        #判断mutation_del3_file第一列基因名与数据库第4个工作表Drugs(NSCLC)第2列基因名一致，并且mutation_del3_file第6列refid的值（存在mutation_refid变量里）与数据库第4个工作表Drugs(NSCLC)的第1列refid值一致，并且mutation_del3_file第7列癌种为“lung”
                        if z[0]== table_drug.row(i)[1].value and mutation_refid == RefID and z[6] == "lung":
                            add_new2 = {}
                            drug = table_drug.row(i)[5].value
                            #print(drug)
                            drug_list.append(drug)
                        
                            ClinicalDescription = ''
                            ClinicalDescription_list = []
                            RefPMID = ''
                            PMID_for_ref=''
                            RefPMID_list = []
                            Author = ''
                            Author_list = []
                            ###遍历数据库第5个工作表Targeted的除第一行外的所有行
                            for p in range(1,nrows_target):
                                #判断mutation_del3_file第一列基因名与数据库第5个工作表Targeted的第二列基因名一致，并且mutation_del3_file第6列refid的值（存在mutation_refid变量里）与数据库第5个工作表Targeted的第1列refid值一致，并且数据库第4个工作表Drugs(NSCLC)的第11列（table_drug.row(i)[10].value）与数据库第5个工作表Targeted的第5列药物名字一致，并且数据库第5个工作表Targeted的7列值为“x”
                                if z[0]== table_target.row(p)[1].value and mutation_refid == table_target.row(p)[0].value and table_drug.row(i)[10].value==table_target.row(p)[4].value and table_target.row(p)[6].value == "x":
                                    #print(table_target.row(p)[6].value)
                                    ClinicalDescription = table_target.row(p)[9].value
                                
                                    Pre_author=table_target.row(p)[10].value
                                    #print(mutation_refid)
                                    #如果mutation_del3_file第6列refid的值（存在mutation_refid变量里）为no_mutation，Author为空值，否则Author为数据库第5个工作表Targeted的第11列前面加(，后面加逗号，为了在表格“五、相关用药信息 ：  靶向药物相关的基因”相关研究依据那一列里方便展示
                                    if mutation_refid == "no_mutation" or mutation_refid == "nras_onc":
                                        Author=""
                                    else:
                                        Author = "("+str(table_target.row(p)[10].value)+","
                                    #判断数据库第5个工作表Targeted的第12列PMID号如果为整数(ctype==2),则取整，或取整后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  靶向药物相关的基因”相关研究依据那一列里方便展示
                                    if table_target.row(p)[11].ctype == 2:
                                        RefPMID = "PMID:"+str(int(table_target.row(p)[11].value))+")"
                                        PMID_for_ref=int(table_target.row(p)[11].value)#只取整，用于生成6.3参考引文部分
                                    #如果mutation_del3_file第6列refid的值（存在mutation_refid变量里）为no_mutation,则RefPMID为空
                                    elif mutation_refid == "no_mutation" or mutation_refid == "nras_onc":
                                        RefPMID=""
                                    #判断数据库第5个工作表Targeted的第12列PMID号如果不为整数(ctype==2),mutation_refid也不是no_mutation,则不取整，而是转换为字符str()后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  靶向药物相关的基因”相关研究依据那一列里方便展示
                                    else:
                                        RefPMID ="PMID:"+str(table_target.row(p)[11].value)+")"
                                        PMID_for_ref=table_target.row(p)[11].value
                                    ClinicalDescription_list.append(ClinicalDescription)
                                    RefPMID_list.append(RefPMID)
                                    Author_list.append(Author)
                                    Part_author_list.append(Author)
                                    Part_PMID_list.append(PMID_for_ref)##用于后面生成6.3参考引文
                            #字典里添加键值对        
                            add_new2['ClinicalDescription_list_table']=ClinicalDescription_list
                            add_new2['Author_list_table']=Author_list
                            add_new2['RefPMID_list_table']=RefPMID_list
                            add_new2['RefPMID_number']=len(RefPMID_list)
                        #将add_new2这个字典添加到d_drug这个列表中
                            d_drug.append(add_new2)
                #如果样本癌种为结直肠癌
                elif z[6] == "CRC" and (z[5] in CRC_refid_list):
                    ##遍历数据库11个工作表Drugs(CRC)的除第一行外的所有行
                    for i in range(1,nrows_CRC):
                    
                        RefID = table_CRC.row(i)[0].value
                        #print(table_CRC.row(i)[0].value)
                        #判断mutation_del3_file第一列基因名与数据库第11个工作表Drugs(CRC)第2列基因名一致，并且mutation_del3_file第6列refid的值（存在mutation_refid变量里）与数据库第11个工作表Drugs(CRC)的第1列refid值一致，并且mutation_del3_file第7列癌种为“CRC”
                        if z[0]== table_CRC.row(i)[1].value and mutation_refid == RefID and z[6] == "CRC":
                            add_new2 = {}
                            drug = table_CRC.row(i)[5].value
                            #print(drug)
                            drug_list.append(drug)
                        
                            ClinicalDescription = ''
                            ClinicalDescription_list = []
                            RefPMID = ''
                            PMID_for_ref=''
                            RefPMID_list = []
                            Author = ''
                            Author_list = []
                            ###遍历数据库第5个工作表Targeted的除第一行外的所有行
                            for p in range(1,nrows_target):
                                #print(table_target.row(p)[4].value)
                                #判断mutation_del3_file第一列基因名与数据库第5个工作表Targeted的第二列基因名一致，并且mutation_del3_file第6列refid的值（存在mutation_refid变量里）与数据库第5个工作表Targeted的第1列refid值一致，并且数据库第11个工作表Drugs(CRC)的第11列（table_CRC.row(i)[10].value）与数据库第5个工作表Targeted的第5列药物名字一致，并且数据库第5个工作表Targeted的8列值为“x”
                                if z[0]== table_target.row(p)[1].value and mutation_refid == table_target.row(p)[0].value and table_CRC.row(i)[10].value==table_target.row(p)[4].value and table_target.row(p)[7].value == "x":
                                    
                                    ClinicalDescription = table_target.row(p)[9].value
                                
                                    Pre_author=table_target.row(p)[10].value
                                    #print(mutation_refid)
                                    #如果mutation_del3_file第6列refid的值（存在mutation_refid变量里）为no_mutation，Author为空值，否则Author为数据库第5个工作表Targeted的第11列前面加(，后面加逗号，为了在表格“五、相关用药信息 ：  靶向药物相关的基因”相关研究依据那一列里方便展示
                                    if mutation_refid == "no_mutation" or mutation_refid == "tp53_onc":
                                        Author=""
                                    else:
                                        Author = "("+str(table_target.row(p)[10].value)+","
                                    #判断数据库第5个工作表Targeted的第12列PMID号如果为整数(ctype==2),则取整，或取整后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  靶向药物相关的基因”相关研究依据那一列里方便展示
                                    if table_target.row(p)[11].ctype == 2:
                                        RefPMID = "PMID:"+str(int(table_target.row(p)[11].value))+")"
                                        PMID_for_ref=int(table_target.row(p)[11].value)#只取整，用于生成6.3参考引文部分
                                    #如果mutation_del3_file第6列refid的值（存在mutation_refid变量里）为no_mutation,则RefPMID为空
                                    elif mutation_refid == "no_mutation" or mutation_refid == "tp53_onc":
                                        RefPMID=""
                                    #判断数据库第5个工作表Targeted的第12列PMID号如果不为整数(ctype==2),mutation_refid也不是no_mutation,则不取整，而是转换为字符str()后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  靶向药物相关的基因”相关研究依据那一列里方便展示
                                    else:
                                        RefPMID ="PMID:"+str(table_target.row(p)[11].value)+")"
                                        PMID_for_ref=table_target.row(p)[11].value
                                    ClinicalDescription_list.append(ClinicalDescription)
                                    RefPMID_list.append(RefPMID)
                                    Author_list.append(Author)
                                    Part_author_list.append(Author)
                                    Part_PMID_list.append(PMID_for_ref)#用于后面生成6.3参考引文
                            #字典里添加键值对        
                            add_new2['ClinicalDescription_list_table']=ClinicalDescription_list
                            add_new2['Author_list_table']=Author_list
                            add_new2['RefPMID_list_table']=RefPMID_list
                            add_new2['RefPMID_number']=len(RefPMID_list)
                        #将add_new2这个字典添加到d_drug这个列表中
                            d_drug.append(add_new2)
                 
                 
                 
                 
                 
                 
                 
                 
                #如果样本癌种为结直肠癌
                elif z[6] == "CRC" and (z[5] not in CRC_refid_list):

                    add_new2 = {}
                    drug = "/"
                    #print(drug)
                    drug_list.append(drug)
                    ClinicalDescription = "/"    
                    ClinicalDescription_list = []
                    RefPMID = ""
                    RefPMID_list = []
                    Author = ""
                    Author_list = []
                    ClinicalDescription_list.append(ClinicalDescription)
                    RefPMID_list.append(RefPMID)
                    Author_list.append(Author)
                    Part_author_list.append(Author)
                            #字典里添加键值对        
                    add_new2['ClinicalDescription_list_table']=ClinicalDescription_list
                    add_new2['Author_list_table']=Author_list
                    add_new2['RefPMID_list_table']=RefPMID_list
                    add_new2['RefPMID_number']=len(RefPMID_list)
                        #将add_new2这个字典添加到d_drug这个列表中
                    d_drug.append(add_new2)                 
                 
                 
                 
                #如果样本癌种为结肺癌
                elif z[6] == "lung" and (z[5] not in NSCLC_refid_list):

                    add_new2 = {}
                    drug = "/"
                    #print(drug)
                    drug_list.append(drug)
                    ClinicalDescription = "/"    
                    ClinicalDescription_list = []
                    RefPMID = ""
                    RefPMID_list = []
                    Author = ""
                    Author_list = []
                    ClinicalDescription_list.append(ClinicalDescription)
                    RefPMID_list.append(RefPMID)
                    Author_list.append(Author)
                    Part_author_list.append(Author)
                            #字典里添加键值对        
                    add_new2['ClinicalDescription_list_table']=ClinicalDescription_list
                    add_new2['Author_list_table']=Author_list
                    add_new2['RefPMID_list_table']=RefPMID_list
                    add_new2['RefPMID_number']=len(RefPMID_list)
                        #将add_new2这个字典添加到d_drug这个列表中
                    d_drug.append(add_new2)                        
                 
                 
                 
                 
                 
                 
                #print(k[1])
                #print(mutation_refid)
                #print(drug_list)
                add_new['drug_list_table']=drug_list
                add_new['drug_number'] = len(drug_list)
                add_new['drug_description']=d_drug
                #print(d_drug)
                
                add_new["Mutation_type"]=mutation_type
               
                d_mutation.append(add_new)
                
        #print(d_mutation)
        add_d_new["Mutation"] = d_mutation
        add_d_new["Mutation_type_number"]=len(mutation_type_list)
        add_d_new["Mutation_type_list_table"]=mutation_type_list
        
        d1['Fifth_Target_Drug_Table'].append(add_d_new)

    f1.close()
    return d1,Part_PMID_list
Fifth_Target_Drug_Table_Dict,part_PMID_target_list = test_drug(mutation_uniq_gene_list_file,mutation_del3_file,db_file)
#print(Fifth_Target_Drug_Table_Dict)
#print(part_PMID_target_list)
context.update(Fifth_Target_Drug_Table_Dict) 

##############################################################################################################################################################################

################################################五、相关用药信息 ：  化疗药物相关的基因 
##通过test_chemo_drug函数读入uniq_snp_chemo_file（例如：C_0101200320001_uniq_snp_chemo.txt）和db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现
#uniq_snp_chemo_file（例如：C_0101200320001_uniq_snp_chemo.txt）与snp_chemo_file（例如：C_0101200320001_uniq_snp_chemo.txt）的差别只在于第一行有无##数字，其它因为SNP不存在一个样品的一个基因有多种SNP表型的可能，所以没有进行去重，即使不去重也没有重复的可能
def test_chemo_drug(filein1,db_name):
    

    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #定义一个字典d1,键名为Fifth_chemo_table，值为一个空列表[],这个字典的键名Fifth_chemo_table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：{%tr for a in Fifth_chemo_table %}里的Fifth_chemo_table即为此处定义而来。
    d1 = { 'Fifth_chemo_table' : [] }
    #f1用于接收打开filein1=uniq_snp_chemo_file（例如：C_0101200320001_uniq_snp_chemo.txt）
    f1 = open(filein1, "r", encoding ='utf-8')
    #用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table_target = data.sheet_by_index(5)   #药物未去重 #数据库文件的第6个工作表Chemo的内容存到table_target里
    nrows_target = table_target.nrows #数据库文件的第6个工作表Chemo的行数存到nrows_target里
    #新建空列表
    Part_author_list = []
    Part_PMID_list=[]
    #遍历uniq_snp_chemo_file（例如：C_0101200320001_uniq_snp_chemo.txt）文件里的每一行
    for line in f1:
        #新建一个空字典
        add_new = {}
        #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
        k= line.rstrip().split("\t")
        #生成字典的键值对
        add_new["Gene_Name"] = RichText(k[0],italic = True)

        add_new["Chemo_Gene_Name"] = RichText(k[0]+' ',italic=False)
        #新建空字符或者列表
        mutation_type = ''
        mutation_type_list = []      
        drug = ''
        drug_list = []
        mutation_type = ''
        mutation_type_list = []
        ClinicalDescription = ''
        ClinicalDescription_list = []
        RefPMID = ''
        PMID_for_ref=''
        RefPMID_list = []
        Author = ''
        Author_list = []
        d_mutation=[]
        ###遍历数据库第6个工作表Chemo的的除第一行外的所有行                
        for m in range(1,nrows_target):
            #如果uniq_snp_chemo_file（例如：C_0101200320001_uniq_snp_chemo.txt）文件的第三行refid(例如：mthfr_677)与数据库第6个工作表Chemo的第一列的refid一致,癌种为肺癌basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="肺癌"， 数据库第6个工作表Chemo的第4列有"x"
            if k[3] == table_target.row(m)[0].value and basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="肺癌" and table_target.row(m)[3].value == "x":
                mutation_refid = table_target.row(m)[0].value                    
                mutation_type = table_target.row(m)[2].value
                mutation_type_list.append(mutation_type)
                
                drug = table_target.row(m)[5].value
                drug_list.append(drug)
                ClinicalDescription = table_target.row(m)[6].value
                ClinicalDescription_list.append(ClinicalDescription)
                ##判断数据库第6个工作表Chemo的第9列PMID号如果为整数(ctype==2),则取整，或取整后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  化疗药物”相关研究依据那一列里方便展示
                if table_target.row(m)[8].ctype == 2:
                    RefPMID = "PMID:"+str(int(table_target.row(m)[8].value))+")"
                    PMID_for_ref=int(table_target.row(m)[8].value)
                ##判断数据库第6个工作表Chemo的第9列PMID号如果不为整数,则不取整，而是将PMID转化为str然后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  化疗药物”相关研究依据那一列里方便展示
                else:
                    RefPMID ="PMID:"+str(table_target.row(m)[8].value)+")"
                    PMID_for_ref=table_target.row(m)[8].value
                RefPMID_list.append(RefPMID)
                #作者在左边加括号，右边加逗号，为了在表格“五、相关用药信息 ：  化疗药物”相关研究依据那一列里方便展示
                Author = "("+str(table_target.row(m)[7].value)+","
                Part_author_list.append(Author)
                Author_list.append(Author)
                Part_PMID_list.append(PMID_for_ref)#用于后面生成6.3参考引文
            #如果uniq_snp_chemo_file（例如：C_0101200320001_uniq_snp_chemo.txt）文件的第三行refid(例如：mthfr_677)与数据库第6个工作表Chemo的第一列的refid一致,癌种为肺癌basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="结直肠癌"， 数据库第6个工作表Chemo的第5列有"x"    
            elif k[3] == table_target.row(m)[0].value and basic_information_dict['DETECTION_OF_CANCER_SPECIES']=="结直肠癌" and table_target.row(m)[4].value == "x":
                mutation_refid = table_target.row(m)[0].value                    
                mutation_type = table_target.row(m)[2].value
                mutation_type_list.append(mutation_type)
                
                drug = table_target.row(m)[5].value
                drug_list.append(drug)
                ClinicalDescription = table_target.row(m)[6].value
                ClinicalDescription_list.append(ClinicalDescription)
                ##判断数据库第6个工作表Chemo的第9列PMID号如果为整数(ctype==2),则取整，或取整后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  化疗药物”相关研究依据那一列里方便展示
                if table_target.row(m)[8].ctype == 2:
                    RefPMID = "PMID:"+str(int(table_target.row(m)[8].value))+")"
                    PMID_for_ref=int(table_target.row(m)[8].value)
                ##判断数据库第6个工作表Chemo的第9列PMID号如果不为整数,则不取整，而是将PMID转化为str然后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  化疗药物”相关研究依据那一列里方便展示
                else:
                    RefPMID ="PMID:"+str(table_target.row(m)[8].value)+")"
                    PMID_for_ref=table_target.row(m)[8].value
                RefPMID_list.append(RefPMID)
                #作者在左边加括号，右边加逗号，为了在表格“五、相关用药信息 ：  化疗药物”相关研究依据那一列里方便展示
                Author = "("+str(table_target.row(m)[7].value)+","
                Part_author_list.append(Author)
                Author_list.append(Author)
                Part_PMID_list.append(PMID_for_ref)#用于后面生成6.3参考引文
            
            
            
            
            
            
            

        add_new['drug_list_table']=drug_list
        add_new['drug_number'] = len(drug_list)
        add_new['Clinical_Descrip_table']=ClinicalDescription_list
        add_new['RefPMID_table']=RefPMID_list
        add_new['Author_table']=Author_list

                #print(d_drug)
                
        add_new["Mutation_type"]=mutation_type
       
        d1['Fifth_chemo_table'].append(add_new)

    f1.close()
    return d1,Part_PMID_list


#调用函数test_chemo_drug，返回值Fifth_chemo_Table_Dict=d1,part_pmid_chemo_list=Part_PMID_list
Fifth_chemo_Table_Dict,part_pmid_chemo_list = test_chemo_drug(uniq_snp_chemo_file,db_file)
#print(Fifth_chemo_Table_Dict)
#print(part_pmid_chemo_list)
context.update(Fifth_chemo_Table_Dict) 


############################################################################################################################################################################


################################################五、相关用药信息 ：  msi相关
##通过test_msi_table函数读入msi_result_file(例如：C_0101200320001_msi_result.txt),db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现
def test_msi_table(filein1,db_name):
    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #定义一个字典d1,键名为Fifth_msi_table，值为一个空列表[],这个字典的键名Fifth_msi_table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：{%tr for a in Fifth_msi_table %}里的Fifth_msi_table即为此处定义而来。
    d1 = { 'Fifth_msi_table' : [] }
    #f1用于接收打开filein1=msi_result_file（例如：C_0101200320001_msi_result.txt）
    f1 = open(filein1, "r", encoding ='utf-8')
    #用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table_target = data.sheet_by_index(4)   #药物未去重#数据库文件的第5个工作表Targeted的内容存到table_target里
    nrows_target = table_target.nrows#数据库文件的第5个工作表Targeted的行数存到nrows_target里
    Part_author_list = []
    Part_PMID_list=[]
    #遍历msi_result_file(例如：C_0101200320001_msi_result.txt)文件里的每一行
    for line in f1:
        #新建一个空字典
        add_new = {}
        #每一行突变用读进来后去除右侧的空白符号，然后用“\t”分隔的结果存到k里，k是个列表
        k= line.rstrip().split("\t")
        #生成字典的键值对
        add_new["msi_Name"] = RichText(k[0],italic = False)

        mutation_type = ''
        mutation_type_list = []      
        drug = ''
        drug_list = []
        mutation_type = ''
        mutation_type_list = []
        ClinicalDescription = ''
        ClinicalDescription_list = []
        RefPMID = ''
        PMID_for_ref=''
        RefPMID_list = []
        Author = ''
        Author_list = []
        d_mutation=[]
        ###遍历数据库第5个工作表Targeted的的除第一行外的所有行       
        for m in range(1,nrows_target):

            if k[1] == table_target.row(m)[0].value: #将输入msi结果的表格与数据库第5个工作表Targeted里面的第一列匹配
                mutation_refid = table_target.row(m)[0].value                    
                mutation_type = table_target.row(m)[2].value
                mutation_type_list.append(mutation_type)
                
                drug = table_target.row(m)[4].value
                drug_list.append(drug)
                ClinicalDescription = table_target.row(m)[9].value
                ClinicalDescription_list.append(ClinicalDescription)

                #判断如果数据库第5个工作表Targeted里面的第一列mutation_refid为mss
                if mutation_refid == "mss":
                    #print("yes")
                    Author=""
                    RefPMID=""
                #否则如果数据库第5个工作表Targeted里面的第一列mutation_refid为msi_h
                elif mutation_refid=="msi_h":
                    #print("no")
                    Author = "("+str(table_target.row(m)[10].value)+","
                    ##判断数据库第5个工作表Targeted的第12列PMID号如果为整数(ctype==2),则取整，或取整后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ： 免疫药物相关的微卫星状态”相关研究依据那一列里方便展示            
                    if table_target.row(m)[11].ctype == 2:
                        RefPMID = "PMID:"+str(int(table_target.row(m)[11].value))+")"
                        PMID_for_ref=int(table_target.row(m)[11].value)
                    ##判断数据库第5个工作表Targeted的第12列PMID号如果不为整数,则不取整，而是将PMID转化为str然后在左边加PMID:,右边加括号，为了在表格“五、相关用药信息 ：  免疫药物相关的微卫星状态”相关研究依据那一列里方便展示
                    else:
                        RefPMID = "PMID:"+str(table_target.row(m)[11].value)+")"
                        PMID_for_ref=table_target.row(m)[11].value



                RefPMID_list.append(RefPMID)
                #Author=table_target.row(m)[10].value
                Part_author_list.append(Author)
                Author_list.append(Author)
                Part_PMID_list.append(PMID_for_ref)#用于后面生成6.3参考引文

        add_new['drug_list_table']=drug_list
        add_new['drug_number'] = len(drug_list)
        add_new['Clinical_Descrip_table']=ClinicalDescription_list
        add_new['RefPMID_table']=RefPMID_list
        add_new['Author_table']=Author_list

                #print(d_drug)
                
        add_new["Mutation_type"]=mutation_type
       
        d1['Fifth_msi_table'].append(add_new)

    f1.close()
    return d1,Part_PMID_list
Fifth_msi_Table_Dict,part_pmid_msi_list = test_msi_table(msi_result_file,db_file)
#print(Fifth_msi_Table_Dict)
#print(part_pmid_msi_list)
context.update(Fifth_msi_Table_Dict) 
############################################################################################################################################################################

###########################################################################第六部分，6.3参考引文
#将前面三部分生成的PMID合并到一起用于生成6.3参考引文
all_pmid_list = []
all_pmid_list.extend(part_PMID_target_list)
all_pmid_list.extend(part_pmid_chemo_list)
all_pmid_list.extend(part_pmid_msi_list)

#print(all_pmid_list)
#print(part_PMID_target_list)
#print(len(all_pmid_list))
#将所有引文去重(通过set()实现去重）后存入列表
uniq_pmid_list=list(set(all_pmid_list))
#判断如果去重后的PMID列表里有空值，则把空值去掉
if '' in uniq_pmid_list:
    uniq_pmid_list.remove('')
#print(uniq_pmid_list)
#print(len(uniq_pmid_list))



##通过reference函数读入1093行生成的uniq_pmid_list,db_file（例如：S001报告生成数据库_20200117v1.8.3.xlsx）实现
def reference(filein1,db_name):
    #db_file_name用于接收数据库文件名字db_name=db_file，例如：S001报告生成数据库_20200117v1.8.3.xlsx
    db_file_name=db_name
    #定义一个字典d1,键名为Sixth_ref_table，值为一个空列表[],这个字典的键名Sixth_ref_table在基因检测报告模板（例如：template_20191224_with_msi.docx）里需要用到：6.3参考引文{%p for a in Sixth_ref_table %}里的Sixth_ref_table即为此处定义而来。
    d1 = { 'Sixth_ref_table' : [] }
    #用xlrd读入数据库文件db_file_name=db_name，例如：S001报告生成数据库_20200117v1.8.3.xlsx，存到data里
    data = xlrd.open_workbook(db_file_name)
    table = data.sheet_by_index(7)   #Ref工作表#数据库文件的第8个工作表Ref的内容存到table里
    nrows = table.nrows#数据库文件的第7个工作表Ref的行数存到nrows里
    #f1读入所有去重后的PMID列表filein1=uniq_pmid_list
    f1=filein1
    #print(type(f1))
    num=0
    #遍历去重后的每一个PMID号
    for i in f1:
        
        add_new = {}
        ####遍历数据库第8个工作表Ref的除第一行外的所有行       
        for m in range(1,nrows):
            ##判断数据库第8个工作表Ref的第1列PMID号如果为整数(ctype==2),则取整,如6789345
            if table.row(m)[0].ctype == 2:
                RefPMID=int(table.row(m)[0].value)
            ##判断数据库第8个工作表Ref的第1列PMID号如果不为整数,则不取整，而是保持原值，如NSCLC
            else:
                RefPMID=table.row(m)[0].value
            #判断去重后的每一个PMID号如果等于 判断数据库第8个工作表Ref的第1列的PMID号   
            if i == RefPMID:
            
                add_new["Ref_Number"] = str(num+1)+'.'
                num=num+1

                add_new["Ref_content"] = table.row(m)[2].value
        d1['Sixth_ref_table'].append(add_new)

    return d1
Sixth_ref_table_dict = reference(uniq_pmid_list,db_file)
context.update(Sixth_ref_table_dict) 
#(Sixth_ref_table_dict)
#################################6.4自动换行
page_break_dict={'page_break': RichText('\f')}
context.update(page_break_dict) 
############################################################################################################################################################################
#################################################################################################
doc.render(context)
#最后输出的报告文件名命名规则为“检测者姓名”+“样本编号”.docx
doc.save(basic_information_dict['PATIENT_NAME']+basic_information_dict['SAMPLE_NUMBER']+".docx")


