#!/usr/bin/perl

use File::Basename;

die "perl $0 <InFastq> <length> <OutFastq>" unless @ARGV == 3;

my $InF = shift;
my $length = shift;
my $OutF = shift;

open(IN,"$InF") || die "Can't open file $InF\n";
open OUT, ">$OutF";
while(my $ID=<IN>){
    chomp($ID);
    my $Seq = <IN>;
    chomp($Seq);
    my $A = <IN>;
    my $Que = <IN>;
    chomp($Que);
    my $Re_len = length($Seq) - $length;
    my $NewSeq = substr($Seq, 0, $Re_len);
    my $NewQue = substr($Que, 0, $Re_len);
    print OUT $ID."\n".$NewSeq."\n"."+"."\n".$NewQue."\n";
}
close IN;
close OUT;
