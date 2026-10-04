#!/usr/bin/perl
#use strict;
use File::Basename;

die "perl $0 <indir> <outdir>" unless @ARGV==2;

my $in=shift;
my $out=shift;
my %hash=();

#print "Sample\tDel1_Ref\tDel1_Mut\tDel1_AF\tDel2_Ref\tDel2_Mut\tDel2_AF\n";


my @file1=`ls $in/Sample*/Step3Variant/*.indel.vcf`;
#print $file1[0];
for(my $a=0;$a<@file1;$a++){
  chomp($file1[$a]);
  my $sample=(split/\/Step3/,$file1[$a])[0];
#  print $sample."\n";
  $sample=(split/\//,$sample)[-1];
# print $sample."\n";
  open(OUT,">$out");
print OUT "Sample\tDel1_Ref\tDel1_Mut\tDel1_AF\tDel2_Ref\tDel2_Mut\tDel2_AF\n";
  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref,$mut,$AF)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55242464 && $line[3] eq "AGGAATTAAGAGAAGC" && $line[4] eq "A")
  {
  my @symbol=split/:/,"$line[8]";
  my @count=split/:/,"$line[9]";
   $ref=$count[4];
  $mut=$count[5];
  $AF=$count[6];

  }
}
close IN;


  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref1,$mut1,$AF1)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55242465 && $line[3] eq "GGAATTAAGAGAAGCA" && $sline[4] eq "G" )
  {
  my @symbol1=split/:/,"$line[8]";
  my @count1=split/:/,"$line[9]";
   $ref1=$count1[4];
  $mut1=$count1[5];
  $AF1=$count1[6];

  }
}
close IN;



 if(defined $hash{$sample})
{  
$hash{$sample}="$hash{$sample}\t$ref\t$mut\t$AF\t$ref1\t$mut1\t$AF1";
}
else {$hash{$sample}="$ref\t$mut\t$AF\t$ref1\t$mut1\t$AF1";}

}


foreach my $key(keys %hash)

{
my @data=split/\t/,$hash{$key};
my $Del1_ref=$data[0];
my $Del1_mut=$data[1];
my $Del1_AF=$data[2];
my $Del2_ref=$data[3];
my $Del2_mut=$data[4];
my $Del2_AF=$data[5];

print OUT "$key\t$Del1_ref\t$Del1_mut\t$Del1_AF\t$Del2_ref\t$Del2_mut\t$Del2_AF\n";


}



#print @file1;




   



