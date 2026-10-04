#!/usr/bin/perl
#use strict;
use File::Basename;

die "perl $0 <indir> <in2> <in3> <in4> <outdir> <out2>" unless @ARGV==6;

my $in=shift;######R1.fastq
my $in2=shift;#####length
my $seq=shift;#####Seq
my $in3=shift;#####R2.fastq
my $out=shift;
my $out2=shift;
my %hash=();

open(OUT, ">$out");
open(OUTT, ">$out2");
open(IN, "$in") || die "Can't open file $in\n";
while(my $line=<IN>){
    chomp($line);
    my $Seq=<IN>;
    chomp($Seq);
    <IN>;
    my $Qual=<IN>;
    chomp($Qual);
    if(length($Seq) >= int($in2)){
        my $RefSeq = substr($Seq, 1, $in2);
        if($RefSeq eq $seq){
            $hash{$line}=1;
            print OUT $line."\n".$Seq."\n"."+"."\n".$Qual."\n";
        }else{
            next;
        }
    }else{
        next;
    }
}

open(IN2, "$in3") || die "Can't open file $in3\n";
while(my $Line=<IN2>){
    chomp($Line);
    my $SEQ=<IN2>;
    chomp($SEQ);
    <IN2>;
    my $qual=<IN2>;
    chomp($qual);
    my @Line=split/\//,$Line;
    my $ID = $Line[0]."/1";
    if(exists $hash{$ID}){
        print OUTT $Line."\n".$SEQ."\n"."+"."\n".$qual."\n";
    }else{
        next;
    }
}


close IN;
close IN2;
close OUT;
close OUTT;
