#!/usr/bin/perl -w
use strict;
#use autodie;
use Getopt::Long;

my $Usage =<<Usage_end;
Usage:
    perl $0 -i probe-informatin-file -l list -d Script_dir -t DATA -p probe_bed -s Sample_name.bed
    
        -i <file name>  input probe informatin file name
        -l <file name>  input Sample name list
        -d <directory name> output directory 
        -t <character>  input DATA 
        -p <file name>  output probe bed file name
        -s <file name>  output Sample Name bed
        -h/help <boolean> Print help of current program 

Usage_end

#Dfault parameters #
my $in;
my $list;
my $dir;
my $Data;
my $probe;
my $output;
my $help;

#Get parameters
GetOptions(
    'i|input=s'  =>\$in,
    'l|iist=s'  =>\$list,
    'd|dir=s'  =>\$dir,
    't|time=s'  =>\$Data,
    'p|probe-bed=s'  =>\$probe,
    's|samplename=s'  =>\$output,
    'h|help'  =>\$help);

die "$Usage" unless ($in && $list && $dir && $Data && $probe && $output);

if ($help){
    print $Usage;
    exit;
}


my @head;
open(PRO,">$dir/../bed/$probe") or die "Can' t open file $dir/../bed/$probe! $!";
open(IN,"$in")||die "Can't open the input probe informatin file $in!\n";
while(my $line=<IN>){
    chomp($line);
    if($line=~/^Chr/){
        next;
    }else{
        my @line=split/\t/,$line;
        my $head="    \$line=~s/$line[4]_/$line[3]_/g;\n";
        push @head,$head;

        print PRO "$line[0]\t$line[1]\t$line[2]\t$line[3]\t$line[4]\t$line[5]\t$line[6]\t$line[7]\n";
    }
}
close IN;

open(OUT,">$output");
open(IN2,"$list") || die "Can't open file $list\n";
while(my $Line=<IN2>){
    chomp($Line);
    my @Line=split/\t/,$Line;
    $Line[0] =~ /^IonXpress_C(\d+)[\._]R_\S+\.fastq.gz$/;
    my $Barcode="SC".$1;
    print OUT $Barcode."\n";
}
close IN2;
close OUT;



open(HEAD,">$dir/change_probe_head.pl");
print HEAD "#!/usr/bin/perl\n\n\$in=shift;\n\nopen(IN,\"\$in\");\nopen(OUT,\">Probe_Stats_$Data.txt\");while(\$line=<IN>){\n";
open(HEADA,">$dir/change_probeumi_head.pl");
print HEADA "#!/usr/bin/perl\n\n\$in=shift;\n\nopen(IN,\"\$in\");\nopen(OUT,\">Probe_Stats_$Data\_UMI.txt\");while(\$line=<IN>){\n";

#my $len=@head;
my @len=reverse(@head);
#my $len=$#head;
for (my $i=0;$i<@len;$i++){
    print HEAD $len[$i];
    print HEADA $len[$i];
}

#for (my $i=$len;$i>0;$i--){
#    print HEAD $head[$i];
#}

print HEAD "    print OUT \$line;\n}\nclose IN;\nclose OUT;\n";
print HEADA "    print OUT \$line;\n}\nclose IN;\nclose OUT;\n";
close HEAD;
close HEADA;
close PRO;
