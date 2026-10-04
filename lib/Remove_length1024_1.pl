#!/usr/bin/perl

use File::Basename;

die "perl $0 <In.fastqDir> <length> <Out.fastqDir> <$Sample>" unless @ARGV == 4;
my $in=shift;
my $length=shift;
my $out=shift;
my $Sample=shift;
   open OUT,">>$out\/IonXpress_$Sample-removelength.fastq";
   open(IN,"$in") || die "Can't open file $in!\n";
    while($ID=<IN>)
      {
      chomp($ID);
      my $a=<IN>;
      chomp($a);
      my $count=length $a;
      $i=<IN>;
      chomp($i);
      $QC=<IN>;
      chomp($QC);
         if ($count<$length)
            {
            print OUT "$ID\n$a\n$i\n$QC\n";
            }
       }
       close IN;
       close OUT;

