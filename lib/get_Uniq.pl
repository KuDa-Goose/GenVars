#!/usr/bin/perl

use strict;
use warnings;

my $in=shift;
my $in2=shift;
my $in3=shift;
my $out=shift;
my $out2=shift;
my %hash=();

open(IN,"$in") || die "Can't open file $in\n";
while(my $line=<IN>){
    chomp($line);
    my @Name = split/\-/,$line;
    my @Number = split/\//,$Name[1];
    $hash{$Name[0]} = $Number[0];
}
close IN;

open(OUT, ">$out");
open(IN2, "$in2") || die "Can't open file $in2\n";
while(my $Line=<IN2>){
    chomp($Line);
    my $Seq=<IN2>;
    my $Str=<IN2>;
    my $Qual=<IN2>;
    my $Lines = (split/\//,$Line)[0];
    my $L = (split/\//,$Line)[1];
    my @Lines = split/\@/,$Lines;
    if(exists $hash{$Lines[1]}){
        print OUT $Lines."-".$hash{$Lines[1]}."/".$L."\n".$Seq.$Str.$Qual;
    }else{
        next;
    }
}
close IN2;
close OUT;

open(OUTT, ">$out2");
open(IN3, "$in3") || die "Can't open file $in3\n";
while(my $Line=<IN3>){
    chomp($Line);
    my $Seq=<IN3>;
    my $Str=<IN3>;
    my $Qual=<IN3>;
    my $Lines = (split/\//,$Line)[0];
    my $L = (split/\//,$Line)[1];
    my @Lines = split/\@/,$Lines;
    if(exists $hash{$Lines[1]}){
        print OUTT $Lines."-".$hash{$Lines[1]}."/".$L."\n".$Seq.$Str.$Qual;
    }else{
        next;
    }
}
close IN3;
close OUTT;

