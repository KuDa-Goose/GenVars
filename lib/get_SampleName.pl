#!/usr/bin/perl

use strict;
use warnings;

die "perl $0 <list> <SampleName> " unless @ARGV == 2;

my $input=shift;
my $output=shift;

open(OUT,">$output");
open(IN,"$input") || "Can't open file $input\n";
while(my $line=<IN>){
    chomp($line);
    my @line=split/\t/,$line;
    my @Name=split/\_/,$line[0];
    my $Barcode="S".$Name[1];
    print OUT $Barcode."\n";
}
close IN;
close OUT;
