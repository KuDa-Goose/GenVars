#!/usr/bin/perl
package ToolsCfg;
use warnings;
use strict;

our %geno_lib = (
    refFa   => "/thinker/net/Analysis_Projects/Reference/Ontarget_Reference/S001_N_Ref/hg38_GenoN.fasta",
    bwaIndex=> "/thinker/net/Analysis_Projects/Reference/Ontarget_Reference/S001_N_Ref/hg38_GenoN.fasta",
    FusionExonsBed => "/thinker/net/Analysis_Projects/Reference/hg38/S001.bed",
    Fusion2bit=> "/thinker/net/Analysis_Projects/Reference/Ontarget_Reference/S001_N_Ref/hg38_GenoN.2bit",
    hg38_2bit=> "/thinker/storage/Reference/Reference/hg38/hg38.2bit",
    #annoDB  => "/thinker/Software/humandb/"
);

our %BioTools = (
    fastqc  => "/thinker/net/Analysis_Projects/Software/FastQC/fastqc",
    iTools  => "/thinker/net/Analysis_Projects/Software/iTools_Code/iTools",
    bwa     => "/thinker/net/Analysis_Projects/Software/bwa-0.7.13/bwa",
    sortSam => "/thinker/net/Analysis_Projects/Software/picard/build/libs/picard.jar",
    buildIndex => "/thinker/net/Analysis_Projects/Software/picard/build/libs/picard.jar",
    picard     => "/thinker/net/Analysis_Projects/Software/picard/build/libs/picard.jar",
    varscan    => "/thinker/net/Analysis_Projects/Software/VarScan.v2.3.8.jar",
    cutadapt   => "/home/storage/Software/anaconda3/bin/cutadapt",
    samToFastq => "/thinker/net/Analysis_Projects/Software/picard/build/libs/picard.jar",
    factera    => "/thinker/net/Analysis_Projects/Software/factera.pl",
    #tophat    => "/thinker/Software/tophat-2.1.1.Linux_x86_64/tophat",
    fgbio      => "/thinker/net/Analysis_Projects/Software/fgbio/fgbio-1.0.0.jar",
    msisensor2 => "/thinker/net/Analysis_Projects/Software/MSISensor/msisensor2/msisensor2",
    twoBitToFa => "/thinker/storage/Software/twoBitToFa",
    igvtools   => "/thinker/storage/Software/IGVTools/igvtools"
);

our %MetaInfo = (
    sample     =>"S001",
    group      =>"NGS",
    platform   =>"Illumina"
);
