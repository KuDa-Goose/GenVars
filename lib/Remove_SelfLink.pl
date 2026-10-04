#!/usr/bin/perl 

use warnings;
use strict;

my $in1=shift;##R1
my $in2=shift;##R2
my $in3=shift;##探针长度
my $out1=shift;##不自连的R1
my $out2=shift;##自连的R1
my $out3=shift;##不自连的R2
my $out4=shift;##自连的R2
my %hash=();

open(OUT,">$out1");
open(OUTT,">$out2");
open(IN,"$in1") || die "Can't open file $in1\n";
while(my $line=<IN>){
    chomp($line);
    my $seq=<IN>;
    chomp($seq);
    <IN>;
    my $qual=<IN>;
    chomp($qual);
    my @line = split/\//,$line;
    if(length($seq) >= (int($in3)+20)){
        $hash{$line[0]}=1;
        print OUT $line."\n".$seq."\n"."+"."\n".$qual."\n";
    }else{
        print OUTT $line."\n".$seq."\n"."+"."\n".$qual."\n";
    }
}

open(OUTTT,">$out3");
open(OUTTTT,">$out4");
open(IN2,"$in2") || die "Can't open file $in2\n";
while(my $Line=<IN2>){
    chomp($Line);
    my $Seq=<IN2>;
    chomp($Seq);
    <IN2>;
    my $Qual=<IN2>;
    chomp($Qual);
    my @Line = split/\//,$Line;
    if(exists $hash{$Line[0]}){
        print OUTTT $Line."\n".$Seq."\n"."+"."\n".$Qual."\n";
    }else{
        print OUTTTT $Line."\n".$Seq."\n"."+"."\n".$Qual."\n";
    }
}


close IN;
close IN2;
close OUT;
close OUTT;
close OUTTT;
close OUTTTT;

