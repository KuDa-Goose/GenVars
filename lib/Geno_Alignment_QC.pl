#!/usr/bin/perl -w
use strict;
use File::Basename;

die "perl $0 <indir> <sample> <ontarget_bed> <uniformity.bed>" unless @ARGV==4;

my $in=shift;
my $sample=shift;
my $bed=shift;
my $bed_U=shift;
#my $probe_name=shift;
my %hash=(); 
my $raw_base=0;

print "Sample\tTotal Reads(M)\tReads Q20\tReads Q30\tAlign Rate\tMean Depth(1000x)\tOn Target Rate\tSpecificity\tUniformity\tCoverage(>1x)\tCoverage(>100x)\tCoverage(>500x)\tCoverage(>1000x)\tCoverage(>5000x)\tCoverage(>10000x)\n";

my @file1=`ls $in/$sample/Step1QC/*.GC.stat`;
for(my $a=0;$a<@file1;$a++){
        chomp($file1[$a]);
        my $sam=(split/\/Step/,$file1[$a])[0];
        $sam=(split/\//,$sam)[-1];
        open(IN,"$file1[$a]") || die "Can't open file $file1[$a]!\n";
        my ($n,$raw_read1,$raw_base1,$raw1_q20,$raw1_q30) = 0;
        while(<IN>)
        {
             chomp;
             $_=~s/\s+//g;
             
          
                   if($_=~ /^\#ReadNum:(\d+)BaseNum:(\d+)ReadLeng:/)
                   {
                        $raw_read1=$1;
                        $raw_base1=$2;
                        $raw_base += $raw_base1;
                   }
                   if ($_=~ /^\#BaseQ:10--20:.*>Q20:(.*)%/)
                   {
                        $raw1_q20 = $1;
                   }
                   if ($_=~ /^\#BaseQ:20--30:.*>Q30:(.*)%/)
                   {
                        $raw1_q30 = $1;
                   }
     
           
        }
        close IN;
        if(defined $hash{$sam})
        {
                $hash{$sam}="$hash{$sam}\t$raw_read1\t$raw_base\t$raw1_q20\t$raw1_q30";
        }
        else{$hash{$sam}="$raw_read1\t$raw_base\t$raw1_q20\t$raw1_q30";}   
        
  
}







my @file3=`ls $in/$sample/Step2Alignment/*.alignment.txt`;
for(my $c=0;$c<@file3;$c++)

{
        chomp($file3[$c]);
        my $sam=(split/\/Step/,$file3[$c])[0];
        $sam=(split/\//,$sam)[-1];
        open(IN,"$file3[$c]") || die "Can't open file $file3[$c]!\n";
        my $map = 0;
        while(<IN>)
        {
                 chomp;
                 if($_=~ /mapped \((.*):.*\)/)
                 {
                       $map = $1;
                 }
        }
        if(defined $hash{$sam})
        {
                $hash{$sam}="$hash{$sam}\t$map";
        }
        else{$hash{$sam}="$map";}
        close IN;
}


my %total_dep;
my %len;
open IN, $bed or die $!;
my $length;
while(<IN>)
{
        chomp;
        my @d=split/\t/,$_;
        my $site = "$d[1]\t$d[2]";
           $total_dep{$d[0]}{$site} = 0;
           $length +=$d[2]-$d[1]+1;
           for (my $i=$d[1];$i<=$d[2];$i++)
           {
                  my $key = "$d[0]\t$i";
                  $len{$key}=0;
           }
}
close IN;


my @file4=`ls $in/$sample/Step2Alignment/*.deep`;
for(my $d=0;$d<@file4;$d++)
{
        chomp($file4[$d]);
        my $sam=(split/\/Step/,$file4[$d])[0];
        $sam=(split/\//,$sam)[-1];
        open(IN,"$file4[$d]") || die "Can't open file $file4[$d]!\n";
        my $total_length = keys %len;
        my ($depth,$aln_base,$target_base,$on_target,$hit_1,$hit_100,$hit_500,$hit_1000,$hit_5000,$hit_10000,$cov_1,$cov_100,$cov_500,$cov_1000,$cov_5000,$cov_10000)=0;
        while(<IN>)
        {
                chomp;
                $_=~s/\s+/\t/g;
                my @d=split/\t/,$_;
                    if($_=~/^chr/){$aln_base +=$d[-1];}
                    foreach my $i(keys %total_dep)
                    {
                         next if ($i ne $d[0]);
                         foreach my $j(keys %{$total_dep{$i}})
                         {
                               my ($st,$ed) = (split /\t/,$j)[0,1];
                               if($d[1]>=$st && $d[1]<=$ed)
                               {
                                        $target_base += $d[-1];
                                        last;
                               }
                         }
                    }
                    foreach my $chr(keys %total_dep)
                    {
                         next if ($chr ne $d[0]);
                         foreach my $pos(keys %{$total_dep{$chr}})
                         {
                               my ($st,$ed) = (split /\t/,$pos)[0,1];
                               if($d[1]>=$st && $d[1]<=$ed)
                               {
                                       $depth +=$d[-1];
                                       if($d[-1]>=1){$hit_1++;}
                                       if($d[-1]>=100){$hit_100++;}
                                       if($d[-1]>=500){$hit_500++;}
                                       if($d[-1]>=1000){$hit_1000++;}
                                       if($d[-1]>=5000){$hit_5000++;}
                                       if($d[-1]>=10000){$hit_10000++;}
                                       last;
                               }
                         }
                   }
        }
        close IN;
        $depth = $depth/$length;
        $on_target = $target_base/$aln_base;
        $cov_1 = $hit_1/$total_length;
        $cov_100 = $hit_100/$total_length;
        $cov_500 = $hit_500/$total_length;
        $cov_1000 = $hit_1000/$total_length;
        $cov_5000 = $hit_5000/$total_length;
        $cov_10000 = $hit_10000/$total_length;
        
   
        
        open(IN,"$file4[$d]") || die "Can't open file $file4[$d]!\n";
        my $uniformity=0;
        while(<IN>)
        {
                chomp;
                $_=~s/\s+/\t/g;
                my @d=split/\t/,$_;
                    foreach my $chr(keys %total_dep)
                    {
                         next if ($chr ne $d[0]);
                         foreach my $pos(keys %{$total_dep{$chr}})
                         {
                               my ($st,$ed) = (split /\t/,$pos)[0,1];
                               if($d[1]>=$st && $d[1]<=$ed)
                               {
                                     if($d[-1]>=(0.2*$depth)){$uniformity++;last;}
                               }
                         }
                   }
        }
        close IN;
        $uniformity = $uniformity/$total_length;
        if(defined $hash{$sam}){
                $hash{$sam}="$hash{$sam}\t$depth\t$on_target\t$target_base\t$uniformity\t$cov_1\t$cov_100\t$cov_500\t$cov_1000\t$cov_5000\t$cov_10000";
        } else {$hash{$sam}="$depth\t$on_target\t$target_base\t$uniformity\t$cov_1\t$cov_100\t$cov_500\t$cov_1000\t$cov_5000\t$cov_10000";
        }
}

############################################################################################################        
my %total_dep_U;
my %len_U;
open IN, $bed_U or die $!;
my $length_U;
while(<IN>)
{
        chomp;
        my @d_U=split/\t/,$_;
        my $site_U = "$d_U[1]\t$d_U[2]";
           $total_dep_U{$d_U[0]}{$site_U} = 0;
           $length_U +=$d_U[2]-$d_U[1]+1;
           for (my $i=$d_U[1];$i<=$d_U[2];$i++)
           {
                  my $key_U = "$d_U[0]\t$i";
                  $len_U{$key_U}=0;
           }
}
close IN;

my @file4_U=`ls $in/$sample/Step2Alignment/*.deep`;
for(my $d_U=0;$d_U<@file4_U;$d_U++)
{
        chomp($file4_U[$d_U]);
        my $sam=(split/\/Step/,$file4_U[$d_U])[0];
        $sam=(split/\//,$sam)[-1];
        open(IN,"$file4_U[$d_U]") || die "Can't open file $file4_U[$d_U]!\n";
       my $total_length_U = keys %len_U;
     # print $total_length_U."\n";
       my ($depth_U,$aln_base_U,$target_base_U)=0; 
              while(<IN>)
        {
                chomp;
                $_=~s/\s+/\t/g;
                my @d_U=split/\t/,$_;
                    if($_=~/^chr/){my $aln_base_U +=$d_U[-1];}
                    foreach my $i(keys %total_dep_U)
                    {
                         next if ($i ne $d_U[0]);
                         foreach my $j(keys %{$total_dep_U{$i}})
                         {
                               my ($st_U,$ed_U) = (split /\t/,$j)[0,1];
                               if($d_U[1]>=$st_U-30 && $d_U[1]<=$ed_U+30)
                               {
                                        $target_base_U += $d_U[-1];
                                        last;
                               }
                         }
                    }
                    foreach my $chr_U(keys %total_dep_U)
                    {
                         next if ($chr_U ne $d_U[0]);
                         foreach my $pos_U(keys %{$total_dep_U{$chr_U}})
                         {
                               my ($st_U,$ed_U) = (split /\t/,$pos_U)[0,1];
                               if($d_U[1]>=$st_U && $d_U[1]<=$ed_U)
                               {
                                       $depth_U +=$d_U[-1];
                                       last;
                               }
                         }
                   }
        }
        close IN;
          #print $depth."\n";
          $depth_U = $depth_U/$length_U;
        #print $depth."\n";
        open(IN,"$file4_U[$d_U]") || die "Can't open file $file4_U[$d_U]!\n";
        my $uniformity_U=0;
        while(<IN>)
        {
                chomp;
                $_=~s/\s+/\t/g;
                my @d_U=split/\t/,$_;
                    foreach my $chr_U(keys %total_dep_U)
                    {
                         next if ($chr_U ne $d_U[0]);
                         foreach my $pos_U(keys %{$total_dep_U{$chr_U}})
                         {
                               my ($st_U,$ed_U) = (split /\t/,$pos_U)[0,1];
                               if($d_U[1]>=$st_U && $d_U[1]<=$ed_U)
                               {
                                     if($d_U[-1]>=(0.2*$depth_U)){$uniformity_U++;last;}
                               }
                         }
                   }
        }
        close IN;
        $uniformity_U = $uniformity_U/$total_length_U;
        # print $uniformity."\n";  

#################################################################################################

        if(defined $hash{$sam}){
                $hash{$sam}="$hash{$sam}\t$uniformity_U";
        } else {$hash{$sam}="\t$uniformity_U";
        }
}

foreach my $key(keys %hash)
{        
         my @data = split/\t/,$hash{$key};
         
         
         my $raw_reads = ($data[0])/1000000;
            $raw_reads = flt($raw_reads);
         
         my $raw_q20 = $data[2];

         my $raw_q30 = $data[3];
   
         
         my $aln_rate = $data[4];
         my $mean_depth = $data[5]/1000;
            $mean_depth = flt($mean_depth);
         my $on_tar = $data[6];
            $on_tar = flt_to_pct($on_tar);
         my $specificity = $data[7]/$data[1];
            $specificity = flt_to_pct($specificity);
         my $unifor = $data[15];
            $unifor = flt_to_pct($unifor);
         my $cov1 = $data[9];
            $cov1 = flt_to_pct($cov1);
         my $cov100 = $data[10];
            $cov100 = flt_to_pct($cov100);
         my $cov500 = $data[11];
            $cov500 = flt_to_pct($cov500);
         my $cov1000 = $data[12];
            $cov1000 = flt_to_pct($cov1000);
         my $cov5000 = $data[13];
            $cov5000 = flt_to_pct($cov5000);
         my $cov10000 = $data[14];
            $cov10000 = flt_to_pct($cov10000);
         #my $uniformity_U = $data[15];
         #   $uniformity_U = flt_to_pct($uniformity_
         print "$key\t$raw_reads\t$raw_q20\t$raw_q30\t$aln_rate\t$mean_depth\t$on_tar\t$specificity\t$unifor\t$cov1\t$cov100\t$cov500\t$cov1000\t$cov5000\t$cov10000\n";
# print "$key\t$hash{$key}\n";
}
sub average {
      my (@num) = @_;
      my $num = scalar @num;
      my $total;
      foreach (0..$#num) 
      {
          $total += $num[$_];
      }
          return ($total/$num);
}
sub mid{
     my @list = sort{$a<=>$b} @_;
     my $count = @list;
     if( $count == 0 )
     {
         return undef;
     }
     if(($count%2)==1){
         return $list[int(($count-1)/2)];
     }
     elsif(($count%2)==0){
        return ($list[int(($count-1)/2)]+$list[int(($count)/2)])/2;
     }
}
sub Q1_qua{
     my @list = sort{$a<=>$b} @_;
     my $count = @list;
     if( $count == 0 )
     {
         return undef;
     }
     if(($count%2)==1){
         my $pos = ($count+1)*0.25;
         return $list[$pos-1];
     }
     elsif(($count%2)==0){
        my $pos = ($count+1)*0.25;
        my $up_pos = int($pos)-1;
        my $down_pos = int($pos);
        my $up = $list[$up_pos];
        my $down = $list[$down_pos];
        my $Q1 = $up + ($down-$up)*($pos-int($pos));
        return $Q1;
     }
}
sub Q3_qua{
     my @list = sort{$a<=>$b} @_;
     my $count = @list;
     if( $count == 0 )
     {
         return undef;
     }
     if(($count%2)==1){
         my $pos = ($count+1)*0.75;
         return $list[$pos-1];
     }
     elsif(($count%2)==0){
        my $pos = ($count+1)*0.75;
        my $up_pos = int($pos)-1;
        my $down_pos = int($pos);
        my $up = $list[$up_pos];
        my $down = $list[$down_pos];
        my $Q3 = $up + ($down-$up)*($pos-int($pos));
        return $Q3;
     }
}
sub flt {
    sprintf( "%.6f", shift );
}
sub flt_to_pct {
    sprintf( "%.4f", shift ) * 100 . '%';
}

