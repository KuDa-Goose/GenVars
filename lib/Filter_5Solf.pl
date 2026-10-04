#!/usr/bin/perl

use warnings;
use strict;
use File::Basename;

my $in = shift;
my $out = shift;
my %hash = ();

open(IN, "$in") || die "Can't open file $in\n";
open(OUT, ">$out");
while(my $line = <IN>){
    chomp($line);
    if($line=~/^@/){
        next;
    }else{
        my @lines = split/\t/,$line;
        if($lines[5]=~/^(\d+)S/){
            my $S = $1;
	    if($S>3){
                $hash{$lines[0]}=1;
	    }else{
                next;
	    }
        }else{
            next;
	}
    }
}

open(IN2, "$in") || die "Can't open file $in\n";
while(my $line = <IN2>){
    chomp($line);
    if($line=~/^@/){
        print OUT $line."\n";
    }else{
        my @lines = split/\t/,$line;
        if(exists $hash{$lines[0]}){
            next;
        }else{
            print OUT $line."\n";
        }
    }
}

close IN;
close OUT;
