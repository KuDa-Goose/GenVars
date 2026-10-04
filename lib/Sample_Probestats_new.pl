#!/usr/bin/perl 

use warnings;
use strict;

my $InputFile1=shift;
my $OutputFile=shift;
my %hash = ();
my @Probe;
my @ProbeOntarget;
my @ProbeSelfLink;
my @ProbeUmiUniq;
my $Total = "total_reads";

open(IN,"$InputFile1") || die "Can't open file1 $InputFile1\n";
while(my $line = <IN>){
    chomp($line);
    my @line = split/\t/,$line;
    my $LineNum = scalar(@line)-2;
    my $ProbeNumber = int($LineNum/4);
    if($line =~ /^Probe/){
        for(my $i=1;$i<$LineNum+1;$i++){
            if($line[$i]=~/probe(\d+)$/){
                push @Probe, $line[$i];
            }elsif($line[$i]=~/_ontarget$/){
                push @ProbeOntarget, $line[$i];
            }elsif($line[$i]=~/_SelfLink$/){
                push @ProbeSelfLink, $line[$i];
            }elsif($line[$i]=~/_UmiUniq$/){
                push @ProbeUmiUniq, $line[$i];
            }
        }
    }else{
        for(my $i=0;$i<@Probe;$i++){
            $hash{$line[0]}{$Probe[$i]} = $line[$i+1];
        }
        for(my $i=0;$i<@ProbeOntarget;$i++){
            $hash{$line[0]}{$ProbeOntarget[$i]} = $line[$i+1+$ProbeNumber];
        }
        for(my $i=0;$i<@ProbeSelfLink;$i++){
            $hash{$line[0]}{$ProbeSelfLink[$i]} = $line[$i+1+$ProbeNumber+$ProbeNumber];
        }
        for(my $i=0;$i<@ProbeUmiUniq;$i++){
            $hash{$line[0]}{$ProbeUmiUniq[$i]} = $line[$i+1+$ProbeNumber+$ProbeNumber+$ProbeNumber];
        }
        $hash{$line[0]}{$Total} = $line[-1];
    }
}

my $Header = "Sample\tTotal_reads";
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i];
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_ontarget";
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_SelfLink";
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_UmiUniq";
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_ProbeRatio";
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_ontargetRatio";
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_ontargetOfProbe";
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_SelfLinkOfProbe";
}
for(my $i=0;$i<@Probe;$i++){
    $Header.="\t".$Probe[$i]."_UmiUniqOfOntarget";
}

open(OUT, ">$OutputFile");
print OUT $Header."\n";
my @Sample = keys %hash;
foreach my $SampleName(@Sample){
    my $ProbeStats = $SampleName."\t".$hash{$SampleName}{$Total};
    for(my $j=0;$j<@Probe;$j++){
        $ProbeStats.="\t".$hash{$SampleName}{$Probe[$j]};
    }
    for(my $j=0;$j<@ProbeOntarget;$j++){
        $ProbeStats.="\t".$hash{$SampleName}{$ProbeOntarget[$j]};
    }
    for(my $j=0;$j<@ProbeSelfLink;$j++){
        $ProbeStats.="\t".$hash{$SampleName}{$ProbeSelfLink[$j]};
    }
    for(my $j=0;$j<@ProbeUmiUniq;$j++){
        $ProbeStats.="\t".$hash{$SampleName}{$ProbeUmiUniq[$j]};
    }
    for(my $j=0;$j<@Probe;$j++){
        my $ProbeRatio = (int($hash{$SampleName}{$Probe[$j]})/int($hash{$SampleName}{$Total}))*100;
        $ProbeRatio = sprintf("%.2f", $ProbeRatio);
        $ProbeStats.="\t".$ProbeRatio."%";
    }
    for(my $j=0;$j<@ProbeOntarget;$j++){
        my $OntarRatio = (int($hash{$SampleName}{$ProbeOntarget[$j]})/int($hash{$SampleName}{$Total}))*100;
        $OntarRatio = sprintf("%.2f", $OntarRatio);
        $ProbeStats.="\t".$OntarRatio."%";
    }
    for(my $j=0;$j<@Probe;$j++){
        my $OntargetOfProbe = 0;
        if(int($hash{$SampleName}{$Probe[$j]}) == 0){
            $OntargetOfProbe = 0;
        }else{
            $OntargetOfProbe = (int($hash{$SampleName}{$ProbeOntarget[$j]})/int($hash{$SampleName}{$Probe[$j]}))*100;
            $OntargetOfProbe = sprintf("%.2f", $OntargetOfProbe);
        }
        $ProbeStats.="\t".$OntargetOfProbe."%";
    }
    for(my $j=0;$j<@ProbeSelfLink;$j++){
        my $SelfLinkOfProbe = 0;
        if(int($hash{$SampleName}{$Probe[$j]}) == 0){
            $SelfLinkOfProbe = 0;
        }else{
            $SelfLinkOfProbe = (int($hash{$SampleName}{$ProbeSelfLink[$j]})/int($hash{$SampleName}{$Probe[$j]}))*100;
            $SelfLinkOfProbe = sprintf("%.2f", $SelfLinkOfProbe);
        }
        $ProbeStats.="\t".$SelfLinkOfProbe."%";
    }
    for(my $j=0;$j<@ProbeUmiUniq;$j++){
	my $UmiUniqOfOntarget;
        if(int($hash{$SampleName}{$ProbeOntarget[$j]}) == 0){
            $UmiUniqOfOntarget = 0;
        }else{
            $UmiUniqOfOntarget = (int($hash{$SampleName}{$ProbeUmiUniq[$j]})/int($hash{$SampleName}{$ProbeOntarget[$j]}))*100;
        }
        $UmiUniqOfOntarget = sprintf("%.2f", $UmiUniqOfOntarget);
        $ProbeStats.="\t".$UmiUniqOfOntarget."%";
    }
    print OUT $ProbeStats."\n";
}

close IN;
close OUT;

