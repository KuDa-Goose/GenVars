#!/usr/bin/perl

$in=shift;

open(IN,"$in");
open(OUT,">Probe_Stats_2021_Jan_19_UMI.txt");while($line=<IN>){
    $line=~s/probe111_/TP53_i05-1_/g;
    $line=~s/probe112_/TP53_i05-2_/g;
    $line=~s/probe113_/TP53_i06-1_/g;
    $line=~s/probe107_/PIK3CA_i10-1_/g;
    $line=~s/probe104_/NRAS_i03-1_/g;
    $line=~s/probe206_/KRAS_i02-2_/g;
    $line=~s/probe76_/KRAS_i03-1_/g;
    $line=~s/probe210_/HER2_i20-2_/g;
    $line=~s/probe52_/EGFR_i21-2_/g;
    $line=~s/probe228_/EGFR_i20-5_/g;
    $line=~s/probe256_/EGFR_i20-4_/g;
    $line=~s/probe214_/EGFR_i19-3_/g;
    $line=~s/probe229_/BRAF_i15-2_/g;
    print OUT $line;
}
close IN;
close OUT;
