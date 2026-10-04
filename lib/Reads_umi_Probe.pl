#!/usr/bin/perl

use warnings;
use strict;
use File::Basename;

=begin get parameter from arguments

$reads_TXT is input file
$OUTFILE   is output file

=end
=cut

my $reads_TXT=shift;
my $probeName=shift;
my $OUTFILE=shift;

my $i=0;
my @mm=();

#my @headers = qw(Sample_name Probe1 Probe2 Probe3 Probe4 Probe5 Probe6 Probe7 Probe1_ontarget Probe2_ontarget Probe3_ontarget Probe4_ontarget Probe5_ontarget Probe6_ontarget Probe7_ontarget);
open(OUT,">$OUTFILE");
open(IN,"<$probeName") || die $!;

my @h_ontarget = ();
my @h_umiuniq = ();
while(<IN>){
    chomp;
    my @headers = split(/ /,$_);
    #my @h_ontarget = map { $_."_ontarget" }@headers;
    foreach my $p_name (@headers){
        my $p_target = $p_name."_ontarget";
        push @h_ontarget, $p_target;
    }
    foreach my $P_name (@headers){
        my $P_target = $P_name."_umiuniq";
        push @h_umiuniq, $P_target;
    }

    print OUT "\t".join("\t", @h_ontarget)."\t".join("\t", @h_umiuniq)."\n";
    }
close IN;
#print OUT "\t".join("\t", @headers)."\t".join("\t", @h_ontarget);    
open(IN2,"<$reads_TXT") || die $!;
while(<IN2>){
    if ($_=~/(\d+)\s+/){
        $mm[$i]=$1/4;
        $i++;
    }
}

my $TXT_name = basename($reads_TXT);
(my $Sample= $TXT_name) =~ s/.txt$//;

print OUT "S".$Sample."\t".join("\t", @mm)."\n";

close IN2;
close OUT;

