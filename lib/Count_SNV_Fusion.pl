#!/usr/bin/perl

use warnings;
use strict;
use File::Basename;

my $InputFile = shift;
my $InputFile2 = shift;
my $OutputFile = shift;
my $Out2File = shift;
my %hash = ();
my @LineLen;
my @Gene;
my $Cancer;

open(IN3, "$InputFile2") || die "Can't open file $InputFile2\n";
while(my $Lines = <IN3>){
    chomp($Lines);
    if($Lines=~/^检测癌种/){
        my @Lines = split/\t/,$Lines;
        if($Lines[1]=~/^肺癌/){
            $Cancer = "lung"
        }else{
            $Cancer = "CRC"
        }
    }else{
        next;
    }
}

open(OUT, ">$OutputFile");
open(OUTT, ">$Out2File");
open(IN, "$InputFile") || die "Can't open file $InputFile\n";
while(my $line=<IN>){
    chomp($line);
    my @lines = split/\t/,$line;
    if($lines[0]=~/^RAS/){
        my $G = 'RAS';
        push @Gene, $G;
    }else{
        push @Gene, $lines[0];
    }
    push @LineLen, $lines[2];
}

my $MutNum = @LineLen;
print OUT "##".$MutNum."\n";
my $j=1;
if(int($MutNum) > 0){
    open(IN2, "$InputFile") || die "Can't open file $InputFile\n";
    while(my $Line=<IN2>){
        chomp($Line);
        print OUT $Line."\t".$j."\n";
        $j++;
    }
}else{
    print OUT "没有检出突变"."\t"." "."\t"." "."\t"." "."\t"."/"."\t"."no_mutation"."\t".$Cancer."\t"."0"."\n";
}

my @NewGene;
for(my $g=0;$g<@Gene;$g++){
    $hash{$Gene[$g]}+=1;
    if($hash{$Gene[$g]} > 1){
        next;
    }else{
        push @NewGene, $Gene[$g];
    }
}

my $GeneN = scalar @NewGene;
if($GeneN > 0){
    for(my $i=0;$i<@NewGene;$i++){
        my $N = int($i) + 1;
        print OUTT $N."."."\t".$NewGene[$i]."\t".$Cancer."\n";
    }
}else{
    print OUTT " "."\t"."没有检出突变"."\t".$Cancer."\n";
}

close IN;
close IN2;
close IN3;
close OUT;
close OUTT;
