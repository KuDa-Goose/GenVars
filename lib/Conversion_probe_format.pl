#!/usr/bin/perl

use strict;
use warnings;

die "perl $0 <input_file1> <input_file2> <output_file>" unless @ARGV == 3;

my $input1=shift;
my $input2=shift;
my $output=shift;

my @info = split/\_/,$input1;
my $month=$info[3]."_".$info[4];
my @ProbeName;
my @Probe;
my @SampleName;
my %hash=();
my %total=();
my %mean=();

open(IN2,"$input2") || die "Can't open file2 $input2\n";
while(my $line=<IN2>){
    chomp($line);
    if($line=~/^Chr/){
        next;
    }else{
        my @line=split/\t/,$line;
        push @ProbeName, $line[3];
    }
}

open(OUT,">$output");
print OUT "Probe_Name"."\t"."year"."\t"."month"."\t"."Barcode"."\t"."Total_reads"."\t"."Ontarget_reads"."\t"."Mean_ontarget_reads"."\t"."Probe_reads"."\n";
open(IN,"$input1") || die "Can't open file $input1\n";
while(my $Line=<IN>){
    chomp($Line);
    if($Line=~/^Sample/){
        @Probe=split/\t/,$Line;
    }else{
        my @Line=split/\t/,$Line;
        $total{$Line[0]}=$Line[1];
        $mean{$Line[0]}=$Line[-1];
        for(my $i=2;$i<@Probe;$i++){
            my $keys=$Line[0]."\t".$Probe[$i];
            $hash{$keys}=$Line[$i];
        }
        push @SampleName, $Line[0];
    }
}

for(my $j=0;$j<@ProbeName;$j++){
    my $ProbeOntar=$ProbeName[$j]."_ontarget";
    for(my $s=0;$s<@SampleName;$s++){
        print OUT $ProbeName[$j]."\t".$info[2]."\t".$month."\t".$SampleName[$s]."\t".$total{$SampleName[$s]}."\t".$hash{$SampleName[$s]."\t".$ProbeOntar}."\t".$mean{$SampleName[$s]}."\t".$hash{$SampleName[$s]."\t".$ProbeName[$j]}."\n";
    }
}

close IN;
close IN2;
close OUT;
