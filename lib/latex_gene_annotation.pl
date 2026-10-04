#!/usr/bin/perl
use warnings;
use strict;
use Getopt::Long;
use Cwd 'abs_path';

my $usage = <<USAGE_end;
Usage:
    perl $0 -p patient.file -r result -f fusion -g gene_Var -o out.dir -d drugs.file 
    
        -p <file name> patient information file name
        -r <file name> test result file name
        -f <file name> fusion result file name
        -g <file name> gene variants annotation file name
        -o <directory> the output path directory
        -d <file name> target annotation of gene mutation file name
        -h/help <bollean> Print help of current program
USAGE_end

# default parameter
my $pat_in  ;
my $test_result ;
my $fusion ;
my $gene_var ;
my $out ;
my $drug_ann ;
my $help;

# Get parameters
GetOptions(
    'p|patient-information=s' => \$pat_in,
    'r|test-result=s'         => \$test_result,
    'f|fusion-result=s'       => \$fusion,
    'g|gene-variants=s'       => \$gene_var,
    'o|output-directory=s'    => \$out,
    'd|drugs-annatation=s'    => \$drug_ann,
    'h|help'                  => \$help );
die "$usage" unless ($pat_in && $test_result && $gene_var && $out && $drug_ann);

if ($help){
    print $usage;
    exit;
}

my $jpg_path=abs_path($0);

my %hash=();
my %hash1=();
my %hash1f=();
my %hash2=();
my %hash3=();

my $test= "Sample000";
my $line= "Sample000\tpatient\t男\tGeno00000000\t00000000\t医院\t2017. 01. 01\t2017. 01. 02\tcfDNA\t血液\tSABEL";
$hash{$test}=$line;

open(IN,"$pat_in");
<IN>;
while(my $line=<IN>){
    chomp($line);
   # $line=~s/\s+/\t/g;
    my @line=split/\t/,$line;
    $hash{$line[0]}=$line;
    delete $hash{"Sample000"};
}
close IN;


open (IN,"$gene_var");
while(my $line1=<IN>){
    chomp($line1);
    my @line1=split/\t/,$line1;
    my $a=$line1[0].$line1[5];
    $hash1{$a}=$line1;
    my $b=$line1[0]."-"."$line1[5]";
    $hash1f{$b}=$line1;
    }
close IN;


open(IN,"$test_result");
my $snpname=<IN>;
chomp($snpname);
#print $snpname;
while(my $line3=<IN>){
    chomp($line3);
    $line3=~s/\s+/\t/g;    
    my @line3=split/\t/,$line3;
    #    print $line3[0]."\n";
     if ($hash{$line3[0]}){
        my $patient_information=$hash{$line3[0]};
   #     print $patient_information."\n";
        my @patient=split/\t/,$patient_information;
        my $outname=$patient[3]."-".$patient[1]."-".$patient[0].".tex";
   #     print $outname."\n";
        
        open(OUT,">$out/$outname");
        ########导言区
        print OUT "\%导言区\n";
        print OUT "\\documentclass[a4paper,12pt]{report}\n";
        print OUT "\\usepackage{CJK}\n";
        print OUT "\\usepackage{fancyhdr}\n";
        print OUT "\\usepackage{booktabs}\n";
        print OUT "\\usepackage{geometry}\n";
        print OUT "\\usepackage{longtable}\n";
        print OUT "\\usepackage{supertabular}\n";
        print OUT "\\usepackage{array}\n";
        print OUT "\\usepackage{graphicx}\n";
        print OUT "\\usepackage{color}\n";
        print OUT "\\usepackage{indentfirst}\n";
        print OUT "\\setlength{\\parindent}{2em}\n";
        print OUT "\\geometry{left=1.5cm,right=2.0cm,top=2.5cm,bottom=2.5cm}\n";
        print OUT "\\usepackage{multirow}\n";
        print OUT "\\usepackage{textcomp,booktabs}\n";
        print OUT "\\usepackage{colortbl}\n";
        print OUT "\\definecolor{mygray}{gray}{.9}\n";
        print OUT "\\usepackage{ragged2e}\n";
        print OUT "\n";
        print OUT "\n";
        print OUT "\n";


        ########开始报告
        print OUT "\%报告封面\n";
        print OUT "\\begin{document}\n";
        print OUT "\\begin{CJK*}{UTF8}{gbsn}\n";
        print OUT "\n";
        print OUT "\n";
        print OUT "\n";

        ########添加页眉
        print OUT "\%添加页眉\n";
        print OUT "\\pagestyle{fancy}\n";
        print OUT "\\rhead{ID:$patient[4]}\n";
        print OUT "\\lhead{\\includegraphics[scale=0.2]{logo.jpg}}\n";
        print OUT "\\renewcommand{\\headrulewidth}{0.4pt}\n";
        print OUT "\\headsep=25pt\n";
        print OUT "\n";
        print OUT "\n";
        print OUT "\n";
        
        ########报告封面
        print OUT "\%报告封面\n";
        print OUT "\\centering\n";
        print OUT "\\renewcommand{\\abstractname}{\\huge{肿瘤检测报告}}\n";
        print OUT "\\begin{abstract}\n";
        print OUT "\\vspace{4cm}\n";
        print OUT "\\begin{figure}[htbp]\n";
        print OUT "\\centering\n";
        print OUT "\\includegraphics[width=1.0\\textwidth]{banner1}\n";
        print OUT "\\end{figure}\n";
        print OUT "\\vspace{4cm}\n";
        print OUT "\\LARGE\n";
        print OUT "\上海格诺生物科技有限公司\n";
        print OUT "\\vspace{2cm}\n";
        print OUT "\\end{abstract}\n";
        print OUT "\n";
        print OUT "\n";
        print OUT "\n";

        ########报告首页--样品简介
        print OUT "\%报告首页\n";
        print OUT "\\section*{\\\\}\n";
        print OUT "\\section*{\\\\}\n";
        print OUT "\\section*{\\\\}\n";
        print OUT "\\centering\n";
        print OUT "\\section*{\\huge{\\\\肿瘤个体化诊疗检测报告}}\n";
        print OUT "\\vspace{8cm}\n";
        print OUT "\\linespread{2}\\selectfont\n";
        print OUT "\\large\n";
        print OUT "\\begin{tabular}{ccc}\n";
        print OUT "\\centering\n";

        ########读入患者信息
        print OUT "\&\\makebox[4em][s]{\\textbf{姓\\hspace{\\fill}名}}: &\\textbf{$patient[1]}\\\\\n";
        print OUT "\&\\makebox[4em][s]{\\textbf{性\\hspace{\\fill}别}}: &\\textbf{$patient[2]}\\\\\n";
        print OUT "\&\\textbf{报告编号}:&\\textbf{$patient[3]}\\\\\n";
        print OUT "\&\\textbf{样本来源}:&\\textbf{$patient[5]}\\\\\n";
        print OUT "\&\\textbf{采样时间}:&\\textbf{$patient[6]}\\\\\n";
        print OUT "\&\\textbf{报告时间}:&\\textbf{$patient[7]}\\\\\n";
        print OUT "\\end{tabular}\n";
        print OUT "\\pagebreak\n";
        print OUT "\n";
        print OUT "\n";
        print OUT "\n";
    
        ########报告第二页--患者信息
        print OUT "\%报告首页\n";
        print OUT "\\raggedright\n";
        print OUT "\\section*{患者信息}\n";
        print OUT "\\begin{tabular}{ll p{7cm}lp{3cm}p{4cm}}\n";
        print OUT "\\toprule[2pt]\n";
        print OUT "\&\\makebox[4em][s]{姓\\hspace{\\fill}名}&$patient[1] &\\makebox[4em][s]{患者\\hspace{\\fill}ID}&$patient[4]\\\\\n";
        print OUT "\&样本来源 &$patient[5] &样本类型 &$patient[8]\\\\\n";
        print OUT "\&采样时间 &$patient[6] &采样方式 &$patient[9]\\\\\n";
        print OUT "\&样品编号 &$patient[0] &实验方法 &$patient[10]\\\\\n";
        print OUT "\&报告时间 &$patient[7] &报告编号 &$patient[3]\\\\\n";
        print OUT "\\bottomrule[2pt]\n";
        print OUT "\\end{tabular}\n";
        print OUT "\n";
        print OUT "\n";
        print OUT "\n";

        ########报告第二页--格诺技术i简介
        print OUT "\%格诺技术简介\n";
        print OUT "\\raggedright\n";
        print OUT "\\linespread{2}\\selectfont\n";
        print OUT "\\vspace{0.5cm}\n";
        print OUT "\\setlength{\\parindent}{2em}\n";
        print OUT "\\section*{技术简介}\n";
        print OUT "\\justifying\n";
        print OUT "\\indent\n";
        print OUT "\\normalsize\n";
        print OUT "高通量测序（High-Throughput Sequencing）又名下一代测序（Next Generation Sequencing，NGS），是相对于传统的桑格测序（Sanger Sequencing）而言的。个体化用药指导和肿瘤风险评估成为二代测序中肿瘤临床应用的两大领域。靶向治疗现如今已经成为肿瘤治疗的首要手段，也是二代测序在肿瘤临床中的主要应用领域。目前，针对主要癌种的主要靶向相关基因检测，很多医院病理科均已常规开展。常规的检测项目有一定局>限性，使用高通量测序能够进行多基因检测，寻找更多靶向治疗的机会。二代测序在遗传病检测、疑难杂症研究、妇婴生育保健、病源微生物等多个领域均有应用。\\\\\n";
        print OUT "\\indent\n";
        print OUT "格诺生物是“精准医疗”领域里致力于肿瘤诊断技术创新的先行者，旗下涉及多种肿瘤诊断试剂的研发、生产、销售、临床检测服务、肿瘤云数据平台等业务。格诺生物\$\^{Oncoplorare}\$基于NGS技术，检测多个与肺癌发生密切相关的基因突变位点。\n";
        print OUT "\\pagebreak\n";
        print OUT "\n";
        print OUT "\n";
        
        my %hash4=();
        my @jud_line=split/\t/,$snpname;
        my @name=();
        for (my $i=1;$i<@jud_line;$i+=3){
            $line3[$i+2]=~ /(\d+.*\d)%/g;
             my $jud_f1=$1;
           #  print $jud_f1;
             if ($line3[$i] >= 1000 && $jud_f1 >=0.2){
                my @line4_name=split/\_/,$jud_line[$i+2];
                push @name,$line4_name[0].$line4_name[1];
                my $AF=$jud_f1."\\"."%";
                $hash4{$line4_name[0].$line4_name[1]}=$AF;
            }
        }

        ######fusion检测识别#####
        my @fusion=();
        open(INF,"$fusion"); 
        while(my $linef=<INF>){
            chomp($linef);
            my @linef=split/\t/,$linef;
            if ($line3[0] eq $linef[0]){
                push @fusion,$linef;
            }
        }
        close INF;

        my $judf=@fusion;
        my $jud=@name;
        if ($jud >= 1 && $judf>=1){
            #   print $jud."\n";
            ######检测结果--基因变异
            print OUT "\%检测结果--基因变异\n";
            print OUT "\\raggedright\n";
            print OUT "\\linespread{1.5}\\selectfont\n";
            print OUT "\\section*{检测结果小结}\n";
            print OUT "\\subsection*{检出基因变异}\n";
            print OUT "\\centering\n";
            print OUT "\\small\n";
            print OUT "\\begin{longtable}{l p{1cm}p{2.4cm}p{1.3cm}p{2.0cm}p{1cm}p{1.8cm}p{4cm}}\n";
            print OUT "\\toprule[2pt]\n";
            print OUT "\&\\large Gene &\\large Location&\\large CDs&\\large AA&\\large AF&\\large Type&\\large Conditions\\\\\n";
            print OUT "\\midrule[1pt]\n";

            for (my $j=0;$j<=@name;$j++){
                if($hash1{$name[$j]}){
                    if ($j%2 == 0){
                        print OUT "\\rowcolor{mygray}\n";
                    }
                    my @line2=split/\t/,$hash1{$name[$j]};
                    if ($line2[3]=~/>/){
                        my @Mut_cds=split/>/,$line2[3];
                        my $Mut_cds=$Mut_cds[0]."\$".">"."\$".$Mut_cds[1];
                        print OUT "\&$line2[0]&$line2[1]&$Mut_cds&$line2[5]&$hash4{$line2[0].$line2[5]}&$line2[7]&$line2[9]\\\\\n";
                    }else{
                        print OUT "\&$line2[0]&$line2[1]&$line2[3]&$line2[5]&$hash4{$line2[0].$line2[5]}&$line2[7]&$line2[9]\\\\\n";
                    }
                }
            }
            print OUT "\\bottomrule[2pt]\n";      
            print OUT "\\end{longtable}\n";

            
            print OUT "\\centering\n";
            print OUT "\\small\n";
            print OUT "\\begin{longtable}{l p{2.3cm}p{5cm}p{1.3cm}p{1.8cm}p{4cm}}\n";
            print OUT "\\toprule[2pt]\n";
            print OUT "\&\\large Gene &\\large Fusion Location &\\large Rate&\\large Type&\\large Conditions\\\\\n";
            print OUT "\\midrule[1pt]\n";

            my %hashf_drug=();
            my @fusion=();
            open(INF,"$fusion");
            while(my $linef=<INF>){
                chomp($linef);
                my @linef=split/\t/,$linef;
                if ($line3[0] eq $linef[0]){
                    push @fusion,$linef;
                    $hashf_drug{$linef[1]}=1;
                }
            }
            close INF;

            for (my $j=0;$j<=@fusion;$j++){
                my @linef=split/\t/,$fusion[$j];
    
                if($hash1f{$linef[1]}){
                    if ($j%2 == 0){
                        print OUT "\\rowcolor{mygray}\n";
                    }
                    my @line2=split/\t/,$hash1f{$linef[1]};
                    print OUT "\&$linef[1]&$linef[2]&$linef[5]\\%&$line2[7]&$line2[9]\\\\\n";
                }
            }
            print OUT "\\bottomrule[2pt]\n";
            print OUT "\\end{longtable}\n";

            print OUT "\\section*{\\\\}\n";
            print OUT "\n";

            ######用药建议
            print OUT "\%用药建议\n";
            print OUT "\\raggedright\n";
            print OUT "\\subsection*{用药建议}\n";
            print OUT "\\begin{supertabular}{c p{4cm}p{2cm}p{6cm}p{3.0cm}}\n";
            print OUT "\\setlength{\\parindent}{2em}\n";
            print OUT "\\indent\n";
            print OUT "\& \\normalsize 潜在靶向药&&&\\\\\n";
            print OUT "\&&&&\\\\\n";
            print OUT "\&&&&\\\\\n";
            print OUT "\&&&&\\\\\n";
            print OUT "\&&&&\\\\\n";
            print OUT "\&&&&\\\\\n";
            print OUT "\& \\normalsize 可能的耐药&&&\\\\\n";
            print OUT "\&&&&\\\\\n";
            print OUT "\&&&&\\\\\n";
            print OUT "\\end{supertabular}\n";
            print OUT "\\pagebreak\n";

            ########检测结果--靶向药
            print OUT "\%检测结果--靶向药\n";
        
        
            for (my $k=0;$k<@name;$k++){
                print OUT "\\raggedright\n";
                print OUT "\\subsection*{\\large $name[$k]靶向药物}\n";
                print OUT "\\small\n";
                print OUT "\\begin{supertabular}{c p{4cm}p{2cm}p{6cm}p{3.0cm}}\n";
                print OUT "\\toprule[2pt]\n";
                print OUT "\&\\large Drug&\\large Evidence&\\large Indication&\\large Clinical trials\\\\\n";
                print OUT "\\midrule[1pt]\n";
                open (IN1,"$drug_ann");
                my $i=1;
                while(my $line4=<IN1>){
                    chomp($line4);
                    my  @line4=split/\t/,$line4;
                    my $d= $line4[0].$line4[5];
                    if ($d eq $name[$k]){
                        $i++;
                        if ($i % 2 eq 0){
                            print OUT "\\rowcolor{mygray}\n";
                        }
                        print OUT "\&$line4[10]&$line4[13]&$line4[17]&$line4[18]\\\\\n";
                    }
                }
                print OUT "\\bottomrule[2pt]\n";
                print OUT "\\end{supertabular}\n";
                print OUT "\\\\\n";
                print OUT "\\large Notes: \\small Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.\n";
                print OUT "\\pagebreak\n";

            }
           
            close IN1;
            print OUT "\n";
            print OUT "\n";
            print OUT "\n";
          
            my @fusion_result=keys %hashf_drug;
            for (my $k=0;$k<@fusion_result;$k++){
                print OUT "\\raggedright\n";
                print OUT "\\subsection*{\\large $fusion_result[$k]靶向药物}\n";
                print OUT "\\small\n";
                print OUT "\\begin{supertabular}{c p{4cm}p{2cm}p{6cm}p{3.0cm}}\n";
                print OUT "\\toprule[2pt]\n";
                print OUT "\&\\large Drug&\\large Evidence&\\large Indication&\\large Clinical trials\\\\\n";
                print OUT "\\midrule[1pt]\n";
                open (IN1,"$drug_ann");
                my $i=1;
                while(my $line4=<IN1>){
                    chomp($line4);
                    my  @line4=split/\t/,$line4;
                    my $d= $line4[0]."-".$line4[5];
                    if ($d eq $fusion_result[$k]){
                        $i++;
                        if ($i % 2 eq 0){
                            print OUT "\\rowcolor{mygray}\n";
                        }
                        print OUT "\&$line4[10]&$line4[13]&$line4[17]&$line4[18]\\\\\n";
                    }
                }
                print OUT "\\bottomrule[2pt]\n";
                print OUT "\\end{supertabular}\n";
                print OUT "\\\\\n";
                print OUT "\\large Notes: \\small Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.\n";
                print OUT "\\pagebreak\n";

            }

            close IN1;
            print OUT "\n";
            print OUT "\n";
            print OUT "\n";
            }elsif($jud >= 1 && $judf<1){
            ######检测结果--基因变异
                print OUT "\%检测结果--基因变异\n";
                print OUT "\\raggedright\n";
                print OUT "\\linespread{1.5}\\selectfont\n";
                print OUT "\\section*{检测结果小结}\n";
                print OUT "\\subsection*{检出基因变异}\n";
                print OUT "\\centering\n";
                print OUT "\\small\n";
                print OUT "\\begin{longtable}{l p{1cm}p{2.4cm}p{1.3cm}p{2.0cm}p{1cm}p{1.8cm}p{4cm}}\n";
                print OUT "\\toprule[2pt]\n";
                print OUT "\&\\large Gene &\\large Location&\\large CDs&\\large AA&\\large AF&\\large Type&\\large Conditions\\\\\n";
                print OUT "\\midrule[1pt]\n";

                for (my $j=0;$j<=@name;$j++){
                    if($hash1{$name[$j]}){
                        if ($j%2 == 0){
                            print OUT "\\rowcolor{mygray}\n";
                        }
                        my @line2=split/\t/,$hash1{$name[$j]};
                        if ($line2[3]=~/>/){
                            my @Mut_cds=split/>/,$line2[3];
                            my $Mut_cds=$Mut_cds[0]."\$".">"."\$".$Mut_cds[1];
                            print OUT "\&$line2[0]&$line2[1]&$Mut_cds&$line2[5]&$hash4{$line2[0].$line2[5]}&$line2[7]&$line2[9]\\\\\n";
                        }else{
                            print OUT "\&$line2[0]&$line2[1]&$line2[3]&$line2[5]&$hash4{$line2[0].$line2[5]}&$line2[7]&$line2[9]\\\\\n";
                        }
                    }
                }
                print OUT "\\bottomrule[2pt]\n";
                print OUT "\\end{longtable}\n";
                print OUT "\\section*{\\\\}\n";
                print OUT "\n";

                ######用药建议
                print OUT "\%用药建议\n";
                print OUT "\\raggedright\n";
                print OUT "\\subsection*{用药建议}\n";
                print OUT "\\begin{supertabular}{c p{4cm}p{2cm}p{6cm}p{3.0cm}}\n";
                print OUT "\\setlength{\\parindent}{2em}\n";
                print OUT "\\indent\n";
                print OUT "\& \\normalsize 潜在靶向药&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\& \\normalsize 可能的耐药&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\\end{supertabular}\n";
                print OUT "\\pagebreak\n";
        

                ########检测结果--靶向药
                print OUT "\%检测结果--靶向药\n";
                for (my $k=0;$k<@name;$k++){
                    print OUT "\\raggedright\n";
                    print OUT "\\subsection*{\\large $name[$k]靶向药物}\n";
                    print OUT "\\small\n";
                    print OUT "\\begin{supertabular}{c p{4cm}p{2cm}p{6cm}p{3.0cm}}\n";
                    print OUT "\\toprule[2pt]\n";
                    print OUT "\&\\large Drug&\\large Evidence&\\large Indication&\\large Clinical trials\\\\\n";
                    print OUT "\\midrule[1pt]\n";
                    open (IN1,"$drug_ann");
                    my $i=1;
                    while(my $line4=<IN1>){
                        chomp($line4);
                        my  @line4=split/\t/,$line4;
                        my $d= $line4[0].$line4[5];
                        if ($d eq $name[$k]){
                            $i++;
                            if ($i % 2 eq 0){
                                print OUT "\\rowcolor{mygray}\n";
                            }
                            print OUT "\&$line4[10]&$line4[13]&$line4[17]&$line4[18]\\\\\n";
                        }
                    }
                print OUT "\\bottomrule[2pt]\n";
                print OUT "\\end{supertabular}\n";
                print OUT "\\\\\n";
                print OUT "\\large Notes: \\small Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.\n";
                print OUT "\\pagebreak\n";
                }
                close IN1;
                print OUT "\n";
                print OUT "\n";
                print OUT "\n";

            }elsif($jud < 1 && $judf>=1){
                print OUT "\%检测结果--基因变异\n";
                print OUT "\\raggedright\n";
                print OUT "\\linespread{1.5}\\selectfont\n";
                print OUT "\\section*{检测结果小结}\n";
                print OUT "\\subsection*{检出基因变异}\n";
                print OUT "\\centering\n";
                print OUT "\\small\n";
                print OUT "\\begin{longtable}{l p{2.3cm}p{5cm}p{1.3cm}p{1.8cm}p{4cm}}\n";
                print OUT "\\toprule[2pt]\n";
                print OUT "\&\\large Gene &\\large Fusion Location &\\large Rate&\\large Type&\\large Conditions\\\\\n";
                print OUT "\\midrule[1pt]\n";
  
                my %hashf_drug=();
                my @fusion=();
                open(INF,"$fusion");
                while(my $linef=<INF>){
                    chomp($linef);
                    my @linef=split/\t/,$linef;
                    if ($line3[0] eq $linef[0]){
                        push @fusion,$linef;
                        $hashf_drug{$linef[1]}=1;
                    }
                }
                close INF;
                my @fusion_result=keys %hashf_drug;
                for (my $j=0;$j<=@fusion;$j++){
                    my @linef=split/\t/,$fusion[$j];
    
                    if($hash1f{$linef[1]}){
                        if ($j%2 == 0){
                            print OUT "\\rowcolor{mygray}\n";
                        }
                        my @line2=split/\t/,$hash1f{$linef[1]};
                        print OUT "\&$linef[1]&$linef[2]&$linef[5]\\%&$line2[7]&$line2[9]\\\\\n";
                    }
                }
                
                print OUT "\\bottomrule[2pt]\n";
                print OUT "\\end{longtable}\n";

                print OUT "\\section*{\\\\}\n";
                print OUT "\n";
                print OUT "\%用药建议\n";
                print OUT "\\raggedright\n";
                print OUT "\\subsection*{用药建议}\n";
                print OUT "\\begin{supertabular}{c p{4cm}p{2cm}p{6cm}p{3.0cm}}\n";
                print OUT "\\setlength{\\parindent}{2em}\n";
                print OUT "\\indent\n";
                print OUT "\& \\normalsize 潜在靶向药&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\& \\normalsize 可能的耐药&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\&&&&\\\\\n";
                print OUT "\\end{supertabular}\n";
                print OUT "\\pagebreak\n";
                 
                print OUT "\%检测结果--靶向药\n";
        #        my @fusion_result=keys %hashf_drug;
                for (my $k=0;$k<@fusion_result;$k++){
                    print OUT "\\raggedright\n";
                    print OUT "\\subsection*{\\large $fusion_result[$k]靶向药物}\n";
                    print OUT "\\small\n";
                    print OUT "\\begin{supertabular}{c p{4cm}p{2cm}p{6cm}p{3.0cm}}\n";
                    print OUT "\\toprule[2pt]\n";
                    print OUT "\&\\large Drug&\\large Evidence&\\large Indication&\\large Clinical trials\\\\\n";
                    print OUT "\\midrule[1pt]\n";
                    open (IN1,"$drug_ann");
                    my $i=1;
                    while(my $line4=<IN1>){
                        chomp($line4);
                        my  @line4=split/\t/,$line4;
                        my $d= $line4[0]."-".$line4[5];
                        if ($d eq $fusion_result[$k]){
                            $i++;
                            if ($i % 2 eq 0){
                                print OUT "\\rowcolor{mygray}\n";
                            }
                            print OUT "\&$line4[10]&$line4[13]&$line4[17]&$line4[18]\\\\\n";
                        }
                    }
                    print OUT "\\bottomrule[2pt]\n";
                    print OUT "\\end{supertabular}\n";
                    print OUT "\\\\\n";
                    print OUT "\\large Notes: \\small Evidence level A: Trgeted threrapy surpported by NCCN or CSCO guidlines; B: Trgeted threrapy surpported by FDA or CFDA but not NCCN or CSCO guidlines; C: The drug is currently in clinical trials or FDA approved for treating other kinds of cancers, but not lung cancer; D: Trgeted threrapy surpported by literature.\n";
                    print OUT "\\pagebreak\n";
  
                }

                close IN1;
                print OUT "\n";
                print OUT "\n";
                print OUT "\n";
 
            }else{
            
                print OUT "\%检测结果--基因变异\n";
                print OUT "\\raggedright\n";
                print OUT "\\linespread{1.5}\\selectfont\n";
                print OUT "\\section*{检测结果--基因变异}\n";
                print OUT "\\subsection*{未检出相关基因突变}\n";

                print OUT "\\section*{\\\\}\n";
                print OUT "\n";
                print OUT "\n";
                print OUT "\n";
            }
        print OUT "\%附录--突变基因简介\n";
        print OUT "\\section*{附录}\n";
        print OUT "\\linespread{2}\\selectfont\n";
        print OUT "\\subsection*{1. 检测突变基因简介}\n";
        print OUT "\\setlength{\\parindent}{2em}\n";
        print OUT "\\justifying\n";
        print OUT "\\subsubsection{1.1 ALK}\n";
        print OUT "\\indent\n";
        print OUT "ALK是一种间变性淋巴瘤激酶（Anaplastic Lymphoma kinase, ALK），肺癌中ALK变异主要为ALK基因发生重排与其他基因融合。其中，EML4-ALK（棘皮动物微管结合蛋白样4-间变性淋巴瘤激酶）融合基因
变异是其主要类型，约占所有NSCLC的5\\%左右\$\^{[1-2]}\$。肺癌中与ALK基因融合的其他基因还包括TFG、KIF5B等。尽管ALK阳性的NSCLC在肺癌的比例很低，但在我国每年新发病例数仍然接近35000例\$\^{[3]}\$。因此，
准确鉴定出ALK重排阳性的NSCLC，并给予相应的治疗是需要的。针对ALK靶点的小分子抑制剂克唑替尼（Crizotinib）是一种ATP竞争性酪氨酸激酶抑制剂，可特异性靶向抑哈哈哈哈制ALK激酶，也可抑制c-MET和ROS1等信号通>路\$\^{[4]}\$。Alectinib(艾乐替尼)和Ceritini(色瑞替尼)作为第二代酪氨酸激酶抑制剂，分别通过抑制间变性淋巴瘤酪氨酸激酶和ALK的自体磷酸化过程，来降低癌细胞的增值和生存能力\$\^{[5]}\$。\\\\\n";
        print OUT "\$\\left[1\\right]\$ Soda \\ M, \\ Choi \\ YL, \\ Enomoto \\ M \\ et \\ al. \\ Identification \\ of \\ the \\ transforming \\ EML4-ALK \\ fusion \\ gene \\ in \\ non-small-cell \\ lung \\ cancer. \\ Nature. \\ 2007, \\ 448:561–566. \\\\\n";
        print OUT "\$\\left[2\\right]\$ Soda M, Takada S, Takeuchi K et al. A mouse model for EML4-ALK-positive lung cancer. Proc Natl Acad Sci USA.2008, 105:19893–19897. \\\\\n";
        print OUT "\$\\left[3\\right]\$ 全国肿瘤防治研究办公室/全国肿瘤登记中心/卫生部疾病预防控制局.2009 全国肿瘤登记年报. 北京:军事医学科学出版社.2010.\\\\\n";
        print OUT "\$\\left[4\\right]\$ 国家卫生和计划生育委员会。原发性肺癌诊疗规范（2015年）.中华肿瘤杂志，2015，37：1-12.\\\\\n";
        print OUT "\$\\left[5\\right]\$ NCCN Guidelines Version 2.2017, Non-small cell Lung cancer.\n";
        print OUT "\\pagebreak\n";
        print OUT "\n";
        print OUT "\n";

        print OUT "\\setlength{\\parindent}{2em}\n";
        print OUT "\\justifying\n";
        print OUT "\\subsubsection{1.2 BRAF}\n";
        print OUT "\\indent\n";
        print OUT "鼠类肉瘤病毒癌基因同源物B1（V-raf murine sarcoma viral oncogene homolog B1,BRAF）基因位于人第7号染色体上，其编码的一种丝氨酸/苏氨酸蛋白激酶位于EGFR信号通路下游，依>赖KRAS-GTP活化，是RAS-RAF-MEK-ERK信号通路中的重要转导因子。在NSCLC中，BRAF突变多见于腺癌，主要发生在第11和15外显子，约50\\%的BRAF突变为第15外显子上的V600E突变（约占3%的NSCLC患者）\$\^{[1-2]}\$。该>突变能够模拟T798和S601两个位点的磷酸化，从而导致BRAF的持续活化。不同于BRAF突变高发的黑色素瘤，NSCLC的BRAF突变有很大一部分为激酶活化域中的G469A突变（约40\\%）以及激酶结构域中的D594G突变（约10\\%）\$\^{[3]}\$。大部分情况下，BRAF突变不会与其他驱动突变如EGFR、KRAS基因突变同时发生\$\^{[4]}\$。然而研究表明，携带BRAF基因特定突变的患者对EGFR靶向药物治疗存在耐药性，是重要的检测靶标之一\$\^{[5]}\$。针
对BRAF-V600E突变，维罗非尼（Vemurafenib，商品名：Zelboraf）和达拉非尼（Dabrafenib，商品名：Tafinlar）两种靶向药可特异性抑制V600E突变细胞的ERK磷酸化，从而阻断其下游通路的信号转导，达到抗肿瘤效果。其
中，Dabrafenib 已获FDA批准与曲美替尼（Trametinib，商品名：Mekinist）联合使用治疗携带BRAF-V600E突变的转移性NSCLC患者\$\^{[6]}\$。Dabrafenib和Trametinib分别靶向MAPK信号通路中的不同激酶（BRAF和MEK），
临床研究显示联合使用可增加抗肿瘤效果\$\^{[7]}\$。而Vemurafenib目前仅被批准用于治疗黑色素瘤患者\$\^{[5]}\$。\\\\\n";
        print OUT "\$\\left[1\\right]\$  Gou LY, Wu YL. Prevalence of driver mutations in non-small-cell lung cancers in the People\'s Republic of China. Lung Cancer (Auckl) 2014; 5: 1-9.\\\\\n";
        print OUT "\$\\left[2\\right]\$ Zheng D, Wang R, Ye T, et al. MET exon 14 skipping defines a unique molecular class of non-small cell lung cancer. Oncotarget 2016, 7: 41691-41702.\\\\\n";
        print OUT "\$\\left[3\\right]\$ Ji H, Wang Z, Perera SA, et al. Mutations in BRAF and KRAS converge on activation of the mitogen-activated protein kinase pathway in lung cancer mouse models. Cancer Res,2007, 67: 4933-4939.\\\\\n";
        print OUT "\$\\left[4\\right]\$ Paik PK, Arcila ME, Fara M, et al. Clinical characteristics of patients with lung adenocarcinomas harboring BRAF mutations. J Clin Oncol 2011,29: 2046-2051.\\\\\n";
        print OUT "\$\\left[5\\right]\$ Di Nicolantonio F, Martini M, Molinari F, et al. Wild-type BRAF is required for response to panitumumab or cetuximab in metastatic colorectal cancer. J Clin Oncol 2008,26: 5705-5712.\\\\\n";
        print OUT "\$\\left[6\\right]\$ NCCN Guidelines Version 8.2017, Non-Small Cell Lung Cancer.\\\\\n";
        print OUT "\$\\left[7\\right]\$ Planchard D, Besse B, Groen HJM, et al. Dabrafenib plus trametinib in patients with previously treated BRAF(V600E)-mutant metastatic non-small cell lung cancer: an open-label, multicentre phase 2 trial. Lancet Oncol 2016, 17: 984-993.\\\\\n";
        print OUT "\\pagebreak\n";
        print OUT "\n";
        print OUT "\n";

        print OUT "\\setlength{\\parindent}{2em}\n";
        print OUT "\\justifying\n";
        print OUT "\\subsubsection{1.2 EGFR}\n";
        print OUT "\\indent\n";
        print OUT "表皮生长因子受体（Epidermal growth factor receptor, EGFR）信号通路在细胞生长、增殖和分化中发挥着重要作用。EGFR突变将导致EGFR磷酸化，并持续激活其下游信号，导致肿瘤生长。EGFR突变主要发生于第18－21号外显子中，为EGFR的激酶域。在肺癌中，占90\\%的EGFR突变为第19外显子缺失突变及第21外显子L858R点突变\$\^{[1]}\$。上述两种突变是明确的敏感突变，提示肿瘤对EGFR靶向治疗敏感。然而，尽管EGFR靶向治疗可对突变患者产生良好的肿瘤应答，在经过9-13个月的治疗后，大部分患者会产生耐药，主要原因为EGFR第20外显子的T790M点突变，占继发耐药者中的约50\\%\$\^{[2]}\$。亚洲人群中，EGFR突变较西方国家发生率高，约占NSCLC患者的50\\%，因此检测EGFR突变以指导靶向治疗在我国尤其重要\$\^{[3]}\$。第一代吉非替尼（Gefitinib，商品名：易瑞沙Iressa）、厄洛替尼（Erlotinib，商品名：特罗凯Tarceva）和埃克替尼>（Icotinib，商品名：凯美纳），以及第二代阿法替尼（Afatinib，商品名：Gilotrif）是经CFDA批准用于治疗EGFR敏感突变NSCLC患者的EGFR酪氨酸激酶抑制剂（Tyrosine kinase inhibitor，TKI）\$\^{[4]}\$。第一>代EGFR-TKI通过竞争性抑制ATP与EGFR酪氨酸激酶的结合达到抗肿瘤效果；第二代EGFR-TKI不可逆地抑制EGFR酪氨酸激酶。而第三代奥希替尼（Osimertinib，商品名：Tagrisso）则能克服T790M耐药性，目前已获CFDA批准用于
治疗经EGFR-TKI治疗后产生耐药的T790M阳性NSCLC患者。\\\\\n";
        print OUT "\$\\left[1\\right]\$ Pao W, Miller VA. Epidermal growth factor receptor mutations, small-molecule kinase inhibitors, and non-small-cell lung cancer: current knowledge and future directions. J Clin Oncol 2005, 23: 2556-2568.\\\\\n";
        print OUT "\$\\left[2\\right]\$ Kobayashi S, Boggon TJ, Dayaram T, et al. EGFR mutation and resistance of non-small-cell lung cancer to gefitinib. N Engl J Med 2005, 352: 786-792.\\\\\n";
        print OUT "\$\\left[3\\right]\$ Gou LY, Wu YL. Prevalence of driver mutations in non-small-cell lung cancers in the People\'s Republic of China. Lung Cancer (Auckl) 2014, 5: 1-9.\\\\\n";
        print OUT "\$\\left[4\\right]\$ 中国临床肿瘤学会指南工作委员会. 中国临床肿瘤学会（CSCO）原发性肺癌诊疗指南2016.V1.\\\\\n";
        print OUT "\\pagebreak\n";
        print OUT "\n";
        print OUT "\n";

        print OUT "\\setlength{\\parindent}{2em}\n";
        print OUT "\\justifying\n";
        print OUT "\\subsubsection{1.2 KRAS\/NRAS}\n";
        print OUT "\\indent\n";
        print OUT "RAS家族是一种鼠类肉瘤病毒癌基因，主要包括KRAS（Kirsten rat sarcoma viral oncogene，又称p21）和NRAS（Neuroblastoma RAS viral oncogene），分别位于人第12和1号染色体上>。RAS基因变异以点突变为主，其中KRAS突变多发生在第12密码子，NRAS突变多发生在第61密码子。这些突变改变编码Ras蛋白和GTP酶活化蛋白作用位点的氨基酸，导致Ras-GTP处于持续激活状态，在不依赖EGFR等上游生长因>子激活的情况下活化RAS/MAPK信号通路，引起细胞的不可控增殖。在结直肠癌中，KRAS突变与抗EGFR单抗（Panitumumab和Cetuximab）较差的疗效相关，是指导靶向治疗的一种常规基因检测\$\^{[1]}\$。而在NSCLC中，KRAS>突变多见于腺癌，但是亚洲人群较西方人群突变发生率较低，仅占约6\\%（NRAS突变约1\\%）\$\^{[2]}\$。目前尚无治疗肺癌的KRAS/NRAS靶向药物。体外细胞研究显示，MEK抑制剂（Selumetinib和Trametinib）或可能有效>治疗NRAS突变的NSCLC\$\^{[3]}\$。不同于结直肠癌，KRAS突变与EGFR-TKI疗效的相关性仍未有一致定论。尽管大量回顾性研究指出KRAS突变与低EGFR-TKI反应率相关（0-5\\% vs 7-30\\%）\$\^{[4]}\$，但由于EGFR和KRAS突变很少同时存在，因此缺乏大规模前瞻性研究证实两者的关系。而且无论KRAS突变状态如何，野生型EGFR患者均与EGFR-TKI治疗的不良预后相关\$\^{[5]}\$，提示KRAS突变仅为EGFR-TKI耐药的其中一种模式，其指导意>义尚不明确。\\\\\n";
        print OUT "\$\\left[1\\right]\$ NCCN Guidelines Version 2.2017, Colon Cancer.\\\\\n";
        print OUT "\$\\left[2\\right]\$ Gou LY, Wu YL. Prevalence of driver mutations in non-small-cell lung cancers in the People\'s Republic of China. Lung Cancer (Auckl) 2014, 5: 1-9.\\\\\n";
        print OUT "\$\\left[3\\right]\$ Ohashi K, Sequist LV, Archila ME, et al. Characteristics of lung cancers harboring NRAS mutations. Clin Cancer Res 2013, 19: 2584-2591.\\\\\n";
        print OUT "\$\\left[4\\right]\$ Gregory J. Riely, Marc Ladanyi. KRAS mutations: an old oncogene becomes a new predictive biomarker. J Mol Diagn 2008, 10: 493-495.\\\\\n";
        print OUT "\$\\left[5\\right]\$ Cheng L, Zhang S, Alexander R, et al. The landscape of EGFR pathways and personalized management of non-small-cell lung cancer. Future Oncol 2011, 7: 519-541.\\\\\n";
        print OUT "\\pagebreak\n";
        print OUT "\n";
        print OUT "\n";


        print OUT "\%附录--NCCN指南\n";
        print OUT "\\subsection*{2. NCCN临床指南：非小细胞肺癌(2017.V2)}\n";
        print OUT "\\begin{tabular}{|l c|c|c|}\n";
        print OUT "\\cline{1-4}\n";
        print OUT "\&突变基因&突变位点&靶向药\\\\\n";
        print OUT "\\cline{1-4}\n";
        print OUT "\& & &Crizotinib(克唑替尼)\\\\\n";
        print OUT "\&ALK&基因重排&Ceritinib(色瑞替尼)\\\\\n";
        print OUT "\& & &Alectinib(艾乐替尼)\\\\\n";
        print OUT "\& & &Brigatinib(布吉他滨)\\\\\n";
        print OUT "\\cline{1-4}\n";
        print OUT "\& & &vemurafenib(威罗菲尼)\\\\\n";
        print OUT "\&BRAF&V600E&dabrafenib(达拉非尼)\\\\\n";
        print OUT "\& & &dabrafenib+trametinib(曲美替尼)\\\\\n";
        print OUT "\\cline{1-4}\n";
        print OUT "\& & &Erlotinib(厄洛替尼，特罗凯)\\\\\n";
        print OUT "\&EGFR&L858R/L861Q/G719X/S768I/19del&Afatinib(阿法替尼)\\\\\n";
        print OUT "\& & &Gefitinib(吉非替尼，易瑞沙)\\\\\n";
        print OUT "\\cline{3-4}\n";
        print OUT "\& &T790M&Osimertinib(奥斯替尼)\\\\\n";
        print OUT "\\cline{1-4}\n";
        print OUT "\&HER2& &Trastuzumab(曲妥珠单抗)\\\\\n";
        print OUT "\& & &Afatinib(阿法替尼)\\\\\n";
        print OUT "\\cline{1-4}\n";
        print OUT "\&MET&高水平MET扩增或14号外显子跳跃突变&Crizotinib(克唑替尼)\\\\\n";
        print OUT "\\cline{1-4}\n";
        print OUT "\\end{tabular}\n";
        print OUT "\\clearpage\n";
        print OUT "\\end{CJK*}\n";
        print OUT "\\end{document}\n";
        print OUT "\n";
        print OUT "\n";
        print OUT "\n";
 
    }
}
close IN;
close OUT;
