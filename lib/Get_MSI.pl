#/usr/bin/perl

use warnings;
use strict;

my $inputFile = shift;
my $outputFile = shift;

open(OUT, ">$outputFile");
open(IN, "$inputFile") || die "Can't open file $inputFile\n";
while(my $Line = <IN>){
    chomp($Line);
    if($Line =~ /^Total/){
        next;
    }else{
        my @Lines = split/\t/,$Line;
        if(int($Lines[2]) >= 33){
            print OUT "微卫星高度不稳定(MSI-H)\tmsi_h\n";
        }else{
            print OUT "微卫星稳定(MSS)\tmss\n";
        }
    }
}

close IN;
close OUT;
