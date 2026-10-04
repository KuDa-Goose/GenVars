#/usr/bin/perl

use warnings;
use strict;

my $inputFile = shift;
my $outputFile = shift;
my @LineLen;

open(OUT, ">$outputFile");
open(IN, "$inputFile") || die "Can't open file $inputFile\n";
while(my $Line = <IN>){
    chomp($Line);
    my @Line = split/\t/,$Line;
    push @LineLen, $Line[0];
}

print OUT "##".(scalar @LineLen)."\n";
open(IN2, "$inputFile") || die "Can't open file $inputFile\n";
while(my $Line = <IN2>){
    chomp($Line);
    my @Lines = split/\t/,$Line;
    print OUT $Lines[0]."__".$Lines[1]."\t".$Lines[2]."\t".$Lines[3]."\n";
}

close IN;
close OUT;
