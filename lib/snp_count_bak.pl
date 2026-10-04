#!/usr/bin/perl
#use strict;
use File::Basename;

die "perl $0 <indir> <outdir>" unless @ARGV==2;

my $in=shift;
my $out=shift;
my %hash=();

#print "Sample\tL858R_Ref\tL858R_Mut\tL858R_AF\tT790M_Ref\tT790M_Mut\tT790M_AF\n";


my @file1=`ls $in/Sample*/Step3Variant/*_pileup.snp.vcf`;
#print $file1[0];
for(my $a=0;$a<@file1;$a++){
  chomp($file1[$a]);
  my $sample=(split/\/Step3/,$file1[$a])[0];
#  print $sample."\n";
  $sample=(split/\//,$sample)[-1];
# print $sample."\n";
  open(OUT,">$out");
print OUT "Sample\tL858R_Ref\tL858R_Mut\tL858R_AF\tT790M_Ref\tT790M_Mut\tT790M_AF\tEGFR_G719S_Ref\tEGFR_G719S_Mut\tEGFR_G719S_AF\tEGFR_S768I_Ref\tEGFR_S768I_Mut\tEGFR_S768I_AF\tEGFR_L858R14_Ref\tEGFR_L858R14_Mut\tEGFR_L858R14_AF\tEGFR_L858R16_Ref\tEGFR_L858R16_Mut\tEGFR_L858R16_AF\tKRAS_G12S_Ref\tKRAS_G12S_Mut\tKRAS_G12S_AF\tKRAS_G12C_Ref\tKRAS_G12C_Mut\tKRAS_G12C_AF\tKRAS_G12D_Ref\tKRAS_G12D_Mut\tKRAS_G12D_AF\tKRAS_G12A_Ref\tKRAS_G12A_Mut\tKRAS_G12A_AF\tKRAS_G12V_Ref\tKRAS_G12V_Mut\tKRAS_G12V_AF\tKRAS_G13D_Ref\tKRAS_G13D_Mut\tKRAS_G13D_AF\tNRAS_G12D_Ref\tNRAS_G12D_Mut\tNRAS_G12D_AF\tNRAS_Q61K_Ref\tNRAS_Q61K_Mut\tNRAS_Q61K_AF\tNRAS_Q61R_Ref\tNRAS_Q61R_Mut\tNRAS_Q61R_AF\tBRAF_V600E_Ref\tBRAF_V600E_Mut\tBRAF_V600E_AF\tBRAF_V600E61_Ref\tBRAF_V600E61_Mut\tBRAF_V600E61_AF\tBRAF_V600E62_Ref\tBRAF_V600E62_Mut\tBRAF_V600E62_AF\tPIK3CA_H1047R_Ref\tPIK3CA_H1047R_Mut\tPIK3CA_H1047R_AF\tQ787Q_Ref\tQ787Q_Mut\tQ787Q_AF\n";
  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref,$mut,$AF)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55259515 && $line[2] eq "T" && $line[3] eq "G")
  {
  my @count=@line;
 # my @symbol=split/:/,"$line[8]";
  #my @count=split/:/,"$line[9]";
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
  if($line[0] eq "chr7" && $line[1]==55249071 && $line[2] eq "C" && $line[3] eq "T")
  {
  #my @symbol1=split/:/,"$line[8]";
  #my @count1=split/:/,"$line[9]";
  my @count1=@line;
  $ref1=$count1[4];
  $mut1=$count1[5];
  $AF1=$count1[6];

  }
}
close IN;

  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref2,$mut2,$AF2)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55241707 && $line[2] eq "G" && $line[3] eq "A")
  {
  #my @symbol2=split/:/,"$line[8]";
  #my @count2=split/:/,"$line[9]";
  my @count2=@line;
  $ref2=$count2[4];
  $mut2=$count2[5];
  $AF2=$count2[6];

  }
}
close IN;

  open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref3,$mut3,$AF3)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55249005 && $line[2] eq "G" && $line[3] eq "T")
  {
  #my @symbol3=split/:/,"$line[8]";
  #my @count3=split/:/,"$line[9]";
  my @count3=@line;
  $ref3=$count3[4];
  $mut3=$count3[5];
  $AF3=$count3[6];

  }
}
close IN;

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref4,$mut4,$AF4)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55259514 && $line[2] eq "C" && $line[3] eq "A")
  {
  #my @symbol4=split/:/,"$line[8]";
  #my @count4=split/:/,"$line[9]";
  my @count4=@line;
  $ref4=$count4[4];
  $mut4=$count4[5];
  $AF4=$count4[6];

  }
}
close IN;

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref5,$mut5,$AF5)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55259516 && $line[2] eq "G" && $line[3] eq "T")
  {
  #my @symbol5=split/:/,"$line[8]";
  #my @count5=split/:/,"$line[9]";
  my @count5=@line;
  $ref5=$count5[4];
  $mut5=$count5[5];
  $AF5=$count5[6];

  }
}
close IN;
###################################################KRAS_G12S

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref6,$mut6,$AF6)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398285 && $line[2] eq "C" && $line[3] eq "T")
  {
  #my @symbol6=split/:/,"$line[8]";
  #my @count6=split/:/,"$line[9]";
  my @count6=@line;
  $ref6=$count6[4];
  $mut6=$count6[5];
  $AF6=$count6[6];

  }
}
close IN;
#######################################################KRAS_G12C

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref7,$mut7,$AF7)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398285 && $line[2] eq "C" && $line[3] eq "A")
  {
  #my @symbol7=split/:/,"$line[8]";
  #my @count7=split/:/,"$line[9]";
  my @count7=@line;
  $ref7=$count7[4];
  $mut7=$count7[5];
  $AF7=$count7[6];

  }
}
close IN;
#####################################################KRAS_G12D

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref8,$mut8,$AF8)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398284 && $line[2] eq "C" && $line[3] eq "T")
  {
  #my @symbol8=split/:/,"$line[8]";
  #my @count8=split/:/,"$line[9]";
  my @count8=@line;
  $ref8=$count8[4];
  $mut8=$count8[5];
  $AF8=$count8[6];

  }
}
close IN;
###################################################KRAS_G12A
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref9,$mut9,$AF9)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398284 && $line[2] eq "C" && $line[3] eq "G")
  {
  #my @symbol9=split/:/,"$line[8]";
  #my @count9=split/:/,"$line[9]";
  my @count9=@line;
  $ref9=$count9[4];
  $mut9=$count9[5];
  $AF9=$count9[6];

  }
}
close IN;
#########################################################KRAS_G12V
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref10,$mut10,$AF10)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398284 && $line[2] eq "C" && $line[3] eq "A")
  {
  #my @symbol10=split/:/,"$line[8]";
  #my @count10=split/:/,"$line[9]";
  my @count10=@line;
  $ref10=$count10[4];
  $mut10=$count10[5];
  $AF10=$count10[6];

  }
}
close IN;
#######################################################################G13_D
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref11,$mut11,$AF11)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr12" && $line[1]==25398281 && $line[2] eq "C" && $line[3] eq "T")
  {
  #my @symbol11=split/:/,"$line[8]";
  #my @count11=split/:/,"$line[9]";
  my @count11=@line;
  $ref11=$count11[4];
  $mut11=$count11[5];
  $AF11=$count11[6];

  }
}
close IN;
########################################################NRAS_G12D
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref12,$mut12,$AF12)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr1" && $line[1]==115258747 && $line[2] eq "C" && $line[3] eq "T")
  {
  #my @symbol12=split/:/,"$line[8]";
  #my @count12=split/:/,"$line[9]";
  my @count12=@line;
  $ref12=$count12[4];
  $mut12=$count12[5];
  $AF12=$count12[6];

  }
}
close IN;
#########################################################NRAS_Q61K

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref13,$mut13,$AF13)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr1" && $line[1]==115256530 && $line[2] eq "G" && $line[3] eq "T")
  {
  #my @symbol13=split/:/,"$line[8]";
  #my @count13=split/:/,"$line[9]";
  my @count13=@line;
  $ref13=$count13[4];
  $mut13=$count13[5];
  $AF13=$count13[6];

  }
}
close IN;
##############################################################NRAS_Q61R

 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref14,$mut14,$AF14)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr1" && $line[1]==115256529 && $line[2] eq "T" && $line[3] eq "C")
  {
  #my @symbol14=split/:/,"$line[8]";
  #my @count14=split/:/,"$line[9]";
  my @count14=@line;
  $ref14=$count14[4];
  $mut14=$count14[5];
  $AF14=$count14[6];

  }
}
close IN;
######################################################################BRAF_V600E
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref15,$mut15,$AF15)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==140453135 && $line[2] eq "C" && $line[3] eq "T")
  {
  #my @symbol15=split/:/,"$line[8]";
  #my @count15=split/:/,"$line[9]";
  my @count15=@line;
  $ref15=$count15[4];
  $mut15=$count15[5];
  $AF15=$count15[6];

  }
}
close IN;
#############################################################BRAF_V600E61
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref16,$mut16,$AF16)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==140453136 && $line[2] eq "A" && $line[3] eq "T")
  {
  #my @symbol16=split/:/,"$line[8]";
  #my @count16=split/:/,"$line[9]";
  my @count16=@line;
  $ref16=$count16[4];
  $mut16=$count16[5];
  $AF16=$count16[6];

  }
}
close IN;
###############################################################BRAF_V600E62
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref17,$mut17,$AF17)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==140453136 && $line[2] eq "A" && $line[3] eq "T")
  {
  #my @symbol17=split/:/,"$line[8]";
  #my @count17=split/:/,"$line[9]";
  my @count17=@line;
  $ref17=$count17[4];
  $mut17=$count17[5];
  $AF17=$count17[6];

  }
}
close IN;
#####################################################################PIK3CA_H1047R
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref18,$mut18,$AF18)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr3" && $line[1]==178952085 && $line[2] eq "A" && $line[3] eq "G")
  {
  #my @symbol18=split/:/,"$line[8]";
  #my @count18=split/:/,"$line[9]";
  my @count18=@line;
  $ref18=$count18[4];
  $mut18=$count18[5];
  $AF18=$count18[6];

  }
}
close IN;
#####################################################################Q787Q
 open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
  my  ($ref19,$mut19,$AF19)=0;

  while(<IN>)
{
  chomp;
  $_=~s/\s+/\t/g;
  my @line=split/\t/,$_;
  if($line[0] eq "chr7" && $line[1]==55249063 && $line[2] eq "G" && $line[3] eq "A")
  {
  #my @symbol18=split/:/,"$line[8]";
  #my @count18=split/:/,"$line[9]";
  my @count19=@line;
  $ref19=$count19[4];
  $mut19=$count19[5];
  $AF19=$count19[6];

  }
}
close IN;
##############################################################
 if(defined $hash{$sample})
{
$hash{$sample}="$hash{$sample}\t$ref\t$mut\t$AF\t$ref1\t$mut1\t$AF1\t$ref2\t$mut2\t$AF2\t$ref3\t$mut3\t$AF3\t$ref4\t$mut4\t$AF4\t$ref5\t$mut5\t$AF5\t$ref6\t$mut6\t$AF6\t$ref7\t$mut7\t$AF7\t$ref8\t$mut8\t$AF8\t$ref9\t$mut9\t$AF9\t$ref10\t$mut10\t$AF10\t$ref11\t$mut11\t$AF11\t$ref12\t$mut12\t$AF12\t$ref13\t$mut13\t$AF13\t$ref14\t$mut14\t$AF14\t$ref15\t$mut15\t$AF15\t$ref16\t$mut16\t$AF16\t$ref17\t$mut17\t$AF17\t$ref18\t$mut18\t$AF18\t$ref19\t$mut19\t$AF19";
}
else {$hash{$sample}="$ref\t$mut\t$AF\t$ref1\t$mut1\t$AF1\t$ref2\t$mut2\t$AF2\t$ref3\t$mut3\t$AF3\t$ref4\t$mut4\t$AF4\t$ref5\t$mut5\t$AF5\t$ref6\t$mut6\t$AF6\t$ref7\t$mut7\t$AF7\t$ref8\t$mut8\t$AF8\t$ref9\t$mut9\t$AF9\t$ref10\t$mut10\t$AF10\t$ref11\t$mut11\t$AF11\t$ref12\t$mut12\t$AF12\t$ref13\t$mut13\t$AF13\t$ref14\t$mut14\t$AF14\t$ref15\t$mut15\t$AF15\t$ref16\t$mut16\t$AF16\t$ref17\t$mut17\t$AF17\t$ref18\t$mut18\t$AF18\t$ref19\t$mut19\t$AF19";}

}


foreach my $key(keys %hash)

{
my @data=split/\t/,$hash{$key};
my $L858R_ref=$data[0];
my $L858R_mut=$data[1];
my $L858R_AF=$data[2];
my $T790M_ref=$data[3];
my $T790M_mut=$data[4];
my $T790M_AF=$data[5];
my $EGFR_G719S_Ref=$data[6];
my $EGFR_G719S_Mut=$data[7];
my $EGFR_G719S_AF=$data[8];
my $EGFR_S768I_Ref=$data[9];
my $EGFR_S768I_Mut=$data[10];
my $EGFR_S768I_AF=$data[11];
my $EGFR_L858R14_Ref=$data[12];
my $EGFR_L858R14_Mut=$data[13];
my $EGFR_L858R14_AF=$data[14];
my $EGFR_L858R16_Ref=$data[15];
my $EGFR_L858R16_Mut=$data[16];
my $EGFR_L858R16_AF=$data[17];
my $KRAS_G12S_Ref=$data[18];
my $KRAS_G12S_Mut=$data[19];
my $KRAS_G12S_AF=$data[20];
my $KRAS_G12C_Ref=$data[21];
my $KRAS_G12C_Mut=$data[22];
my $KRAS_G12C_AF=$data[23];
my $KRAS_G12D_Ref=$data[24];
my $KRAS_G12D_Mut=$data[25];
my $KRAS_G12D_AF=$data[26];
my $KRAS_G12A_Ref=$data[27];
my $KRAS_G12A_Mut=$data[28];
my $KRAS_G12A_AF=$data[29];
my $KRAS_G12V_Ref=$data[30];
my $KRAS_G12V_Mut=$data[31];
my $KRAS_G12V_AF=$data[32];
my $KRAS_G13D_Ref=$data[33];
my $KRAS_G13D_Mut=$data[34];
my $KRAS_G13D_AF=$data[35];
my $NRAS_G12D_Ref=$data[36];
my $NRAS_G12D_Mut=$data[37];
my $NRAS_G12D_AF=$data[38];
my $NRAS_Q61K_Ref=$data[39];
my $NRAS_Q61K_Mut=$data[40];
my $NRAS_Q61K_AF=$data[41];
my $NRAS_Q61R_Ref=$data[42];
my $NRAS_Q61R_Mut=$data[43];
my $NRAS_Q61R_AF=$data[44];
my $BRAF_V600E_Ref=$data[45];
my $BRAF_V600E_Mut=$data[46];
my $BRAF_V600E_AF=$data[47];
my $BRAF_V600E61_Ref=$data[48];
my $BRAF_V600E61_Mut=$data[49];
my $BRAF_V600E61_AF=$data[50];
my $BRAF_V600E62_Ref=$data[51];
my $BRAF_V600E62_Mut=$data[52];
my $BRAF_V600E62_AF=$data[53];
my $PIK3CA_H1047R_Ref=$data[54];
my $PIK3CA_H1047R_Mut=$data[55];
my $PIK3CA_H1047R_AF=$data[56];
my $Q787Q_ref=$data[57];
my $Q787Q_mut=$data[58];
my $Q787Q_AF=$data[59];




print OUT "$key\t$L858R_ref\t$L858R_mut\t$L858R_AF\t$T790M_ref\t$T790M_mut\t$T790M_AF\t$EGFR_G719S_Ref\t$EGFR_G719S_Mut\t$EGFR_G719S_AF\t$EGFR_S768I_Ref\t$EGFR_S768I_Mut\t$EGFR_S768I_AF\t$EGFR_L858R14_Ref\t$EGFR_L858R14_Mut\t$EGFR_L858R14_AF\t$EGFR_L858R16_Ref\t$EGFR_L858R16_Mut\t$EGFR_L858R16_AF\t$KRAS_G12S_Ref\t$KRAS_G12S_Mut\t$KRAS_G12S_AF\t$KRAS_G12C_Ref\t$KRAS_G12C_Mut\t$KRAS_G12C_AF\t$KRAS_G12D_Ref\t$KRAS_G12D_Mut\t$KRAS_G12D_AF\t$KRAS_G12A_Ref\t$KRAS_G12A_Mut\t$KRAS_G12A_AF\t$KRAS_G12V_Ref\t$KRAS_G12V_Mut\t$KRAS_G12V_AF\t$KRAS_G13D_Ref\t$KRAS_G13D_Mut\t$KRAS_G13D_AF\t$NRAS_G12D_Ref\t$NRAS_G12D_Mut\t$NRAS_G12D_AF\t$NRAS_Q61K_Ref\t$NRAS_Q61K_Mut\t$NRAS_Q61K_AF\t$NRAS_Q61R_Ref\t$NRAS_Q61R_Mut\t$NRAS_Q61R_AF\t$BRAF_V600E_Ref\t$BRAF_V600E_Mut\t$BRAF_V600E_AF\t$BRAF_V600E61_Ref\t$BRAF_V600E61_Mut\t$BRAF_V600E61_AF\t$BRAF_V600E62_Ref\t$BRAF_V600E62_Mut\t$BRAF_V600E62_AF\t$PIK3CA_H1047R_Ref\t$PIK3CA_H1047R_Mut\t$PIK3CA_H1047R_AF\t$Q787Q_ref\t$Q787Q_mut\t$Q787Q_AF\n";


}



#print @file1;
