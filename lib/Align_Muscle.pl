#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;
use List::Util qw/max sum/;
use File::Basename;
use List::Util qw(shuffle);
#use Bio::SeqIO;

my $InputFasta = shift;
my $OutputFile = shift;
my $ErrorLog = shift;
my %hash = ();
my @Len;
my @Name;
my $name;

sub getMax {
    my (%temp, @ret);
    my $max = 0;
    foreach ( @_ ) {
        my $count = $temp{$_}++;
        $max = $count if $count > $max; 
    }
    foreach ( keys %temp ) {
        push @ret, $_ if $temp{$_} == $max + 1;
    }    
    return @ret;
}

open(OUT, ">>$OutputFile");
open(OUTT, ">>$ErrorLog");
#my $InFasta  = Bio::SeqIO->new(-file => $InputFasta ,-format => 'fasta');
#while(my $obj = $InFasta->next_seq()){
#    my $id = $obj->id;
#    my $seq = $obj->seq;
#    my $len = length($seq);
#    $hash{$id} = $seq;
#    push @Len, $len;
#}
my $Sample = (split/\./,$InputFasta)[0];
open(IN,"$InputFasta") || die "Can't open file $InputFasta\n";
while(<IN>){
    chomp;
    if(/^>(\S+)/){
        $name = $1;
    }else{
        $hash{$name} .= $_;
    }
}
foreach my $seq(values %hash){
    push @Len, length($seq);
}

my @ReadsID = keys %hash;
my $MaxLen = max @Len;
my $MainReads = "";
my $MainID = "";
my $MainQuality = "";

############get Main Reads
for(my $i=0; $i<$MaxLen; $i++){
    my @Base;
    foreach my $ID (@ReadsID){
        my $Seq = substr($hash{$ID}, $i, 1);
        push @Base, $Seq;
    }
    my @Max = &getMax(@Base);
    my $count;
    foreach my $B (@Base){
        if($B eq $Max[0]){
            $count++;
        }
    }
    my $AF = $count/(scalar @Base);
    $MainReads .= $Max[0];
    if((scalar @Max) >1){
        print OUTT $Sample."\t".$i."\t".$AF."\n";
    }
}
#$MainReads=~s/-//g;
my %score = ();
while((my $key, my $value) = each %hash){
    #$value=~s/-//g;
    my $Score = 0;
    for(my $j=0; $j<length($value); $j++){
        my $RefBase = substr($MainReads, $j, 1);
        my $SeqBase = substr($value, $j, 1);
        if($RefBase eq $SeqBase){
            $Score += 1;
        }else{
            $Score += 0;
        }
    }
    $score{$key} = $Score;
}
my @keys = sort { $score{$b} <=> $score{$a} } keys %score;

my @Names = split/\//,$keys[0];
print OUT $Names[0]."-".scalar(@ReadsID)."/".$Names[1]."\n";

close OUT;
close OUTT;
