#!/usr/bin/perl
use strict;
use File::Basename;

die "perl $0 <indir> <outdir>" unless @ARGV==2;

my $in=shift;
my $out=shift;
my %hash=();

#print "Sample\tL858R_Ref\tL858R_Mut\tL858R_AF\tT790M_Ref\tT790M_Mut\tT790M_AF\n";


my @file1=`ls $in/Sample*/Step2Alignment/*.deep`;
#print $file1[0];
for(my $a=0;$a<@file1;$a++){
  chomp($file1[$a]);
  my $sample=(split/\/Step2/,$file1[$a])[0];
#  print $sample."\n";
  $sample=(split/\//,$sample)[-1];
# print $sample."\n";
  open(OUT,">$out");
print OUT "Sample\tL858R_Ref\tT790M_Ref\tEGFR_G719S_Ref\tEGFR_S768I_Ref\tEGFR_L858R14_Ref\tEGFR_L858R16_Ref\tKRAS_G12S_Ref\tKRAS_G12C_Ref\tKRAS_G12D_Ref\tKRAS_G12A_Ref\tKRAS_G12V_Ref\tKRAS_G13D_Ref\tNRAS_G12D_Ref\tNRAS_Q61K_Ref\tNRAS_Q61R_Ref\tBRAF_V600E_Ref\tBRAF_V600E61_Ref\tBRAF_V600E62_Ref\tPIK3CA_H1047R_Ref\tQ787Q_Ref\t19Del_1_Ref\t19Del_2_Ref\n";
  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55259515)
  {
 my @count=@line;
 # my @symbol=split/:/,"$line[8]";
  #my @count=split/:/,"$line[9]";
  $ref=$count[2];
  #$mut=$count[5];
  #$AF=$count[6];

  }
}
close IN;


  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref1=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55249071 )
  {
  #my @symbol1=split/:/,"$line[8]";
  #my @count1=split/:/,"$line[9]";
  my @count1=@line;
  $ref1=$count1[2];
  #$mut1=$count1[5];
  #$AF1=$count1[6];

  }
}
close IN;

  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref2=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55241707 )
  {
  #my @symbol2=split/:/,"$line[8]";
  #my @count2=split/:/,"$line[9]";
  my @count2=@line;
  $ref2=$count2[2];
  #$mut2=$count2[5];
  #$AF2=$count2[6];

  }
}
close IN;

  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref3=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55249005 )
  {
  #my @symbol3=split/:/,"$line[8]";
  #my @count3=split/:/,"$line[9]";
  my @count3=@line;
  $ref3=$count3[2];
  #$mut3=$count3[5];
  #$AF3=$count3[6];

  }
}
close IN;

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref4=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55259514 )
  {
  #my @symbol4=split/:/,"$line[8]";
  #my @count4=split/:/,"$line[9]";
  my @count4=@line;
  $ref4=$count4[2];
  #$mut4=$count4[5];
  #$AF4=$count4[6];

  }
}
close IN;

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref5=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55259516 )
  {
  #my @symbol5=split/:/,"$line[8]";
  #my @count5=split/:/,"$line[9]";
  my @count5=@line;
  $ref5=$count5[2];
  #$mut5=$count5[5];
  #$AF5=$count5[6];

  }
}
close IN;
###################################################KRAS_G12S

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref6=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398285 )
  {
  #my @symbol6=split/:/,"$line[8]";
  #my @count6=split/:/,"$line[9]";
  my @count6=@line;
  $ref6=$count6[2];
  #$mut6=$count6[5];
  #$AF6=$count6[6];

  }
}
close IN;
#####################################################KRAS_G12D
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref7=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398285 )
  {
  #my @symbol7=split/:/,"$line[8]";
  #my @count8=split/:/,"$line[9]";
  my @count7=@line;
  $ref7=$count7[2];
  #$mut8=$count8[5];
  #$AF8=$count8[6];

  }
}
close IN;
#####################################################KRAS_G12D

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref8=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398284)
  {
  #my @symbol8=split/:/,"$line[8]";
  #my @count8=split/:/,"$line[9]";
  my @count8=@line;
  $ref8=$count8[2];
  #$mut8=$count8[5];
  #$AF8=$count8[6];

  }
}
close IN;
###################################################KRAS_G12A
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref9=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398284)
  {
 # my @symbol9=split/:/,"$line[8]";
 # my @count9=split/:/,"$line[9]";
  my @count9=@line;
  $ref9=$count9[2];
  #$mut9=$count9[5];
  #$AF9=$count9[6];

  }
}
close IN;
#########################################################KRAS_G12V
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref10=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398284)
  {
  #my @symbol10=split/:/,"$line[8]";
  #my @count10=split/:/,"$line[9]";
  my @count10=@line;
  $ref10=$count10[2];
  #$mut10=$count10[5];
  #$AF10=$count10[6];

  }
}
close IN;
#######################################################################G13_D
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref11=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398281)
  {
  #my @symbol11=split/:/,"$line[8]";
  #my @count11=split/:/,"$line[9]";
  my @count11=@line;
  $ref11=$count11[2];
  #$mut11=$count11[5];
  #$AF11=$count11[6];

  }
}
close IN;
########################################################NRAS_G12D
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref12=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr1" && $line[1]==115258747 )
  {
 # my @symbol12=split/:/,"$line[8]";
  #my @count12=split/:/,"$line[9]";
  my @count12=@line;
  $ref12=$count12[2];
#  $mut12=$count12[5];
#  $AF12=$count12[6];

  }
}
close IN;
#########################################################NRAS_Q61K

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref13=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr1" && $line[1]==115256530 )
  {
  #my @symbol13=split/:/,"$line[8]";
  #my @count13=split/:/,"$line[9]";
  my @count13=@line;
  $ref13=$count13[2];
  #$mut13=$count13[5];
  #$AF13=$count13[6];

  }
}
close IN;
##############################################################NRAS_Q61R

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref14=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr1" && $line[1]==115256529 )
  {
  #my @symbol14=split/:/,"$line[8]";
  #my @count14=split/:/,"$line[9]";
  my @count14=@line;
  $ref14=$count14[2];
  #$mut14=$count14[5];
  #$AF14=$count14[6];

  }
}
close IN;
######################################################################BRAF_V600E
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref15=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==140453135 )
  {
  #my @symbol15=split/:/,"$line[8]";
  #my @count15=split/:/,"$line[9]";
  my @count15=@line;
  $ref15=$count15[2];
  #$mut15=$count15[5];
  #$AF15=$count15[6];

  }
}
close IN;
#############################################################BRAF_V600E61
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref16=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==140453136 )
  {
  #my @symbol16=split/:/,"$line[8]";
  #my @count16=split/:/,"$line[9]";
  my @count16=@line;
  $ref16=$count16[2];
  #$mut16=$count16[5];
  #$AF16=$count16[6];

  }
}
close IN;
###############################################################BRAF_V600E62
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref17=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==140453136)
  {
 # my @symbol17=split/:/,"$line[8]";
  #my @count17=split/:/,"$line[9]";
  my @count17=@line;
  $ref17=$count17[2];
  #$mut17=$count17[5];
  #$AF17=$count17[6];

  }
}
close IN;
#####################################################################PIK3CA_H1047R
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref18=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr3" && $line[1]==178952085 )
  {
  #my @symbol18=split/:/,"$line[8]";
  #my @count18=split/:/,"$line[9]";
  my @count18=@line;
  $ref18=$count18[2];
  #$mut18=$count18[5];
  #$AF18=$count18[6];

  }
}
close IN;
#####################################################################
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref19=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55249063 )
  {
  #my @symbol18=split/:/,"$line[8]";
  #my @count18=split/:/,"$line[9]";
  my @count19=@line;
  $ref19=$count19[2];
  #$mut18=$count18[5];
  #$AF18=$count18[6];

  }
}
close IN;
#######################################################
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref20=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55242464 )
  {
  #my @symbol18=split/:/,"$line[8]";
  #my @count18=split/:/,"$line[9]";
  my @count20=@line;
  $ref20=$count20[2];
  #$mut18=$count18[5];
  #$AF18=$count18[6];

  }
}
close IN;

####################################################
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my $ref21=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55242465 )
  {
  #my @symbol18=split/:/,"$line[8]";
  #my @count18=split/:/,"$line[9]";
  my @count21=@line;
  $ref21=$count21[2];
  #$mut18=$count18[5];
  #$AF18=$count18[6];

  }
}
close IN;

##################

 if(defined $hash{$sample})
{
$hash{$sample}="$hash{$sample}\t$ref\t$ref1\t$ref2\t$ref3\t$ref4\t$ref5\t$ref6\t$ref7\t$ref8\t$ref9\t$ref10\t$ref11\t$ref12\t$ref13\t$ref14\t$ref15\t$ref16\t$ref17\t$ref18\t$ref19\t$ref20\t$ref21";
}
else {$hash{$sample}="$ref\t$ref1\t$ref2\t$ref3\t$ref4\t$ref5\t$ref6\t$ref7\t$ref8\t$ref9\t$ref10\t$ref11\t$ref12\t$ref13\t$ref14\t$ref15\t$ref16\t$ref17\t$ref18\t$ref19\t$ref20\t$ref21";}

}


foreach my $key(keys %hash)

{
my @data=split/\t/,$hash{$key};
my $L858R_Ref=$data[0];
#my $L858R_mut=$data[1];
#my $L858R_AF=$data[2];
my $T790M_Ref=$data[1];
#my $T790M_mut=$data[4];
#my $T790M_AF=$data[5];
my $EGFR_G719S_Ref=$data[2];
#my $EGFR_G719S_Mut=$data[7];
#my $EGFR_G719S_AF=$data[8];
my $EGFR_S768I_Ref=$data[3];
#my $EGFR_S768I_Mut=$data[10];
#my $EGFR_S768I_AF=$data[11];
my $EGFR_L858R14_Ref=$data[4];
#my $EGFR_L858R14_Mut=$data[13];
#my $EGFR_L858R14_AF=$data[14];
my $EGFR_L858R16_Ref=$data[5];
#my $EGFR_L858R16_Mut=$data[16];
#my $EGFR_L858R16_AF=$data[17];
my $KRAS_G12S_Ref=$data[6];
#my $KRAS_G12S_Mut=$data[19];
#my $KRAS_G12S_AF=$data[20];
my $KRAS_G12C_Ref=$data[7];
#my $KRAS_G12C_Mut=$data[22];
#my $KRAS_G12C_AF=$data[23];
my $KRAS_G12D_Ref=$data[8];
#my $KRAS_G12D_Mut=$data[25];
#my $KRAS_G12D_AF=$data[26];
my $KRAS_G12A_Ref=$data[9];
#my $KRAS_G12A_Mut=$data[28];
#my $KRAS_G12A_AF=$data[29];
my $KRAS_G12V_Ref=$data[10];
#my $KRAS_G12V_Mut=$data[31];
#my $KRAS_G12V_AF=$data[32];
my $KRAS_G13D_Ref=$data[11];
#my $KRAS_G13D_Mut=$data[34];
#my $KRAS_G13D_AF=$data[35];
my $NRAS_G12D_Ref=$data[12];
#my $NRAS_G12D_Mut=$data[37];
#my $NRAS_G12D_AF=$data[38];
my $NRAS_Q61K_Ref=$data[13];
#my $NRAS_Q61K_Mut=$data[40];
#my $NRAS_Q61K_AF=$data[41];
my $NRAS_Q61R_Ref=$data[14];
#my $NRAS_Q61R_Mut=$data[43];
#my $NRAS_Q61R_AF=$data[44];
my $BRAF_V600E_Ref=$data[15];
#my $BRAF_V600E_Mut=$data[46];
#my $BRAF_V600E_AF=$data[47];
my $BRAF_V600E61_Ref=$data[16];
#my $BRAF_V600E61_Mut=$data[49];
#my $BRAF_V600E61_AF=$data[50];
my $BRAF_V600E62_Ref=$data[17];
#my $BRAF_V600E62_Mut=$data[52];
#my $BRAF_V600E62_AF=$data[53];
my $PIK3CA_H1047R_Ref=$data[18];
#my $PIK3CA_H1047R_Mut=$data[55];
#my $PIK3CA_H1047R_AF=$data[56];
my $Q787Q_Ref=$data[19];
my $Del_1_Ref=$data[20];
my $Del_2_Ref=$data[21];

print OUT "$key\t$L858R_Ref\t$T790M_Ref\t$EGFR_G719S_Ref\t$EGFR_S768I_Ref\t$EGFR_L858R14_Ref\t$EGFR_L858R16_Ref\t$KRAS_G12S_Ref\t$KRAS_G12C_Ref\t$KRAS_G12D_Ref\t$KRAS_G12A_Ref\t$KRAS_G12V_Ref\t$KRAS_G13D_Ref\t$NRAS_G12D_Ref\t$NRAS_Q61K_Ref\t$NRAS_Q61R_Ref\t$BRAF_V600E_Ref\t$BRAF_V600E61_Ref\t$BRAF_V600E62_Ref\t$PIK3CA_H1047R_Ref\t$Q787Q_Ref\t$Del_1_Ref\t$Del_2_Ref\n";


}

