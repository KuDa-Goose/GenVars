#!/usr/bin/perl

use warnings;
use strict;

my $InputFile=shift;
my $InputProbe=shift;
my $InputSam=shift;
my $OutputFile=shift;
my %hash = ();
my %Reads = ();

open(IN3,"$InputSam") || die "Can't open file $InputSam\n";
while(my $Line=<IN3>){
    chomp($Line);
    my @Lines = split/\t/,$Line;
    $Line=~/RG:Z:(\w+)/;
    my $ID=$1;
    $Line=~/MI:Z:(\d+)/;
    my $Number=$1;
    my $UMIID=$ID.":".$Number;
    $hash{$UMIID}.=$Lines[0]."\t";
}

my @UMI = keys %hash;
foreach my $UMI(@UMI){
    my @ID = split/\t/,$hash{$UMI};
    my $IDNumber = scalar(@ID)-1;
    $Reads{$UMI} = $IDNumber;
}


open(OUT, ">$OutputFile");
open(IN,"$InputFile") || die "Can't open file $InputFile\n";
while(my $Line=<IN>){
    chomp($Line);
    if($Line=~/^@/){
        print OUT $Line."\n";
    }else{
        my @Lines = split/\t/,$Line;
        my $ID = $Lines[0]."_".$InputProbe."-".$Reads{$Lines[0]};
        my $Len = scalar @Lines - 1;
        my @Info = @Lines[1..$Len];
        my $Info =  join("\t",@Info);
        print OUT $ID."\t".$Info."\n";
    }
}

close IN;
close OUT;
