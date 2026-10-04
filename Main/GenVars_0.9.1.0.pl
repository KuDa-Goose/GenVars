#!/usr/bin/perl

use warnings;
use strict;
use Getopt::Long;
use File::Basename;
use Cwd qw(abs_path getcwd);
use POSIX ":sys_wait_h";
use FindBin qw($Bin);
use lib "$Bin/../lib";
use ToolsCfg;

=begin Explanation parameters for softwares and genome files

software:
    fastqc  => "/thinker/net/logs/Softwares/FastQC/fastqc",
    iTools  => "/local/usr/bin/iTools_Code/iTools",
    bwa     => "/usr/bin/bwa-0.7.13/bwa",
    sortSam => "/thinker/net/logs/Softwares/picard/build/libs/picard.jar",
    buildIndex => "/thinker/net/logs/Softwares/picard/build/libs/picard.jar",
    varscan    => "/usr/bin/VarScan.v2.3.8.jar",
    cutadapt   => "/usr/bin/cutadapt",
    samToFastq => "/thinker/net/logs/Softwares/picard/build/libs/picard.jar"

genome files:
    refFa = "/thinker/dstore/r3data/AnalysisET/Reference/Ubuntu-Congr/hg19_UCSC/genomics/genome.fa";
    bwaIndex="/thinker/dstore/r3data/AnalysisET/Reference/Ubuntu-Congr/hg19_UCSC/BWAindex/genome.fa";
    annoDB = "/thinker/dstore/r3data/humandb/";

Sample label:
    sample="S001";
    group="NGS";
    platform="Ion_Torrent";

=end
=cut

# Initialize softwares and genome files
my %soft   = %ToolsCfg::BioTools;
my %dbFile = %ToolsCfg::geno_lib;
my %label  = %ToolsCfg::MetaInfo;

=doc begin  Interpretation of the script

WorkFlow
    1. FastQC
       Reads_Stat
       Mapping
       Sort_Alignment
       Variant_Calling
       Stat
    2. Cutadapt_probe
       Mapping
       Sort_Alignment
       Extract_Reads
       Comparison_Stat

Sub
    read_List
    VarScan_Shell
    Probe_Shell

=doc end
=cut

##### create Results Directory  #####


my $usage = <<USAGE_end;
Usage:
    perl $0 -i fq_list -d fastq_dir -b ontarget-bed [-o output_dir] [-n process_number] [-f fusion_probe] [-t time] [-e SampleInfo]
    
        -i <file> the file name of list, which store fq_file names 
        -d <directory>  the directory of Fastq files
        -o <directory>  the directory of output Directory
        -b <bedfile>  the absolute path of bed file for Ontarget Calculation
        -q <Integer Number>  Average quality for VarScan    
        -n <Integer Number>  Maximal Parallel running process for sample
        -a <directory> summary of all sample analysis results
        -c <boolean>   whether to do cut adaptor for VarScan and Probe analysis, default Not
        -t <character> Date for generating machine learning data
        -f <character> Fusion of Probe txt
        -e <character> Sample Info txt
        -h/help <boolean>    Print help of current program
        
USAGE_end


##### Get current time for name of result directory #####

my ($sec,$min,$hour,$day,$mon,$year,$wday,$yday,$isdst) = localtime();
my $year_t = $year + 1900;
my $month = $mon + 1;
my $Month = (sprintf "%02d", $month);
print $year_t."-".$Month."-".$day." ".$hour.":".$min.":".$sec."\n";

my %DATA = (
   '01'        =>         'Jan',
   '02'        =>         'Feb',
   '03'        =>         'Mar',
   '04'        =>         'Apr',
   '05'        =>         'May',
   '06'        =>         'Jun',
   '07'        =>         'Jul',
   '08'        =>         'Aug',
   '09'        =>         'Sep',
   '10'        =>         'Oct',
   '11'        =>         'Nov',
   '12'        =>         'Dec',
   );

my $fqList ;
my $ODIR = "Results_".$year_t."_".$month."_".$day ;
my $DATA = $year_t."_".$DATA{$Month}."_".$day;
my $FQ_DIR ;
my $S_Dir = "$Bin/../lib";
my $Bed_Dir = "$Bin/../bed";
my $bed_file;                                      ## add bed option
my $qualAvg = 15; 
my $P_num = 3; 
my $fusionP;
my $SampleInfo = 0;
my %Primer=();

my $cutad      = 0 ;                                  ## cutadapt option
my $all_summ       ;                                  ## all sample analysis table results
my $help           ;

# Get parameters

GetOptions(
    'i|input=s'     => \$fqList,
    'd|fq=s'        => \$FQ_DIR,
    'o|output=s'    => \$ODIR,
    'b|ontar_bed=s' => \$bed_file,                        ## Add bed option for Uniformity
    'q|avg_qual=i'  => \$qualAvg,
    'n|num_p=i'     => \$P_num,
    'c|cut!'        => \$cutad,
    't|time=s'      => \$DATA,
    'a|allreport=s' => \$all_summ,
    'f|fusionP=s'     => \$fusionP,
    'e|SampleInfo=s'  => \$SampleInfo,
    'h|help'        => \$help );
    
die "$usage" unless ($fqList && $FQ_DIR && $bed_file && $all_summ);

if ($help) {
    print $usage;
    exit;
}

my @data=split/\_/,$DATA;
my $Data_Time = $data[0]."_".$DATA{$data[1]}."_".$data[2];
$bed_file =~ /ontarget([\d\D]*)\.bed/;
my $U_bed="probe".$1.".bed";
system("perl $S_Dir/get_probe_information.pl -i $Bed_Dir/Probe-information.txt -l $fqList -d $S_Dir -t $Data_Time -p $U_bed -s $Bed_Dir/Sample_name.bed");
system("$soft{twoBitToFa} $dbFile{hg38_2bit} -bed=$bed_file $Bed_Dir/ontarget.fa");
system("python $S_Dir/Get_Base.py $bed_file $Bed_Dir/ontarget.fa $Bed_Dir/ontargetBase.txt");
##### create Results Directory  ##### 


if (-d $ODIR){
    print "Output Directory has been created, Please use other name.\n";
    exit;
} else {
    mkdir $ODIR;
}

mkdir("$ODIR/Fastq", 0755) or die "Can\'t create directory Fastq, $!";
system("ln -s $FQ_DIR/*.fastq.gz $ODIR/Fastq");

mkdir("$ODIR/Work_shell", 0755) or die "Can\'t create directory Work_shell, $!";
mkdir("$ODIR/Varscan_analysis", 0755) or die "Can\'t create directory Varscan_Analysis, $!";
mkdir("$ODIR/Probe_analysis", 0755) or die "Can\'t create directory Probe_Analysis, $!";
mkdir("$ODIR/Fusion_analysis", 0755) or die "Can\'t create directory Fusion_Analysis, $!";
mkdir("$ODIR/MSI_analysis", 0755) or die "Can\'t create directory Fusion_Analysis, $!";
mkdir("$ODIR/Result_Dir", 0755) or die "Can\'t create directory Fusion_Analysis, $!";

##### Generate file and set work directory #####

system("cp $fqList $ODIR/Work_shell");
chdir("$ODIR/Work_shell");

my $WORK_DIR = abs_path(getcwd);

my $Out_Dir = abs_path("../");

my $V_Dir = abs_path("$Out_Dir/Varscan_analysis");
my $P_Dir = abs_path("$Out_Dir/Probe_analysis");
my $T_Dir = abs_path("$Out_Dir/Fusion_analysis");
my $M_Dir = abs_path("$Out_Dir/MSI_analysis");
my $R_Dir = abs_path("$Out_Dir/Result_Dir");
my $FQ = abs_path("$Out_Dir/Fastq");


my %Probes = &get_probe("$Bed_Dir/Probe-information.txt");


my %Sample_Probes = &get_sample($fqList);
my @Sample_Files = keys(%Sample_Probes);

##### Main data processing  #####

&Probe_Shell(@Sample_Files);


#&Fusion_shell(@Sample_Files);

    
if (! -e "SABEL_Sample_ProbeAnalysis.log"){
    print "Analysis for Start!\n";
    system("perl $S_Dir/Parallel_Run.pl $P_num PRO_ShellList.txt");
    system("touch SABEL_Sample_ProbeAnalysis.log");
}


print "All sample analysis Done\n";

#### get probe information subroutine ####

my %Str = ();
sub get_probe{
    my $file=shift;
    my %hash=();

    open(IN,"$file")||die "Can't open the file $file !\n";
    my $line=<IN>;
    while(my $line=<IN>){
        chomp($line);
        my @line=split/\t/,$line;
        my $key=$line[4];
        my $value=$line[8]."\t".$line[0].":".$line[9];
        $Primer{$key}=$line[10];
        $hash{$key}=$value;
        $Str{$key}=$line[5];
    }
    close IN;
    return (%hash);
}


#### BWA- VarScan analysis subroutine ####

sub Probe_Shell{
    open PSH, ">PRO_ShellList.txt" or die "$!";

    foreach my $SP (@_){
    # for each fq file

        $SP =~ /^IonXpress_C(\d+)[\._]R_\S+\.R1.fastq.gz$/;
        my $Sample = "SampleC".$1;
        
        my $R3=$1;
        #$_=undef;
        $SP =~ /(IonXpress_.*[\._]R_\S+)\.R1.fastq.gz$/;
        my $R1=$1;

        print PSH "$Sample-PR.sh\n";
        # file handle for pipeline per sample
        open OUTSH, ">$Sample-PR.sh" or die "$!";


        print OUTSH "mkdir $P_Dir/$Sample\n";
        
        foreach my $E_Probe ( @{ $Sample_Probes{$SP} } ){
            print OUTSH "mkdir $P_Dir/$Sample/bwa_$E_Probe\n";
        }
        my $probe_name_txt = join( "\t", @{ $Sample_Probes{$SP} } );
        print OUTSH "echo $probe_name_txt >$P_Dir/$Sample/$Sample.probe_name.txt \n";
        print OUTSH "echo start pipeline at `date`\n";
  
        my $Input1;
        my $Input2;
        print OUTSH "$soft{fastqc} -o $P_Dir/$Sample $FQ/$R1.R1.fastq.gz\n";
        print OUTSH "$soft{fastqc} -o $P_Dir/$Sample $FQ/$R1.R2.fastq.gz\n";
        ##########################1
        foreach my $E_Probe ( @{ $Sample_Probes{$SP} } ){
            print OUTSH "cd $P_Dir/$Sample\n";
            my $PRE_FN = $R1.$E_Probe;
            
            my $R4="UN_$E_Probe.S".$R3;
            my $R5="biotin_$E_Probe.S".$R3;

            my @probe_info = split(/\t/, $Probes{$E_Probe});
            my $probe_seq = $probe_info[0];
            my $probe_length = length($probe_seq);
            my $probe_region = $probe_info[1];

            if ($cutad) {
                print OUTSH "$soft{cutadapt} -a CTGTCTCTTATACACATCTCCGAGCCCACGAGAC $FQ/$R1.R1.fastq.gz -o cut_$R1.R1.fastq\n";
                print OUTSH "$soft{cutadapt}  -g ^$probe_seq --untrimmed-output $R4.R1.fastq cut_$R1.R1.fastq> $R5.R1.fastq\n";
                print OUTSH "perl $S_Dir/delete11.pl $P_Dir/$Sample/$R4.R1.fastq cut_$R1.R1.fastq $PRE_FN.R1.fastq\n";
            } else {           
                print OUTSH "$soft{cutadapt}  -g ^$probe_seq --untrimmed-output $R4.R1.fastq $FQ/$R1.R1.fastq.gz> $R5.R1.fastq\n";
                print OUTSH "perl $S_Dir/delete11.pl $P_Dir/$Sample/$R4.R1.fastq $FQ/$R1.R1.fastq.gz $PRE_FN.R1.fastq\n";
            }
            if ($cutad) {
                print OUTSH "$soft{cutadapt} -a CTGTCTCTTATACACATCTGACGCTGCCGACGA $FQ/$R1.R2.fastq.gz -o cut_$R1.R2.fastq\n";
                print OUTSH "perl $S_Dir/Get_FastqID.pl $PRE_FN.R1.fastq cut_$R1.R2.fastq $PRE_FN.R2.fastq\n";
            } else {
                print OUTSH "$soft{cutadapt}  -a $probe_seq --untrimmed-output $R4.R2.fastq $FQ/$R1.R2.fastq.gz> $R5.R2.fastq\n";
                print OUTSH "perl $S_Dir/delete11.pl $P_Dir/$Sample/$R4.R2.fastq $FQ/$R1.R2.fastq.gz $PRE_FN.R2.fastq\n";
            }

            print OUTSH "cd $P_Dir/$Sample/bwa_$E_Probe\n";
            print OUTSH "cp $P_Dir/$Sample/$PRE_FN.R1.fastq $P_Dir/$Sample/bwa_$E_Probe\n";
            print OUTSH "cp $P_Dir/$Sample/$PRE_FN.R2.fastq $P_Dir/$Sample/bwa_$E_Probe\n";
            print OUTSH "$soft{iTools} Fqtools stat -minBaseQ ! -InFq  $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.R1.fastq -InFq  $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.R2.fastq -OutStat $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.GC.stat\n";
            print OUTSH "perl $S_Dir/Get_UMI.pl $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.R2.fastq $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.R1.fastq $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.umi.R2.fastq $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.umi.R1.fastq\n";
            print OUTSH "$soft{bwa} mem -M -R \"\@RG\\tID:$label{group}\\tSM:$label{sample}\\tPL:$label{platform}\" -t 12 $dbFile{bwaIndex} $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.umi.R1.fastq $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.umi.R2.fastq>$P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sam\n";
            print OUTSH "java -jar $soft{sortSam} SortSam INPUT=$P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sam  OUTPUT=$P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sorted.sam SORT_ORDER=coordinate\n";
            print OUTSH "samtools view -bS $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sorted.sam > $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sorted.bam\n";
            print OUTSH "java -jar $soft{buildIndex} BuildBamIndex I=$P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sorted.bam\n";

            my $RS3="S".$R3."$E_Probe";
            print OUTSH "samtools depth -d 2147483647 $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sorted.bam >$RS3.deep\n";
            print OUTSH "#! \/bin\/sh\n";
            print OUTSH "if test -s $RS3.deep; then \n";
            print OUTSH "continue\n";
            print OUTSH "else\n";
            print OUTSH "echo \"chr\t1\t0\">>$RS3.deep\n";
            print OUTSH "fi\n";

            print OUTSH "samtools flagstat $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sorted.bam > $PRE_FN.alignment.txt\n";
            #############################################################################################
            print OUTSH "samtools view -b $P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.sorted.bam $probe_region > $PRE_FN.hg19.ontarget.sorted.bam\n";
            print OUTSH "java -jar $soft{samToFastq} SamToFastq I=$P_Dir/$Sample/bwa_$E_Probe/$PRE_FN.hg19.ontarget.sorted.bam F=$PRE_FN.R1.hg38.ontarget.sorted.fastq F2=$PRE_FN.R2.hg38.ontarget.sorted.fastq\n";

            ########remove SelfLink
            print OUTSH "perl $S_Dir/Remove_SelfLink.pl $PRE_FN.R1.hg38.ontarget.sorted.fastq $PRE_FN.R2.hg38.ontarget.sorted.fastq $probe_length $PRE_FN.ontarget.sorted.R1.fastq $PRE_FN.SelfLink.R1.fastq $PRE_FN.ontarget.sorted.R2.fastq $PRE_FN.SelfLink.R2.fastq\n";

            my $TrueSeq = $Primer{$E_Probe};
            my $NewLen = length($probe_seq) + 4;
            print OUTSH "perl $S_Dir/Filter_MismatchReads.pl $PRE_FN.ontarget.sorted.R1.fastq $NewLen $TrueSeq $PRE_FN.ontarget.sorted.R2.fastq $PRE_FN.OntargetA.sorted.R1.fastq $PRE_FN.OntargetA.sorted.R2.fastq\n";
            print OUTSH "perl $S_Dir/Remove_15bp.pl $PRE_FN.OntargetA.sorted.R2.fastq $PRE_FN.OntargetA.sorted.R1.fastq $PRE_FN.Ontarget.sorted.R2.fastq $PRE_FN.Ontarget.sorted.R1.fastq\n";

            print OUTSH "java -Xmx8G -jar $soft{picard} FastqToSam FASTQ=$PRE_FN.Ontarget.sorted.R1.fastq FASTQ2=$PRE_FN.Ontarget.sorted.R2.fastq OUTPUT=$PRE_FN.uBAM READ_GROUP_NAME=test SAMPLE_NAME=$Sample LIBRARY_NAME=test PLATFORM_UNIT=NavoSeq PLATFORM=illumina RUN_DATE=`date --iso-8601=seconds`\n";
            print OUTSH "java -jar $soft{fgbio} ExtractUmisFromBam --input=$PRE_FN.uBAM --output=$PRE_FN.umi.uBAM --read-structure=1M+T 15M+T --single-tag=RX --molecular-index-tags=ZA ZB\n";
            print OUTSH "samtools fastq  $PRE_FN.umi.uBAM | $soft{bwa} mem -t 8 -p $dbFile{bwaIndex} /dev/stdin | samtools view -b > $PRE_FN.umi.BAM\n";
            print OUTSH "java -Xmx8G -jar $soft{picard} MergeBamAlignment R=$dbFile{bwaIndex} UNMAPPED_BAM=$PRE_FN.umi.uBAM ALIGNED_BAM=$PRE_FN.umi.BAM O=$PRE_FN.umi.merged.BAM CREATE_INDEX=true MAX_GAPS=-1 ALIGNER_PROPER_PAIR_FLAGS=true VALIDATION_STRINGENCY=SILENT SO=coordinate ATTRIBUTES_TO_RETAIN=XS\n";
            print OUTSH "java -jar $soft{fgbio} GroupReadsByUmi --input=$PRE_FN.umi.merged.BAM --output=$PRE_FN.umi.group.BAM --strategy=Identity --min-map-q=20 --edits=0 --raw-tag=RX\n";
            print OUTSH "samtools view $PRE_FN.umi.group.BAM > $PRE_FN.umi.group.sam\n";
            print OUTSH "java -jar $soft{fgbio} CallMolecularConsensusReads --min-reads=1 --min-input-base-quality=10 --input=$PRE_FN.umi.group.BAM --output=$PRE_FN.consensus.uBAM\n";
            print OUTSH "samtools fastq $PRE_FN.consensus.uBAM | $soft{bwa} mem -t 8 -p $dbFile{bwaIndex}  /dev/stdin | samtools view -b > $PRE_FN.consensus.BAM\n";
            print OUTSH "java -Xmx8G -jar $soft{picard} MergeBamAlignment R=$dbFile{bwaIndex} UNMAPPED_BAM=$PRE_FN.consensus.uBAM ALIGNED_BAM=$PRE_FN.consensus.BAM O=$PRE_FN.consensus.merge.BAM CREATE_INDEX=true MAX_GAPS=-1 ALIGNER_PROPER_PAIR_FLAGS=true VALIDATION_STRINGENCY=SILENT SO=coordinate ATTRIBUTES_TO_RETAIN=XS\n";
            print OUTSH "java -jar $soft{fgbio} FilterConsensusReads --input=$PRE_FN.consensus.merge.BAM --output=$PRE_FN.consensus.merge.filter.BAM --ref=$dbFile{bwaIndex} --min-reads=1 --max-read-error-rate=0.05 --max-base-error-rate=0.1 --min-base-quality=10 --max-no-call-fraction=0.20\n";
            ########Merge Filter Bam
            print OUTSH "samtools view -h $PRE_FN.consensus.merge.filter.BAM > $PRE_FN.consensus.merge.filter.sam\n";
            print OUTSH "perl $S_Dir/Change_samID.pl $PRE_FN.consensus.merge.filter.sam $E_Probe $PRE_FN.umi.group.sam $PRE_FN.consensus.merge.filterName.sam\n";
            print OUTSH "samtools view -bS $PRE_FN.consensus.merge.filterName.sam >$PRE_FN.consensus.merge.filterName.bam\n";
            print OUTSH "java -jar $soft{buildIndex} BuildBamIndex I=$PRE_FN.consensus.merge.filterName.bam\n";

            ########Merge Clip Bam
            print OUTSH "java -jar $soft{fgbio} ClipBam --input=$PRE_FN.consensus.merge.filter.BAM --output=$PRE_FN.consensus.merge.filter.clip.BAM --ref=$dbFile{bwaIndex} --clip-overlapping-reads=true\n";
            print OUTSH "samtools view -h $PRE_FN.consensus.merge.filter.clip.BAM > $PRE_FN.consensus.merge.filter.clip.sam\n";
            print OUTSH "perl $S_Dir/Filter_5Solf.pl $PRE_FN.consensus.merge.filter.clip.sam $PRE_FN.consensus.merge.filter5.clip.sam\n";
            print OUTSH "perl $S_Dir/Change_samID.pl $PRE_FN.consensus.merge.filter5.clip.sam $E_Probe $PRE_FN.umi.group.sam $PRE_FN.consensus.merge.clip.Filter.sam\n";
            print OUTSH "samtools view -bS $PRE_FN.consensus.merge.clip.Filter.sam > $PRE_FN.consensus.merge.clip.Filter.bam\n";
            print OUTSH "java -jar $soft{buildIndex} BuildBamIndex I=$PRE_FN.consensus.merge.clip.Filter.bam\n";
            ################################
            print OUTSH "samtools view -b $PRE_FN.consensus.merge.clip.Filter.bam $probe_region > $PRE_FN.consensus.merge.filter.target.bam\n";
            print OUTSH "samtools view -h -f 128 $PRE_FN.consensus.merge.filter.target.bam > $PRE_FN.consensus.merge.filter.R2.sam\n";
            print OUTSH "python $S_Dir/LastBase_Mismatch.py $Bed_Dir/ontargetBase.txt $PRE_FN.consensus.merge.filter.R2.sam $Str{$E_Probe} $PRE_FN.consensus.merge.clip.Filter.sam $PRE_FN\_Ontarget.sam $PRE_FN\_Errot.txt\n";
            print OUTSH "samtools view -bS -h $PRE_FN\_Ontarget.sam > $PRE_FN\_Ontarget.bam\n";
            print OUTSH "samtools index $PRE_FN\_Ontarget.bam\n";

            print OUTSH "java -jar $soft{samToFastq} SamToFastq I=$PRE_FN.consensus.merge.clip.Filter.bam F=$PRE_FN.clip.umi.R1.fastq F2=$PRE_FN.clip.umi.R2.fastq\n";
        }
        print OUTSH "mkdir $P_Dir/$Sample/FilterBam\n";
        print OUTSH "cd $P_Dir/$Sample/FilterBam\n";
        print OUTSH "ln -s $P_Dir/$Sample/bwa_*/*consensus.merge.filterName.bam .\n";
        print OUTSH "samtools merge $P_Dir/$Sample/$R1\.OntargetFilter.bam *consensus.merge.filterName.bam\n";
        
        print OUTSH "mkdir $P_Dir/$Sample/ClipBam\n";
        print OUTSH "cd $P_Dir/$Sample/ClipBam\n";
        print OUTSH "ln -s $P_Dir/$Sample/bwa_*/*consensus.merge.clip.Filter.bam .\n";
        print OUTSH "samtools merge $P_Dir/$Sample/$R1\.OntargetClip.bam *consensus.merge.clip.Filter.bam\n";
        print OUTSH "java -jar $soft{buildIndex} BuildBamIndex I=$P_Dir/$Sample/$R1\.OntargetFilter.bam\n";
        print OUTSH "perl $soft{factera} $P_Dir/$Sample/$R1\.OntargetFilter.bam $dbFile{FusionExonsBed} $dbFile{Fusion2bit}\n";
        print OUTSH "java -jar $soft{buildIndex} BuildBamIndex I=$P_Dir/$Sample/$R1\.OntargetClip.bam\n";
        print OUTSH "java -jar $soft{samToFastq} SamToFastq I=$P_Dir/$Sample/$R1\.OntargetClip.bam F=$P_Dir/$Sample/$R1\.Ontarget.R1.fastq F2=$P_Dir/$Sample/$R1\.Ontarget.R2.fastq\n";
        print OUTSH "cd $P_Dir\n";
        
        print OUTSH "echo Probe end pipeline at `date` \n";

        #########################################################################Varscan Call SNV_INDEL
        print OUTSH "mkdir $V_Dir/$Sample\n";
        print OUTSH "mkdir $V_Dir/$Sample/Step2Alignment\n";
        print OUTSH "mkdir $V_Dir/$Sample/Step3Variant\n";

        print OUTSH "echo Varscan start pipeline at `date` \n";
        print OUTSH "cd $V_Dir/$Sample\n";
        print OUTSH "cd $V_Dir/$Sample/Step2Alignment\n";
        my $R2=$R1."sorted";
        print OUTSH "samtools depth -d 2147483647 $P_Dir/$Sample/$R1\.OntargetClip.bam >$V_Dir/$Sample/Step2Alignment/${R2}.deep\n";
        print OUTSH "echo #####variant calling###at`date` \n";
        print OUTSH "cd $V_Dir/$Sample/Step3Variant\n";

        print OUTSH "cat $P_Dir/$Sample/bwa_*/*Errot.txt > $Sample\_Mutation_Error.xls\n";
        print OUTSH "samtools mpileup -A -d 1000000 -B -Q 0 -f $dbFile{refFa}  $P_Dir/$Sample/$R1\.OntargetClip.bam > ${R2}.mpileup\n";
        print OUTSH "java -jar $soft{varscan} mpileup2snp ${R2}.mpileup  --min-coverage 0 --min-reads2 2 --min-avg-qual $qualAvg -min-var-freq 0 --min-freq-for-hom 0.00001 --p-value 1 --strand-filter 2 --output-vcf 1 > ${R2}.snp.vcf\n";
        print OUTSH "java -jar $soft{varscan} mpileup2indel ${R2}.mpileup --min-coverage 0 --min-reads2 1 --min-avg-qual $qualAvg -min-var-freq 0 --min-freq-for-hom 0.00001 --p-value 1 --strand-filter 2 --output-vcf 1 > ${R2}.indel.vcf\n";
        print OUTSH "java -jar $soft{varscan} pileup2snp ${R2}.mpileup --min-coverage 0 --min-reads2 2 --min-avg-qual $qualAvg -min-var-freq 0 --min-freq-for-hom 0.00001 --p-value 1 --strand-filter 2 --output-vcf 1 > ${R2}_pileup.snp.vcf\n";
        print OUTSH "java -jar $soft{varscan} pileup2indel ${R2}.mpileup --min-coverage 0 --min-reads2 1 --min-avg-qual $qualAvg -min-var-freq 0 --min-freq-for-hom 0.00001 --p-value 1 --strand-filter 2 --output-vcf 1 > ${R2}_pileup.indel.vcf\n";
        print OUTSH "awk \'\!a[\$1\"\\t\"\$2\"\\t\"\$3\"\\t\"\$19]++' $V_Dir/$Sample/Step3Variant/*pileup.snp.vcf > $V_Dir/$Sample/Step3Variant/$Sample-N.vcf\n";
        print OUTSH "perl $S_Dir/snp_indel.pl -v $V_Dir/$Sample -s $Bed_Dir/SNV.txt -i $Bed_Dir/Indel.txt -c $Bed_Dir/Complex_Input.txt -m Middle_snp.xls -e $P_Dir -o snp_indel_frequency.xls\n";
        print OUTSH "python $S_Dir/Transposition_SNV.py snp_indel_frequency.xls Snp_Indel_Frequency.xls\n";
        ##############################
        print OUTSH "cd $V_Dir/$Sample/Step3Variant\n";
        print OUTSH "python $S_Dir/Analysis_SampleInfo.py $SampleInfo $Sample\n";
        print OUTSH "python $S_Dir/Analysis_Report_SNP.py $Bed_Dir/Mutation_Database.txt snp_indel_frequency.xls $V_Dir/$Sample/Step3Variant/basic_information.txt mutation_del.txt\n";
        print OUTSH "python $S_Dir/Get_SNP.py $V_Dir/$Sample/Step3Variant/basic_information.txt $Bed_Dir/SNP_Input.txt $V_Dir/$Sample/Step3Variant/${R2}_pileup.snp.vcf uniq_snp_chemo.txt $V_Dir/$Sample/Step3Variant/${R2}_pileup.indel.vcf\n";
        print OUTSH "perl $S_Dir/Count_Lines.pl uniq_snp_chemo.txt snp_chemo.txt\n";
        
        print OUTSH "echo Varscan end pipeline at `date` \n";

        #######################################Factera Fusion
        print OUTSH "mkdir $T_Dir/$Sample\n";
        print OUTSH "cd $T_Dir/$Sample\n";
        if(-e $fusionP){
            open(INF, "$fusionP") || die "Can't open file $fusionP\n";
            while(my $line=<INF>){
                chomp($line);
                my $PRE_FN = $R1.$line;
                print OUTSH "cp $P_Dir/$Sample/$PRE_FN.R1.fastq $T_Dir/$Sample\n";
                print OUTSH "cp $P_Dir/$Sample/$PRE_FN.R2.fastq $T_Dir/$Sample\n";
            }
            print OUTSH "cat $R1*.R1.fastq >$R1.Fusion_R1.fastq\n";
            print OUTSH "cat $R1*.R2.fastq >$R1.Fusion_R2.fastq\n";
            print OUTSH "$soft{bwa} aln -t 8 $dbFile{bwaIndex} $T_Dir/$Sample/$R1.Fusion_R1.fastq > $R1.Fusion.R1.sai\n";
            print OUTSH "$soft{bwa} aln -t 8 $dbFile{bwaIndex} $T_Dir/$Sample/$R1.Fusion_R2.fastq > $R1.Fusion.R2.sai\n";
            print OUTSH "$soft{bwa} sampe $dbFile{bwaIndex} $R1.Fusion.R1.sai $R1.Fusion.R2.sai $T_Dir/$Sample/$R1.Fusion_R1.fastq $T_Dir/$Sample/$R1.Fusion_R2.fastq > $R1.Fusion.sam\n";
            print OUTSH "java -jar $soft{sortSam} SortSam INPUT=$R1.Fusion.sam  OUTPUT=$R1.Fusion.sorted.sam SORT_ORDER=coordinate\n";
            print OUTSH "samtools view -bS -h $R1.Fusion.sorted.sam > $R1.Fusion.sorted.bam\n";
            print OUTSH "java -jar $soft{buildIndex} BuildBamIndex I=$R1.Fusion.sorted.bam\n";
            print OUTSH "perl $soft{factera} $R1.Fusion.sorted.bam $dbFile{FusionExonsBed} $dbFile{Fusion2bit}\n";
            print OUTSH "python $S_Dir/get_Fusion.py $R1.Fusion.sorted.factera.fusions.txt $V_Dir/$Sample/Step3Variant/basic_information.txt $R1.FusionResult.txt\n";
            print OUTSH "$soft{bwa} mem -M -R \"\@RG\\tID:$label{group}\\tSM:$label{sample}\\tPL:$label{platform}\" -t 12 $dbFile{bwaIndex} $T_Dir/$Sample/$R1.Fusion_R1.fastq $T_Dir/$Sample/$R1.Fusion_R2.fastq > $T_Dir/$Sample/$R1.mem.sam\n";
            print OUTSH "java -jar $soft{sortSam} SortSam INPUT=$T_Dir/$Sample/$R1.mem.sam OUTPUT=$T_Dir/$Sample/$R1.mem.sorted.sam SORT_ORDER=coordinate\n";
            print OUTSH "samtools view -bS -h $T_Dir/$Sample/$R1.mem.sorted.sam > $T_Dir/$Sample/$R1.mem.sorted.bam\n";
            print OUTSH "java -jar $soft{buildIndex} BuildBamIndex I=$T_Dir/$Sample/$R1.mem.sorted.bam\n";
            print OUTSH "perl $soft{factera} $T_Dir/$Sample/$R1.mem.sorted.bam $dbFile{FusionExonsBed} $dbFile{Fusion2bit}\n";

        }else{
            next;
        }
        
        print OUTSH "echo Fusion end pipeline at `date` \n";

        ######################################MSI Analysis
        print OUTSH "mkdir $M_Dir/$Sample\n";
        print OUTSH "cd $M_Dir/$Sample\n";
        ######参考序列不变的情况下，MSI.list不变
        #print OUTSH "$soft{msisensor2} scan -d $dbFile{bwaIndex} -o $Bed_Dir/msi.list\n";
        print OUTSH "$soft{msisensor2} msi -d $Bed_Dir/msi.list -t $P_Dir/$Sample/$R1.OntargetFilter.bam -e $Bed_Dir/MSI.sorted.bed -o $R1\_msi.output -l 1 - q 1 -b 2\n";
        print OUTSH "perl $S_Dir/Get_MSI.pl $R1\_msi.output msi_result.txt\n";

        print OUTSH "echo MSI end pipeline at `date` \n";

        print OUTSH "mkdir $R_Dir/$Sample\n";
        print OUTSH "cd $R_Dir/$Sample\n";
        print OUTSH "cp $Bed_Dir/S001报告生成数据库_20200117v1.9.6.xlsx .\n";
        print OUTSH "cp $Bed_Dir/template_CRC_with_msi_v0.5.docx .\n";
        print OUTSH "cp $Bed_Dir/template_CRC_without_msi_v0.5.docx .\n";
        print OUTSH "cp $Bed_Dir/template_NSCLC_with_msi_v0.5.docx .\n";
        print OUTSH "cp $Bed_Dir/template_NSCLC_without_msi_v0.5.docx .\n";
        print OUTSH "cp $S_Dir/template_20191224_linux_v0.13.py .\n";
        print OUTSH "cp $Bed_Dir/country_name.txt .\n";
        print OUTSH "cp $V_Dir/$Sample/Step3Variant/basic_information.txt .\n";
        print OUTSH "cp $V_Dir/$Sample/Step3Variant/mutation_del.txt .\n";
        print OUTSH "perl $S_Dir/Get_SampleNumber.pl basic_information.txt $V_Dir/$Sample/Step3Variant/uniq_snp_chemo.txt\n";
        print OUTSH "perl $S_Dir/Get_SampleNumber.pl basic_information.txt $V_Dir/$Sample/Step3Variant/snp_chemo.txt\n";
        print OUTSH "cp $T_Dir/$Sample/$R1.FusionResult.txt .\n";
        print OUTSH "perl $S_Dir/Get_SampleNumber.pl basic_information.txt $M_Dir/$Sample/msi_result.txt\n";
        print OUTSH "cat mutation_del.txt $R1.FusionResult.txt > mutation_del1.txt\n";
        print OUTSH "perl $S_Dir/Count_SNV_Fusion.pl mutation_del1.txt basic_information.txt mutation_del3.txt mutation_uniq_gene_list.txt\n";
        print OUTSH "perl $S_Dir/Get_SampleNumber.pl basic_information.txt $R_Dir/$Sample/mutation_del3.txt\n";
        print OUTSH "perl $S_Dir/Get_SampleNumber.pl basic_information.txt $R_Dir/$Sample/mutation_uniq_gene_list.txt\n";
        print OUTSH "echo Summary end pipeline at `date` \n";

        print OUTSH "python template_20191224_linux_v0.13.py\n";
        print OUTSH "echo Report end pipeline at `date` \n";

        close OUTSH;
    }
    close PSH;
}
#####  Subroutines  #####

sub get_sample{
    my $listFile = shift;
    my %Sample_h = ();

    my $s_name;
    open(LISTF , "<", $listFile) or die "Error: Open file: $listFile error !\n $!\n";
    while (<LISTF>){
    chomp;
    $s_name = (split/\t/, $_)[0];
    my @s_probes = (split/,/, (split/\t/, $_)[1]);
    $Sample_h{$s_name} = \@s_probes;
    }
    close LISTF;
    return (%Sample_h);
}
    

my ($Sec,$Min,$Hour,$Day,$Mon,$Year,$Wday,$Yday,$Isdst) = localtime();
my $Year_t = $Year + 1900;
my $MONTH = $Mon + 1;
my $Months = (sprintf "%02d", $MONTH);
print $Year_t."-".$Months."-".$Day." ".$Hour.":".$Min.":".$Sec."\n";


