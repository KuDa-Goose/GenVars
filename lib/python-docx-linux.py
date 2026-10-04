import argparse
import os,sys
import re
from docx import Document
from docx.shared import Pt
from docx.shared import Inches
from docx.oxml.ns import qn 
from docx.enum.text import WD_ALIGN_PARAGRAPH


if __name__ == "__main__":

    Help = """USAGE: python % python-docx.py % -p patient_file -r snp_indels_result -f fusion_result -g variants_file -d drug_file -o out_directory """

    parser = argparse.ArgumentParser(description = Help)

    parser.add_argument('-p', '--patient', action = "store", required = True, help = "<input file> Patient information file name")
    parser.add_argument('-r', '--result', action = "store", required = True, help = "<input file> SNP and INDELS mutation result file name")
    parser.add_argument('-f', '--fusion', action = "store", required = True, help = "<input file> Fusion result file name")
    parser.add_argument('-g', '--variants', action = "store", required = True, help = "<input file> Gene variants information file name")
    parser.add_argument('-d', '--drug', action = "store", required = True, help = "<input file> Variants-Drug information file name")
    parser.add_argument('-o', '--out', action = "store", required = True, help = "<out directory> Output directory")
    parser.add_argument('-v', '--version', action="version", version="%(python-docx)s 0.5.0.1")

    args = parser.parse_args()

    pat_in = args.patient
    test_result = args.result
    fusion = args.fusion
    gene_var = args.variants
    drug_ann = args.drug
    out = args.out

banner_dir = sys.path[0] #或banner_dir = sys.argv[0] ###提取当前被执行脚本路径

dict_P = {}
Sample = 'Sample000'
Patient = 'Sample000\tpatient\t男\tGeno00000000\t00000000\t医院\t2017. 01. 01\t2017. 01. 02\tcfDNA\t血液\tSABEL'
dict_P[Sample] = Patient
Pat_in = open(pat_in, "r")
num_d =0
for line in Pat_in:
    line = line.strip("\n")
    lines = line.split("\t")
    if lines[0] in ["Sample"]:
        continue
    else:
        dict_P[lines[0]] = line
        num_d += 1
Pat_in.close()
if num_d >= 1:
    del dict_P['Sample000']

Gene_var = open(gene_var, "r")
dict_Gf = {}
dict_Ge = {}
for line in Gene_var:
    line = line.strip("\n")
    lines = line.split("\t")
    if lines[0] in ["Gene"]:
        continue
    else:
        if lines[7] in ["fusion"]:
            keyf = lines[0] + "-" + lines[5]
            dict_Gf[keyf] = line
        else:
            key = lines[0] + lines[5]
            dict_Ge[key] = line
Gene_var.close()

Test_result = open(test_result,"r")
for line in Test_result:
    lines = line.strip("\n").split("\t")
    if lines[0] in ["Sample"]:
        name_SI = line
    elif lines[0] in dict_P:
        patient_in = dict_P[lines[0]].split("\t")
        outname = patient_in[3] + "-" + patient_in[1] + "-" + patient_in[0]

        document = Document()

        #首页#
        Head = document.add_paragraph(u'')
                                  
        run = Head.add_run(u'\n\n\t\t\t\t肿瘤检测报告\n\n\n\n') 
        run.font.size = Pt(26)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True  #加粗
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
 
        document.add_picture(banner_dir + '/banner1.jpg',width=Inches(6.25))
        document.add_paragraph('\n\n\n\n\n')

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'\t\t上海格诺生物科技有限公司')
        run.font.size = Pt(24)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        document.add_page_break()

        #第二页#
        document.add_paragraph('\n\n\n')
        Head = document.add_paragraph(u'')
        run = Head.add_run(u'\t\t肿瘤个体化诊疗检测报告\n\n\n\n\n\n\n\n\n')
        run.font.size = Pt(26)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True  #加粗
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        run = Head.add_run(u'\t\t  姓\t名: ' + patient_in[1] + '\n')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True 

        run = Head.add_run(u'\t\t  性\t别: ' + patient_in[2] + '\n')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True  

        run = Head.add_run(u'\t\t  样本来源: ' + patient_in[5] + '\n')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True  

        run = Head.add_run(u'\t\t  采样时间: ' + patient_in[6] + '\n')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True 

        run = Head.add_run(u'\t\t  报告编号: ' + patient_in[3] + '\n')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True  

        run = Head.add_run(u'\t\t  报告时间: ' + patient_in[7] + '\n')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True 
        document.add_page_break()


        #第三页###
        paragraph = document.add_paragraph(u'')
        head2 = paragraph.add_run(u'患者信息')
        head2.font.size = Pt(20)
        head2.font.name=u'宋体'
        #head2.font.underline = True
        head2.font.bold = True 
        r = head2._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        table1 = document.add_table(rows=7, cols=4, style='LightShading-Accent1')
        table1.autofit = False
        table1.columns[0].width = Inches(1.2)
        table1.columns[1].width = Inches(1.85)
        table1.columns[2].width = Inches(1.2)
        table1.columns[3].width = Inches(1.8)

        hdr_cells=table1.rows[0].cells
        hdr_cells[0].text=u'姓    名'
        hdr_cells[1].text= patient_in[1]
        hdr_cells[2].text=u'患者  ID'
        hdr_cells[3].text= patient_in[4]

        hdr_cells = table1.rows[1].cells
        hdr_cells[0].text = ''
        hdr_cells[1].text = ''
        hdr_cells[2].text = ''
        hdr_cells[3].text = ''

        hdr_cells = table1.rows[2].cells
        hdr_cells[0].text = u'采样时间'
        hdr_cells[1].text = patient_in[6]
        hdr_cells[2].text = u'样本类型'
        hdr_cells[3].text = patient_in[8]

        hdr_cells = table1.rows[3].cells
        hdr_cells[0].text = ''
        hdr_cells[1].text = ''
        hdr_cells[2].text = ''
        hdr_cells[3].text = ''

        hdr_cells = table1.rows[4].cells
        hdr_cells[0].text = u'采样方式'
        hdr_cells[1].text = patient_in[9]
        hdr_cells[2].text = u'检测方法'
        hdr_cells[3].text = patient_in[10]

        hdr_cells = table1.rows[5].cells
        hdr_cells[0].text = ''
        hdr_cells[1].text = ''
        hdr_cells[2].text = ''
        hdr_cells[3].text = ''

        hdr_cells = table1.rows[6].cells
        hdr_cells[0].text = u'样品编号'
        hdr_cells[1].text = patient_in[0]
        hdr_cells[2].text = u'报告编号'
        hdr_cells[3].text = patient_in[3]

        table1.style.font.name = u'宋体'
        table1.style.font.size = Pt(16)  
        table1.style._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体') 

        document.add_paragraph('\n\n')
        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'技术简介\n')
        run.font.size = Pt(20)
        run.font.name=u'宋体'
        run.font.bold = True 
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph_format = paragraph.paragraph_format
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph_format.first_line_indent = Inches(0.5)
        run = paragraph.add_run('高通量测序（High-Throughput Sequencing）又名下一代测序（Next Generation Sequening，NGS），是相对于传统的桑格测序（Sanger Sequencing）而言的。个体化用药指导和肿瘤风险评估成为二代测序中肿瘤临床应用的两大领域。靶向治疗现如今已经成为肿瘤治疗的首要手段，也是二代测序在肿瘤临床中的主要应用领域。目前，针对主要癌种的主要靶向相关基因检测，很多医院病理科均已常规开展。常规的检测项目有一定局限性，使用高通量测序能够进行多基因检测，寻找更多靶向治疗的机会。二代测序在遗传病检测、疑难杂症研究、妇婴生育保健、病源微生物等多个领域均有应用。\n    格诺生物是“精准医疗”领域里致力于肿瘤诊断技术创新的先行者，旗下涉及多种肿瘤诊断试剂的研发、生产、销售、临床检测服务、肿瘤云数据平台等业务。格诺生物Oncoplorare基于NGS技术，检测多个与肺癌发生密切相关的基因突变位点。')
        run.font.size = Pt(14)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        document.add_page_break()

       #snp_indels检测结果提取
        name_si = name_SI.split("\t")
        name_range = range(1,len(lines),3)
        dict_si = {}
        name = []
        for i in name_range:
            if lines[i+2] != '0':
                si_AF = re.search(r'^(\d+.*\d)%',lines[i+2])
                AFs = si_AF.group(1)
                AFs = str(AFs)
                AF = AFs.split("%")
                if (int(lines[i]) + int(lines[i+1]))>= 1000 and float(AF[0]) >= 0.2:
                    name_AA = name_si[i+2].split("_")
                    name.append(name_AA[0] + name_AA[1])
                    key = name_AA[0] + name_AA[1]
                    dict_si[key] = AF[0]
        #fusion检测结果提取#
        fusion_s = []
        dict_f ={}
        fusion_S = open(fusion,"r")
        for linef in fusion_S:
            lines_f = linef.strip("\n").split("\t")
            if lines[0] == lines_f[0]:
                linef = linef.strip("\n")
                fusion_s.append(linef)
                dict_f[linef[1]] = 1
        fusion_S.close()

        #snp_indels和fusuion均检测出来时，进行以下处理：
        if len(name) >=1 and len(fusion_s) >=1:
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检测结果--基因变异')
            run.font.size = Pt(20)
            run.font.name=u'宋体'
            run.font.bold = True 
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检出基因变异')
            run.font.size = Pt(18)
            run.font.name=u'宋体'
            run.font.bold = True 
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            table2 = document.add_table(rows=(len(name) + 1), cols=5, style='LightShading-Accent1')
            table2.autofit = False
            table2.columns[0].width = Inches(0.65)
            table2.columns[1].width = Inches(1.3)
            table2.columns[2].width = Inches(0.95)
            table2.columns[3].width = Inches(0.95)
            table2.columns[4].width = Inches(2.25)
            hdr_cells = table2.rows[0].cells
            hdr_cells[0].text = u'基因'
            hdr_cells[1].text = u'氨基酸突变'
            hdr_cells[2].text = u'突变频率'
            hdr_cells[3].text = u'临床影响'
            hdr_cells[4].text = u'临床表现'
            for i in range(0, len(name)):
                if name[i] in dict_Ge:
                    si_var = dict_Ge[name[i]].split("\t")
                    hdr_cells = table2.rows[i+1].cells
                    hdr_cells[0].text = si_var[0]
                    hdr_cells[1].text = si_var[9]
                    hdr_cells[2].text = str(dict_si[(si_var[0] + si_var[5])]) + "%"
                    hdr_cells[3].text = si_var[11]
                    hdr_cells[4].text = si_var[8]
            table2.style.font.name = u'宋体'
            table2.style.font.size = Pt(14)  
            table2.style._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体') 

            document.add_paragraph('\n')
            table3 = document.add_table(rows=(len(fusion_s) + 1), cols=5, style='LightShading-Accent1')
            table3.autofit = False
            table3.columns[0].width = Inches(0.95)
            table3.columns[1].width = Inches(1.6)
            table3.columns[2].width = Inches(0.95)
            table3.columns[3].width = Inches(0.95)
            table3.columns[4].width = Inches(1.65)
            hdr_cells = table3.rows[0].cells
            hdr_cells[0].text = u'融合基因'
            hdr_cells[1].text = u'融合位点'
            hdr_cells[2].text = u'融合比例'
            hdr_cells[3].text = u'临床影响'
            hdr_cells[4].text = u'临床表现'
            for i in range(0, len(fusion_s)):
                line_f = fusion_s[i].split("\t")
                if line_f[1] in dict_Gf:
                    f_var = dict_Gf[line_f[1]].split("\t")
                    hdr_cells = table3.rows[i+1].cells
                    hdr_cells[0].text = line_f[1]
                    hdr_cells[1].text = line_f[2]
                    hdr_cells[2].text = str(line_f[5]) + "%"
                    hdr_cells[3].text = f_var[11]
                    hdr_cells[4].text = f_var[8]
            table3.style.font.name = u'宋体'
            table3.style.font.size = Pt(14)
            table3.style._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'ACMG变异注释五级术语系统：致病的、可能致病的、意义不明确的、可能良性的、良性的.')
            run.font.size = Pt(12)
            run.font.name=u'宋体'
            r = run._element
#            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'\n用药建议')
            run.font.size = Pt(18)
            run.font.name=u'宋体'
            r = run._element
            run.font.bold = True 
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'    潜在靶向药\n\n\n\n    可能的耐药\n\n\n')
            run.font.size = Pt(14)
            run.font.name=u'宋体'
            r = run._element
            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            document.add_page_break()

                
            for i in range(0,len(name)):
                if name[i] in dict_Ge:
                    si_var = dict_Ge[name[i]].split("\t")
                    num_d = 0
                    drugs =[]
                    Drug_ann = open(drug_ann,"r")
                    for line1 in Drug_ann:
                        line1 = line1.strip("\n")
                        line1s = line1.split("\t")
                        if line1s[0] in ["Gene"]:
                            continue
                        else:
                            value = line1s[10] + "\t" + line1s[13] + "\t" + line1s[17] + "\t" + line1s[18]
                            if name[i] == line1s[0] + line1s[5]:
                                drugs.append(line1)
                                num_d += 1
                    Drug_ann.close()

                    paragraph = document.add_paragraph(u'')
                    run = paragraph.add_run(si_var[0] + " " + si_var[9] + u'靶向药物')
                    run.font.size = Pt(14)
                    run.font.name=u'宋体'
                    r = run._element
                    run.font.bold = True 
                    r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
                    table4 = document.add_table(rows=(num_d + 1), cols=4, style = 'Table Grid')
                    table4.autofit = False
                    table4.columns[0].width = Inches(1.4)
                    table4.columns[1].width = Inches(1)
                    table4.columns[2].width = Inches(1.85)
                    table4.columns[3].width = Inches(1.8)
                    hdr_cells = table4.rows[0].cells
                    hdr_cells[0].text = 'Drug'
                    hdr_cells[1].text = 'Evidence'
                    hdr_cells[2].text = 'Indication'
                    hdr_cells[3].text = 'Clinical trials'
                    for j in range(0,len(drugs)):
                        drug = drugs[j].split("\t")
                        hdr_cells = table4.rows[j+1].cells
                        hdr_cells[0].text = drug[10]
                        hdr_cells[1].text = drug[13]
                        hdr_cells[2].text = drug[17]
                        hdr_cells[3].text = drug[18]
                    paragraph = document.add_paragraph('')
                    run = paragraph.add_run('Notes: Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.')
                    run.font.size = Pt(12)
                    document.add_page_break()
            for i in range(0,len(fusion_s)):
                linef = fusion_s[i].split("\t")
                if linef[1] in dict_Gf:
                    f_var = dict_Gf[linef[1]].split("\t")
                    num_d = 0
                    drugs =[]
                    Drug_ann = open(drug_ann,"r")
                    for line1 in Drug_ann:
                        line1 = line1.strip("\n")
                        line1s = line1.split("\t")
                        if line1s[0] in ["Gene"]:
                            continue
                        else:
                            value = line1s[10] + "\t" + line1s[13] + "\t" + line1s[17] + "\t" + line1s[18]
                            if linef[1] == line1s[0] + "-" + line1s[5]:
                                drugs.append(line1)
                                num_d += 1
                    Drug_ann.close()

                    paragraph = document.add_paragraph(u'')
                    run = paragraph.add_run(linef[1] + u'靶向药物')
                    run.font.size = Pt(14)
                    run.font.name=u'宋体'
                    r = run._element
                    run.font.bold = True
                    r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
                    table4 = document.add_table(rows=(num_d + 1), cols=4, style = 'Table Grid')
                    table4.autofit = False
                    table4.columns[0].width = Inches(1.4)
                    table4.columns[1].width = Inches(1)
                    table4.columns[2].width = Inches(1.85)
                    table4.columns[3].width = Inches(1.8)
                    hdr_cells = table4.rows[0].cells
                    hdr_cells[0].text = 'Drug'
                    hdr_cells[1].text = 'Evidence'
                    hdr_cells[2].text = 'Indication'
                    hdr_cells[3].text = 'Clinical trials'
                    for j in range(0,len(drugs)):
                        drug = drugs[j].split("\t")
                        hdr_cells = table4.rows[j+1].cells
                        hdr_cells[0].text = drug[10]
                        hdr_cells[1].text = drug[13]
                        hdr_cells[2].text = drug[17]
                        hdr_cells[3].text = drug[18]
                    paragraph = document.add_paragraph('')
                    run = paragraph.add_run('Notes: Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.')
                    run.font.size = Pt(12)
                    document.add_page_break()

        #若仅检测出snp_indels，则进行以下处理：
        elif len(name) >=1 and len(fusion_s) < 1:
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检测结果--基因变异')
            run.font.size = Pt(20)
            run.font.name=u'宋体'
            run.font.bold = True
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检出基因变异')
            run.font.size = Pt(18)
            run.font.name=u'宋体'
            run.font.bold = True
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            table2 = document.add_table(rows=(len(name) + 1), cols=5, style='LightShading-Accent1')
            table2.autofit = False
            table2.columns[0].width = Inches(0.65)
            table2.columns[1].width = Inches(1.3)
            table2.columns[2].width = Inches(0.95)
            table2.columns[3].width = Inches(0.95)
            table2.columns[4].width = Inches(2.25)
            hdr_cells = table2.rows[0].cells
            hdr_cells[0].text = u'基因'
            hdr_cells[1].text = u'氨基酸突变'
            hdr_cells[2].text = u'突变频率'
            hdr_cells[3].text = u'临床影响'
            hdr_cells[4].text = u'临床表现'
            for i in range(0, len(name)):
                if name[i] in dict_Ge:
                    si_var = dict_Ge[name[i]].split("\t")
                    hdr_cells = table2.rows[i+1].cells
                    hdr_cells[0].text = si_var[0]
                    hdr_cells[1].text = si_var[9]
                    hdr_cells[2].text = str(dict_si[(si_var[0] + si_var[5])]) + "%"
                    hdr_cells[3].text = si_var[11]
                    hdr_cells[4].text = si_var[8]
            table2.style.font.name = u'宋体'
            table2.style.font.size = Pt(14)
            table2.style._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'ACMG变异注释五级术语系统：致病的、可能致病的、意义不明确的、可能良性的、良性的.')
            run.font.size = Pt(12)
            run.font.name=u'宋体'
            r = run._element
#            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'\n用药建议')
            run.font.size = Pt(18)
            run.font.name=u'宋体'
            r = run._element
            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'    潜在靶向药\n\n\n\n    可能的耐药\n\n\n')
            run.font.size = Pt(14)
            run.font.name=u'宋体'
            r = run._element
            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            document.add_page_break()

            for i in range(0,len(name)):
                if name[i] in dict_Ge:
                    si_var = dict_Ge[name[i]].split("\t")
                    num_d = 0
                    drugs =[]
                    Drug_ann = open(drug_ann,"r")
                    for line1 in Drug_ann:
                        line1 = line1.strip("\n")
                        line1s = line1.split("\t")
                        if line1s[0] in ["Gene"]:
                            continue
                        else:
                            value = line1s[10] + "\t" + line1s[13] + "\t" + line1s[17] + "\t" + line1s[18]
                            if name[i] == line1s[0] + line1s[5]:
                                drugs.append(line1)
                                num_d += 1
                    Drug_ann.close()
                    paragraph = document.add_paragraph(u'')
                    run = paragraph.add_run(si_var[0] + " " + si_var[9] + u'靶向药物')
                    run.font.size = Pt(14)
                    run.font.name=u'宋体'
                    r = run._element
                    run.font.bold = True
                    r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
                    table4 = document.add_table(rows=(num_d + 1), cols=4, style = 'Table Grid')
                    table4.autofit = False
                    table4.columns[0].width = Inches(1.4)
                    table4.columns[1].width = Inches(1)
                    table4.columns[2].width = Inches(1.85)
                    table4.columns[3].width = Inches(1.8)
                    hdr_cells = table4.rows[0].cells
                    hdr_cells[0].text = 'Drug'
                    hdr_cells[1].text = 'Evidence'
                    hdr_cells[2].text = 'Indication'
                    hdr_cells[3].text = 'Clinical trials'
                    for j in range(0,len(drugs)):
                        drug = drugs[j].split("\t")
                        hdr_cells = table4.rows[j+1].cells
                        hdr_cells[0].text = drug[10]
                        hdr_cells[1].text = drug[13]
                        hdr_cells[2].text = drug[17]
                        hdr_cells[3].text = drug[18]
                    paragraph = document.add_paragraph('')
                    run = paragraph.add_run('Notes: Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.')
                    run.font.size = Pt(12)
                    document.add_page_break()

        #若仅检测出fusions，则进行以下处理：
        elif len(name) < 1 and len(fusion_s) >= 1:
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检测结果--基因变异')
            run.font.size = Pt(20)
            run.font.name=u'宋体'
            run.font.bold = True
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检出基因变异')
            run.font.size = Pt(18)
            run.font.name=u'宋体'
            run.font.bold = True
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            
            table3 = document.add_table(rows=(len(fusion_s) + 1), cols=5, style='LightShading-Accent1')
            table3.autofit = False
            table3.columns[0].width = Inches(0.95)
            table3.columns[1].width = Inches(1.6)
            table3.columns[2].width = Inches(0.95)
            table3.columns[3].width = Inches(0.95)
            table3.columns[4].width = Inches(1.65)
            hdr_cells = table3.rows[0].cells
            hdr_cells[0].text = u'融合基因'
            hdr_cells[1].text = u'融合位点'
            hdr_cells[2].text = u'融合比例'
            hdr_cells[3].text = u'临床影响'
            hdr_cells[4].text = u'临床表现'
            for i in range(0, len(fusion_s)):
                line_f = fusion_s[i].split("\t")
                if line_f[1] in dict_Gf:
                    f_var = dict_Gf[line_f[1]].split("\t")
                    hdr_cells = table3.rows[i+1].cells
                    hdr_cells[0].text = line_f[1]
                    hdr_cells[1].text = line_f[2]
                    hdr_cells[2].text = str(line_f[5]) + "%"
                    hdr_cells[3].text = f_var[11]
                    hdr_cells[4].text = f_var[8]
            table3.style.font.name = u'宋体'
            table3.style.font.size = Pt(14)
            table3.style._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'ACMG变异注释五级术语系统：致病的、可能致病的、意义不明确的、可能良性的、良性的.')
            run.font.size = Pt(12)
            run.font.name=u'宋体'
            r = run._element
#            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'\n用药建议')
            run.font.size = Pt(18)
            run.font.name=u'宋体'
            r = run._element
            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'    潜在靶向药\n\n\n\n    可能的耐药\n\n\n')
            run.font.size = Pt(14)
            run.font.name=u'宋体'
            r = run._element
            run.font.bold = True
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            document.add_page_break()

            for i in range(0,len(fusion_s)):
                linef = fusion_s[i].split("\t")
                if linef[1] in dict_Gf:
                    f_var = dict_Gf[linef[1]].split("\t")
                    num_d = 0
                    drugs =[]
                    Drug_ann = open(drug_ann,"r")
                    for line1 in Drug_ann:
                        line1 = line1.strip("\n")
                        line1s = line1.split("\t")
                        if line1s[0] in ["Gene"]:
                            continue
                        else:
                            value = line1s[10] + "\t" + line1s[13] + "\t" + line1s[17] + "\t" + line1s[18]
                            if linef[1] == line1s[0] + "-" + line1s[5]:
                                drugs.append(line1)
                                num_d += 1
                    Drug_ann.close()

                    paragraph = document.add_paragraph(u'')
                    run = paragraph.add_run(linef[1] + u'靶向药物')
                    run.font.size = Pt(14)
                    run.font.name=u'宋体'
                    r = run._element
                    run.font.bold = True
                    r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
                    table4 = document.add_table(rows=(num_d + 1), cols=4, style = 'Table Grid')
                    table4.autofit = False
                    table4.columns[0].width = Inches(1.4)
                    table4.columns[1].width = Inches(1)
                    table4.columns[2].width = Inches(1.85)
                    table4.columns[3].width = Inches(1.8)
                    hdr_cells = table4.rows[0].cells
                    hdr_cells[0].text = 'Drug'
                    hdr_cells[1].text = 'Evidence'
                    hdr_cells[2].text = 'Indication'
                    hdr_cells[3].text = 'Clinical trials'
                    for j in range(0,len(drugs)):
                        drug = drugs[j].split("\t")
                        hdr_cells = table4.rows[j+1].cells
                        hdr_cells[0].text = drug[10]
                        hdr_cells[1].text = drug[13]
                        hdr_cells[2].text = drug[17]
                        hdr_cells[3].text = drug[18]
                    paragraph = document.add_paragraph('')
                    run = paragraph.add_run('Notes: Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.')
                    run.font.size = Pt(12)
                    document.add_page_break()

        #若未检测到突变，则进行以下处理：
        else:
            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检测结果--基因变异')
            run.font.size = Pt(20)
            run.font.name=u'宋体'
            run.font.bold = True
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

            paragraph = document.add_paragraph(u'')
            run = paragraph.add_run(u'检出基因变异\n\n\n\n\t未发现基因突变')
            run.font.size = Pt(18)
            run.font.name=u'宋体'
            run.font.bold = True
            r = run._element
            r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
            document.add_page_break()

        #附录#
        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'附录')
        run.font.size = Pt(20)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True 
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'1. 检测突变基因简介')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True 
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'1.1 ALK')
        run.font.size = Pt(16)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True 
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph_format = paragraph.paragraph_format
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph_format.first_line_indent = Inches(0.5)
        run = paragraph.add_run(u'ALK是一种间变性淋巴瘤激酶（Anaplastic Lymphoma kinase, ALK），肺癌中ALK变异主要为ALK基因发生重排与其他基因融合。其中，EML4-ALK（棘皮动物微管结合蛋白样4-间变性淋巴瘤激酶）融合基因变异是其主要类型，约占所有NSCLC的5%左右[12]。肺癌中与ALK基因融合的其他基因还包括TFG、KIF5B等。尽管ALK阳性的NSCLC在肺癌的比例很低，但在我国每年新发病例数仍然接近35000例[3]。因此，准确鉴定出ALK重排阳性的NSCLC，并给予相应的治疗是需要的。针对ALK靶点的小分子抑制剂克唑替尼（Crizotinib）是一种ATP竞争性酪氨酸激酶抑制剂，可特异性靶向抑制ALK激酶，也可抑制c-MET和ROS1等信号通路[4]。Alectinib(艾乐替尼)和Ceritini(色瑞替尼)作为第二代酪氨酸激酶抑制剂，分别通过抑制间变性淋巴瘤酪氨酸激酶和ALK的自体磷酸化过程，来降低癌细胞的增值和生存能力[5]。')
        run.font.size = Pt(12)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[1] Soda M, Choi YL, Enomoto M et al. Identification of the transforming EML4-ALK fusion gene in non-small-cell lung cancer. Nature. 2007, 448:561566.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[2] Soda M, Takada S, Takeuchi K et al. A mouse model for EML4-ALK-positive lung cancer. Proc Natl Acad Sci USA.2008, 105:1989319897.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'[3] ')
        run.font.size = Pt(12)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run(u'全国肿瘤防治研究办公室/全国肿瘤登记中心/卫生部疾病预防控制局.2009 全国肿瘤登记年报. 北京:军事医学科学出版社.2010.')
        run.font.size = Pt(12)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph('')
        run = paragraph.add_run(u'[4] ')
        run.font.size = Pt(12)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run(u'国家卫生和计划生育委员会。原发性肺癌诊疗规范（2015年）.中华肿瘤杂志，2015，37：1-12.')
        run.font.size = Pt(12)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run(u'[5] NCCN Guidelines Version 2.2017, Non-small cell Lung cancer.\n')
        run.font.size = Pt(12)
        document.add_page_break()

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'1.2 BRAF')
        run.font.size = Pt(16)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph_format = paragraph.paragraph_format
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph_format.first_line_indent = Inches(0.5)
        run = paragraph.add_run(u'鼠类肉瘤病毒癌基因同源物B1（V-raf murine sarcoma viral oncogene homolog B1,BRAF）基因位于人第7号染色体上，其编码的一种丝氨酸/苏氨酸蛋白激酶位于EGFR信号通路下游，依赖KRAS-GTP活化，是RAS-RAF-MEK-ERK信号通路中的重要转导因子。在NSCLC中，BRAF突变多见于腺癌，主要发生在第11和15外显子，约50%的BRAF突变为第15外显子上的V600E突变（约占3%的NSCLC患者）[1-2]。该突变能够模拟T798和S601两个位点的磷酸化，从而导致BRAF的持续活化。不同于BRAF突变高发的黑色素瘤，NSCLC的BRAF突变有很大一部分为激酶活化域中的G469A突变（约40%）以及激酶结构域中的D594G突变（约10%）[3]。大部分情况下，BRAF突变不会与其他驱动突变如EGFR、KRAS基因突变同时发生[4]。然而研究表明，携带BRAF基因特定突变的患者对EGFR靶向药物治疗存在耐药性，是重要的检测靶标之一[5]。针对BRAF-V600E突变，维罗非尼（Vemurafenib，商品名：Zelboraf）和达拉非尼（Dabrafenib，商品名：Tafinlar）两种靶向药可特异性抑制V600E突变细胞的ERK磷酸化，从而阻断其下游通路的信号转导，达到抗肿瘤效果。其中，Dabrafenib 已获FDA批准与曲美替尼（Trametinib，商品名：Mekinist）联合使用治疗携带BRAF-V600E突变的转移性NSCLC患者[6]。Dabrafenib和Trametinib分别靶向MAPK信号通路中的不同激酶（BRAF和MEK），临床研究显示联合使用可增加抗肿瘤效果[7]。而Vemurafenib目前仅被批准用于治疗黑色素瘤患者[5]。')
        run.font.size = Pt(12)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[1] Gou LY, Wu YL. Prevalence of driver mutations in non-small-cell lung cancers in the People\'s Republic of China. Lung Cancer (Auckl) 2014; 5: 1-9.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[2] Zheng D, Wang R, Ye T, et al. MET exon 14 skipping defines a unique molecular class of non-small cell lung cancer. Oncotarget 2016, 7: 41691-41702.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[3] Ji H, Wang Z, Perera SA, et al. Mutations in BRAF and KRAS converge on activation of the mitogen-activated protein kinase pathway in lung cancer mouse models. Cancer Res,2007, 67: 4933-4939.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[4] Paik PK, Arcila ME, Fara M, et al. Clinical characteristics of patients with lung adenocarcinomas harboring BRAF mutations. J Clin Oncol 2011,29: 2046-2051.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[5] Di Nicolantonio F, Martini M, Molinari F, et al. Wild-type BRAF is required for response to panitumumab or cetuximab in metastatic colorectal cancer. J Clin Oncol 2008,26: 5705-5712.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[6] NCCN Guidelines Version 8.2017, Non-Small Cell Lung Cancer.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[7] Planchard D, Besse B, Groen HJM, et al. Dabrafenib plus trametinib in patients with previously treated BRAF(V600E)-mutant metastatic non-small cell lung cancer: an open-label, multicentre phase 2 trial. Lancet Oncol 2016, 17: 984-993.')
        run.font.size = Pt(12)
        document.add_page_break()

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'1.3 EGFR')
        run.font.size = Pt(16)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
  
        paragraph = document.add_paragraph(u'')
        paragraph_format = paragraph.paragraph_format
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph_format.first_line_indent = Inches(0.5)
        run = paragraph.add_run(u'表皮生长因子受体（Epidermal growth factor receptor, EGFR）信号通路在细胞生长、增殖和分化中发挥着重要作用。EGFR突变将导致EGFR磷酸化，并持续激活其下游信号，导致肿瘤生长。EGFR突变主要发生于第18-21号外显子中，为EGFR的激酶域。在肺癌中，占90%的EGFR突变为第19外显子缺失突变及第21外显子L858R点突变[1]。上述两种突变是明确的敏感突变，提示肿瘤对EGFR靶向治疗敏感。然而，尽管EGFR靶向治疗可对突变患者产生良好的肿瘤应答，在经过9-13个月的治疗后，大部分患者会产生耐药，主要原因为EGFR第20外显子的T790M点突变，占继发耐药者中的约50%[2]。亚洲人群中，EGFR突变较西方国家发生率高，约占NSCLC患者的50%，因此检测EGFR突变以指导靶向治疗在我国尤其重要[3]。第一代吉非替尼（Gefitinib，商品名：易瑞沙Iressa）、厄洛替尼（Erlotinib，商品名：特罗凯Tarceva）和埃克替尼（Icotinib，商品名：凯美纳），以及第二代阿法替尼（Afatinib，商品名：Gilotrif）是经CFDA批准用于治疗EGFR敏感突变NSCLC患者的EGFR酪氨酸激酶抑制剂（Tyrosine kinase inhibitor，TKI）[4]。第一代EGFR-TKI通过竞争性抑制ATP与EGFR酪氨酸激酶的结合达到抗肿瘤效果；第二代EGFR-TKI不可逆地抑制EGFR酪氨酸激酶。而第三代奥希替尼（Osimertinib，商品名：Tagrisso）则能克服T790M耐药性，目前已获CFDA批准用于治疗经EGFR-TKI治疗后产生耐药的T790M阳性NSCLC患者。')
        run.font.size = Pt(12)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[1] Pao W, Miller VA. Epidermal growth factor receptor mutations, small-molecule kinase inhibitors, and non-small-cell lung cancer: current knowledge and future directions. J Clin Oncol 2005, 23: 2556-2568.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[2] Kobayashi S, Boggon TJ, Dayaram T, et al. EGFR mutation and resistance of non-small-cell lung cancer to gefitinib. N Engl J Med 2005, 352: 786-792.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[3] Gou LY, Wu YL. Prevalence of driver mutations in non-small-cell lung cancers in the People\'s Republic of China. Lung Cancer (Auckl) 2014, 5: 1-9.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph('')
        run = paragraph.add_run(u'[4] ')
        run.font.size = Pt(12)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run(u'中国临床肿瘤学会指南工作委员会. 中国临床肿瘤学会（CSCO）原发性肺癌诊疗指南2016.V1.')
        run.font.size = Pt(12)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
        document.add_page_break()

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'1.4 KRAS/NRAS')
        run.font.size = Pt(16)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph_format = paragraph.paragraph_format
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        paragraph_format.first_line_indent = Inches(0.5)
        run = paragraph.add_run(u'RAS家族是一种鼠类肉瘤病毒癌基因，主要包括KRAS（Kirsten rat sarcoma viral oncogene，又称p21）和NRAS（Neuroblastoma RAS viral oncogene），分别位于人第12和1号染色体上。RAS基因变异以点突变为主，其中KRAS突变多发生在第12密码子，NRAS突变多发生在第61密码子。这些突变改变编码Ras蛋白和GTP酶活化蛋白作用位点的氨基酸，导致Ras-GTP处于持续激活状态，在不依赖EGFR等上游生长因子激活的情况下活化RAS/MAPK信号通路，引起细胞的不可控增殖。在结直肠癌中，KRAS突变与抗EGFR单抗（Panitumumab和Cetuximab）较差的疗效相关，是指导靶向治疗的一种常规基因检测[1]。而在NSCLC中，KRAS突变多见于腺癌，但是亚洲人群较西方人群突变发生率较低，仅占约6%（NRAS突变约1%）[2]。目前尚无治疗肺癌的KRAS/NRAS靶向药物。体外细胞研究显示，MEK抑制剂（Selumetinib和Trametinib）或可能有效治疗NRAS突变的NSCLC[3]。不同于结直肠癌，KRAS突变与EGFR-TKI疗效的相关性仍未有一致定论。尽管大量回顾性研究指出KRAS突变与低EGFR-TKI反应率相关（0-5% vs 7-30%）[4]，但由于EGFR和KRAS突变很少同时存在，因此缺乏大规模前瞻性研究证实两者的关系。而且无论KRAS突变状态如何，野生型EGFR患者均与EGFR-TKI治疗的不良预后相关[5]，提示KRAS突变仅为EGFR-TKI耐药的其中一种模式，其指导意义尚不明确。')
        run.font.size = Pt(12)
        run.font.name=u'宋体'
        r = run._element
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[1] NCCN Guidelines Version 2.2017, Colon Cancer.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[2] Gou LY, Wu YL. Prevalence of driver mutations in non-small-cell lung cancers in the People\'s Republic of China. Lung Cancer (Auckl) 2014, 5: 1-9.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[3] Ohashi K, Sequist LV, Archila ME, et al. Characteristics of lung cancers harboring NRAS mutations. Clin Cancer Res 2013, 19: 2584-2591.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[4] Gregory J. Riely, Marc Ladanyi. KRAS mutations: an old oncogene becomes a new predictive biomarker. J Mol Diagn 2008, 10: 493-495.')
        run.font.size = Pt(12)

        paragraph = document.add_paragraph(u'')
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = paragraph.add_run('[5] Cheng L, Zhang S, Alexander R, et al. The landscape of EGFR pathways and personalized management of non-small-cell lung cancer. Future Oncol 2011, 7: 519-541.')
        run.font.size = Pt(12)
        document.add_page_break()

        paragraph = document.add_paragraph(u'')
        run = paragraph.add_run(u'2. NCCN临床指南：非小细胞肺癌(2017.V2)')
        run.font.size = Pt(18)
        run.font.name=u'宋体'
        r = run._element
        run.font.bold = True 
        r.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')

        table4 = document.add_table(rows=7, cols=3, style = 'Table Grid')
        table4.autofit = False
        table4.columns[0].width = Inches(1.2)
        table4.columns[1].width = Inches(2.45)
        table4.columns[2].width = Inches(2.4)

        hdr_cells = table4.rows[0].cells
        hdr_cells[0].text = u'突变基因'
        hdr_cells[1].text = u'突变位点'
        hdr_cells[2].text = u' 靶向药'

        hdr_cells = table4.rows[1].cells
        hdr_cells[0].text = '\nALK'
        hdr_cells[1].text = u'\n基因重排'
        hdr_cells[2].text = u'Crizotinib(克唑替尼)\nCeritinib(色瑞替尼)\nAlectinib(艾乐替尼)\nBrigatinib(布吉他滨)'

        hdr_cells = table4.rows[2].cells
        hdr_cells[0].text = '\nBRAF'
        hdr_cells[1].text = u'\nV600E'
        hdr_cells[2].text = u'vemurafenib(威罗菲尼)\ndabrafenib+trametinib(曲美替尼)'

        hdr_cells = table4.rows[3].cells
        hdr_cells[0].text = '\nEGFR'
        hdr_cells[1].text = u'\nL858R/L861Q/G719X/S768I/19del '
        hdr_cells[2].text = u'Erlotinib(厄洛替尼，特罗凯)\nAfatinib(阿法替尼)\nGefitinib(吉非替尼，易瑞沙)'

        hdr_cells = table4.rows[4].cells
        hdr_cells[0].text = 'EGFR'
        hdr_cells[1].text = u'T790M'
        hdr_cells[2].text = u'Osimertinib(奥斯替尼)'

        hdr_cells = table4.rows[5].cells
        hdr_cells[0].text = 'HER2 '
        hdr_cells[1].text = u''
        hdr_cells[2].text = u'Trastuzumab(曲妥珠单抗)\nAfatinib(阿法替尼)'

        hdr_cells = table4.rows[6].cells
        hdr_cells[0].text = 'MET'
        hdr_cells[1].text = u'高水平MET扩增或14号外显子跳跃突变'
        hdr_cells[2].text = u'Crizotinib(克唑替尼)'
        table4.style.font.name = u'宋体'
        table4.style.font.size = Pt(12)  
        table4.style._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体') 

        document.save(out + "/" + outname + '.docx')                                                                

