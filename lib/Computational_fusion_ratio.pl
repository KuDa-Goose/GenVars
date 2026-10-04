#!/usr/bin/perl

use warnings;
use strict;
use Getopt::Long;

#die "perl $0 <input_file1> <input_file2> <input_path> <input_sample>" unless @ARGV==4;
my $usage = <<USAGE_end;
Usage:
    perl $0 -a All_point -s Aln_ALK -i input_path -c sample -o output_file

        -a <file name> input file of All_point.txt
        -s <file name> sam of alignment with ALK
        -i <path> input path
        -c <char> input sample barcode
        -o <filename>  the output file name 
        -h/help <boolean>    Print help of current program

USAGE_end

my $input_file1;
my $input_file2;
my $input_path;
my $Sample;
my $output_file;
my %hash;
my $help;

# Get parameters
GetOptions(
    'a|input=s'      => \$input_file1,
    's|sam=s' => \$input_file2,
    'i|input_path=s' =>\$input_path,
    'c|Sample_barcode=s' =>\$Sample,
    'o|output=s'     => \$output_file,
    'h|help'         => \$help );

die "$usage" unless ($input_file1 && $input_file2 && $input_path && $Sample && $output_file);

if ($help){
    print $usage;
    exit;
}


my $pointer = &Get_Break_Point($input_file1, $input_file2, $input_path, $Sample);
&Computational_Non_Fusion($pointer, $input_file2, $Sample, $output_file);


sub Get_Break_Point{
    my $input_file1=shift;
    my $input_file2=shift;
    my $input_path=shift;
    my $Sample=shift;
    my %hash_Info=();
    open(IN,"$input_file1") || die "Can't open file1 $input_file1\n";
    while(my $line=<IN>){
        chomp($line);
        my @line=split/\t/,$line;
        my @Info=split/\_/,$line[1];
        $hash{$Info[0]."\t".$Info[1]}=$Info[1];
    }
    my @keys = keys %hash;
    for(my $i=0;$i<@keys;$i++){
        my @Geno=split/\t/,$keys[$i];
        my %hash_G=();
        my $break_1;
        my $point;
        my @point;
        my @break;
        open(IN2,"$input_path/Aln_merged_$Sample\_$Geno[0]\.sam") || die "Can't open file2 $input_path/Aln_merged_$Sample\_$Geno[0]\.sam\n";
        while(my $Line=<IN2>){
            chomp($Line);
            if($Line=~/^@/){
                next;
            }else{
                my @Line=split/\t/,$Line;
                if($Line[3] == $Geno[1]){
                    my $length=length($Line[9]);
                    $hash_G{$Line[0]}=$length;
                }
            }
        }
        open(IN3,"$input_file2") || die "Can't open file3 $input_file2\n";
        while(my $Lines=<IN3>){
            chomp($Lines);
            if($Lines=~/^@/){
                next;
            }else{
                my @Lines=split/\t/,$Lines;
                my $count=0;
                if($hash_G{$Lines[0]}){
                    my $position=$Lines[3];
                    while($Lines[5] =~ /(\d+)M/g){
                        $count=$count+$1;
                    }
                    my $Length=$count+$Lines[3]-1;
                    push @point, $position;
                    push @break, $Length; 
                }
            }
        }
        my %Temp;
        my $Max=0;
        foreach ( @point ) {
            my $Count = $Temp{$_}++;
            $Max = $Count if $Count >= $Max;
        }
        foreach ( keys %Temp ) {
            if($Temp{$_} == $Max+1){
                $point = $_;
            }
        }
        my %temp;
        my $max=0;
        foreach ( @break ) {
            my $count = $temp{$_}++;
            $max = $count if $count >= $max;
        }
        foreach ( keys %temp ) {
            if($temp{$_} == $max+1){
                $break_1 = $_;
            }
        }
        $hash_Info{"ALK"."\t".$point."\t".$break_1."\t".$keys[$i]}=1;
    }
    my $pointer = \%hash_Info;
    return $pointer; 
}


sub Computational_Non_Fusion{
    my $pointer=shift;
    my $input_file2=shift;
    my $Sample=shift;
    my $output_file=shift;
    my @Keys = keys %{$pointer};
    my $N_fusion=0;
    open(OUT,">$output_file");
    print OUT "Sample"."\t"."Gene_1"."\t"."Break_point1"."\t"."Gene_2"."\t"."Break_point2"."\t"."Non_Fusion"."\n";
    for(my $i=0;$i<@Keys;$i++){
        my @Info = split/\t/,$Keys[$i]; 
        open(IN4,"$input_file2") || die "Can't open file2 $input_file2\n";
        while(my $Line=<IN4>){
            chomp($Line);
            if($Line=~/^@/){
                next;
            }else{
                my @Line=split/\t/,$Line;
                my $count_m=0;
                my $count_s=0;
                while($Line[5] =~ /(\d+)M/g){
                    $count_m=$count_m+$1;
                }
                if($Line[5]=~/S/){
                    while($Line[5] =~ /(\d+)S/g){
                        $count_s=$count_s+$1;
                    }
                }else{
                    $count_s=0;
                }
                my $Length=$Line[3]+$count_m;
                if(($Line[1] == "16") && (($Line[3]>=$Info[1]-2) && ($Line[3]<=$Info[1]+2)) && ($Length>=$Info[2]+5) && ($count_s<=3)){
                    $N_fusion++;
                }
            }
        }
        print OUT $Sample."\t".$Info[0]."\t".$Info[2]."\t".$Info[3]."\t".$Info[4]."\t".$N_fusion."\n";
    }
}
close IN;
close IN2;
close IN3;
close IN4;
close OUT;
