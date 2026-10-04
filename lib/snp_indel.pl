#!/usr/bin/perl

use warnings;
use strict;
use Getopt::Long;


my $usage = <<USAGE_end;
Usage:
    perl $0 -v input_dir -s snp_file -i insertion-deletion_file -c indels_file -m midele-output -e Mut_Errot.xls-o output_file
    
        -v <directory> the directory which contains directories of Sample* 
        -s <file name> snp input information file name
        -i <file name> insertion and deletion input information file name
        -c <file name> indels input information file name
        -m <file name> snp result midele-output file name
        -e <file name> error mutation pos file name
        -o <filename>  the output name of snp.xls
        -h/help <boolean>    Print help of current program

USAGE_end

# default parameter
my $in       ;
my $SNP_Anno ;
my $Indel_Anno ;
my $indels_Anno;
my $out_name ;
my $mid_out_name ;
my $error_file;
my $help     ;

# Get parameters
GetOptions(
    'v|input=s'      => \$in,
    's|snp-Annotation=s' => \$SNP_Anno,
    'i|insertion-deletion-Annotation=s' =>\$Indel_Anno,
    'c|indels-Annotation=s' =>\$indels_Anno,
    'm|midele-output=s' =>\$mid_out_name,
    'e|error-file=s' =>\$error_file,
    'o|output=s'     => \$out_name,
    'h|help'         => \$help );
    
die "$usage" unless ($in && $SNP_Anno && $Indel_Anno && $indels_Anno && $out_name);

if ($help){
    print $usage;
    exit;
}


open(OUT, ">$out_name");
print OUT "Sample";

open(OUT1,">$mid_out_name");
#######snp位点信息
my @Vars = ();
my @position=();
my %snp_hash=();  #中间文件1
open (ANNO, "<", "$SNP_Anno") or die "Cant't open $SNP_Anno!";
while(<ANNO>){
    chomp;
    my @line_C = split/\t/, $_;
    my $SNP_info = "chr".join("\t",$line_C[0],$line_C[1],$line_C[3],$line_C[4]);
    $snp_hash{$SNP_info}=1;
    push @position,$SNP_info;
    my $varName = $line_C[10];
    push @Vars, $varName;
    print OUT "\t".$varName."_Ref\t".$varName."_Mut\t".$varName."_AF";
}
close ANNO;

######insertion and deletion位点信息
my @Vars_indel = ();
my @position_indel=();
open (INANNO, "<", "$Indel_Anno") or die "Can't open $Indel_Anno!";
while(<INANNO>){
    chomp;
    my @line_C = split(/\t/, $_);
    my $indel_info = "chr".join("\t", $line_C[0],$line_C[1],$line_C[3],$line_C[4]);
    my $varName = $line_C[10];
    push @position_indel,$indel_info;
    push @Vars_indel, $varName;
    print OUT "\t".$varName."_Ref\t".$varName."_Mut\t".$varName."_AF";
}
close INANNO;

######indels位点信息
my @complex=();
open(IN,"$indels_Anno")or die "Cant't open $indels_Anno!"; 
while(my $line=<IN>){
    chomp($line);
    my @line = split/\t/,$line;
    print OUT "\t".$line[-1]."_Ref\t".$line[-1]."_Mut\t".$line[-1]."_AF";
    push @complex,$line;
}
print OUT "\n";
close IN;


######循环每个样本的snp和indel的vcf文件
my @file9=`ls $in/Step3*/*Mutation_Error.xls`;
my @file4=`ls $in/Step3*/*pileup.snp.vcf`;
my @file1=`ls $in/Step3*/*-N.vcf`;
my @file2=`ls $in/Step3*/*pileup.indel.vcf`;
my @file3=`ls $in/Step2*/IonXpress*.deep`;
for(my $a=0;$a<@file1;$a++){
    chomp($file1[$a]);
    my $Sample=(split/\/Step3/,$file1[$a])[0];
    $Sample=(split/\//,$Sample)[-1];
    print OUT $Sample;
    print OUT1 $Sample."\n";
    my %SNP_Hash=();
    my %Indel_Hash=();
    my %Complex_Hash=();
 
######deep信息放进哈希
    my %deep_hash=();
    open(IN,"$file3[$a]") || die "Can't open file $file3[$a]!\n";
    while(<IN>){
        chomp;
        $_=~s/\s+/\t/g;
        my @line=split/\t/,$_;
        $deep_hash{$line[0].$line[1]}=$line[2];
    }
    close IN;
    
############末尾错配碱基
    my %Errot_List=();
    open(INN, "$file9[$a]") || die "Can't open file $file9[$a]\n";
    while(my $line=<INN>){
        chomp($line);
        my @lines = split/\t/,$line;
        my $PosS = $lines[0]."\t".$lines[1]."\t".$lines[2];
        if(exists $Errot_List{$PosS}){
            $Errot_List{$PosS}+=1;
        }else{
            $Errot_List{$PosS}=1;
        }
    }

######Middle output###
    open(IN, "$file4[$a]") || die "Can't open file $file4[$a]!\n";
    while(my $line=<IN>){
        chomp($line);
        $line=~s/\s+/\t/g;
        my @line=split/\t/,$line;
        my $All_Line = ($line[0]."\t".$line[1]."\t".$line[2]."\t".$line[3]);
        if ($snp_hash{$All_Line}){
            print OUT1 "$line\n";
        }
    }
    close IN;

######get_snp_count
    open(IN, "$file1[$a]") || die "Can't open file $file1[$a]!\n";
    while(my $line=<IN>){
        chomp($line);
        $line=~s/\s+/\t/g;
        my @line=split/\t/,$line;
        my $Str_Line = ($line[0]."\t".$line[1]."\t".$line[2]."\t".$line[3]);
        my $o_num;
        if($line[6] eq "0%"){
            $o_num =($line[4]."\t".$line[5]."\t"."0.00%");
        }else{
            $o_num =($line[4]."\t".$line[5]."\t".$line[6]);
        }
        $SNP_Hash{$Str_Line}=$o_num;
        $Complex_Hash{$Str_Line}=$o_num;
    }
    for(my $i=0;$i<@position;$i++){ 
        my @PPP = split/\t/,$position[$i];
        my $PP = $PPP[0]."\t".$PPP[1]."\t".$PPP[3];
        if ($SNP_Hash{$position[$i]}){
            if(exists $Errot_List{$PP}){
                my @AFInfo = split/\t/,$SNP_Hash{$position[$i]};
                my $MutReads = int($AFInfo[1]) - int($Errot_List{$PP});
                my $NewAF;
                my $RefReads = int($AFInfo[0]) + int($AFInfo[1]);
                if(int($RefReads) == 0 ){
                    $NewAF = 0;
                }else{
                    $NewAF = ((int($MutReads)/int($RefReads)) * 100)."%";
                }
                print OUT "\t".$AFInfo[0]."\t".$MutReads."\t".$NewAF;
            }else{
                print OUT "\t".$SNP_Hash{$position[$i]};
            }
        }else{
            my @pos=split/\t/,$position[$i];
            if ($deep_hash{$pos[0].$pos[1]}){
                print OUT "\t".$deep_hash{$pos[0].$pos[1]}."\t0\t0";
            }else{
                print OUT "\t0\t0\t0";
            }
        }
    }

######get_insertion and deletion_count
    open(IN, "$file2[$a]") || die "Can't open file $file2[$a]!\n";
    while(my $line=<IN>){
        chomp($line);
        $line=~s/\s+/\t/g;
        my @line=split/\t/,$line;
        my @o_num=split/\//,$line[3];
        my $o_num;
        if($line[6] eq "0%"){
            $o_num =($line[4]."\t".$line[5]."\t"."0.00%");
        }else{
            $o_num =($line[4]."\t".$line[5]."\t".$line[6]);
        }
        my $Str_Line = ($line[0]."\t".$line[1]."\t".$line[2]."\t".$o_num[0]);
        $Indel_Hash{$Str_Line}=$o_num;
        $Complex_Hash{$Str_Line}=$o_num;
    }
    close IN;
    for(my $i=0;$i<@position_indel;$i++){
        if (exists $Indel_Hash{$position_indel[$i]}){
            print OUT "\t".$Indel_Hash{$position_indel[$i]};
       }else{
            my @pos=split/\t/,$position_indel[$i];
            if ($deep_hash{$pos[0].$pos[1]}){
                print OUT "\t".$deep_hash{$pos[0].$pos[1]}."\t0\t0";
            }else{
                print OUT "\t0\t0\t0";
            }
        }
    }

######get indels_count
    for(my $i=0;$i<@complex;$i++){
        my @line=split/\t/,$complex[$i];
        if(@line == 4){
            my @Mut1=split/,/,$line[0];
            my $key1=$Mut1[0]."\t".$Mut1[1]."\t".$Mut1[2]."\t".$Mut1[3];
            my @Mut2=split/,/,$line[1];
            my $key2=$Mut2[0]."\t".$Mut2[1]."\t".$Mut2[2]."\t".$Mut2[3];
            if((exists $Complex_Hash{$key1}) && (exists $Complex_Hash{$key2})){
                my @id1=split/\t/,$Complex_Hash{$key1};
                my @id2=split/\t/,$Complex_Hash{$key2};
                my $AF1=(split/\%/,$id1[2])[0];
                my $AF2=(split/\%/,$id2[2])[0];
                 if($AF1>=$AF2){
                    print OUT "\t".$Complex_Hash{$key2};
                }else{
                    print OUT "\t".$Complex_Hash{$key1};
                }
            }else{
                if(exists $deep_hash{$Mut1[0].$Mut1[1]}){
                    print OUT "\t".$deep_hash{$Mut1[0].$Mut1[1]}."\t0\t0";
                }else{
                    print OUT "\t0\t0\t0";
                }
            }
        }elsif(@line == 5){
            my @Mut1=split/,/,$line[0];
            my $key1=$Mut1[0]."\t".$Mut1[1]."\t".$Mut1[2]."\t".$Mut1[3];
            my @Mut2=split/,/,$line[1];
            my $key2=$Mut2[0]."\t".$Mut2[1]."\t".$Mut2[2]."\t".$Mut2[3];
            my @Mut3=split/,/,$line[2];
            my $key3=$Mut3[0]."\t".$Mut3[1]."\t".$Mut3[2]."\t".$Mut3[3];
            if((exists $Complex_Hash{$key1}) && (exists $Complex_Hash{$key2}) && (exists $Complex_Hash{$key3})){
                my @id1=split/\t/,$Complex_Hash{$key1};
                my @id2=split/\t/,$Complex_Hash{$key2};
                my @id3=split/\t/,$Complex_Hash{$key3};
                my $AF1=(split/\%/,$id1[2])[0];
                my $AF2=(split/\%/,$id2[2])[0];
                my $AF3=(split/\%/,$id3[2])[0]; 
                if($AF1<=$AF2 && $AF1<=$AF3){
                    print OUT "\t".$Complex_Hash{$key1};
                }elsif($AF2<=$AF1 && $AF2<=$AF3){
                    print OUT "\t".$Complex_Hash{$key2};
                }elsif($AF3<=$AF1 && $AF3<=$AF2){
                    print OUT "\t".$Complex_Hash{$key3};
                }
            }else{
                if(exists $deep_hash{$Mut1[0].$Mut1[1]}){
                    print OUT "\t".$deep_hash{$Mut1[0].$Mut1[1]}."\t0\t0";
                }else{
                    print OUT "\t0\t0\t0";
                }
            }
        }
    }
    print OUT "\n";
}
close OUT; 
close OUT1;
