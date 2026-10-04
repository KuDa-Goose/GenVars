#!/usr/bin/perl

use strict;
use warnings;

my $input=shift;
my $input2=shift;
my $SampleNumber;

open(IN,"$input") || die "Can't open file $input\n";
while(my $line=<IN>){
    chomp($line);
    if($line=~/^样本编号/){
        my @lines = split/\t/,$line;
        $SampleNumber = "C_".$lines[1];
    }else{
        next;
    }
}

my $inFileName = (split/\//,$input2)[-1];
my $outFileName = $SampleNumber."_".$inFileName;
open(OUT, ">$outFileName");
open(IN2, "$input2") || die "Can't open file $input2\n";
while(my $Line=<IN2>){
    chomp($Line);
    print OUT $Line."\n";
}

close IN;
close IN2;
close OUT;
