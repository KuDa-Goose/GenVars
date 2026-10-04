# SABEL Pipeline

**Version:** 0.9.1.0

---

## Function

The SABEL pipeline is used to analyze NGS data (FASTQ format). It was originally
developed for data generated from the **Ion Proton** platform, and has since been
modified to support **Illumina** data flow.

The pipeline is composed of the following modules:

| # | Module | Description |
|---|--------|-------------|
| 1 | `read_List` | Parse the FASTQ list file and build the sample / probe matrix |
| 2 | `Probe_Shell` | Probe-level analysis (cutadapt, UMI extraction, BWA alignment, on-target calculation) |
| 3 | `VarScan_Shell` | SNV / InDel calling with VarScan and variant annotation |
| 4 | `Extract_Reads` | Read extraction for fusion analysis |
| 5 | `Comparison_Stat` | Fusion detection (FACTERA) and MSI detection (MSISensor2) |
| 6 | `Report` | Summary tables and Word report generation |

> Version history: the pipeline was updated to **0.8.0.0** on June 27, 2018, and
> to the current **0.9.1.0** release.

---

## Software

The bioinformatic software used in the SABEL pipeline and its version information:

| Software | Version |
|----------|---------|
| FastQC | v0.11.5 |
| iTools | v0.16 |
| bwa | v0.7.13-r1126 |
| picard | v2.9.4-2 |
| VarScan | v2.3 |
| cutadapt | v1.14 |
| samtools | v1.5 |
| FACTERA | perl script |
| fgbio | v1.0.0 |
| MSISensor2 | — |
| IGVTools | — |
| twoBitToFa | — |
| LaTeX | TeX Live 2017 |
| Python | v3.6.0 |
| bowtie2 | v2.3.2 |
| bowtie | v1.1.2 |
| R | v3.4.0 |

Tool paths and reference files are configured in `../lib/ToolsCfg.pm`.

---

## Usage

### Command

```bash
perl /path/to/SABEL_0.9.1.0/Main/SABEL_0.9.1.0.pl \
    -i fq_list \
    -d fastq_dir \
    -b ontarget_bed \
    -a all_report_dir \
    [-o output_dir] \
    [-n process_number] \
    [-q avg_qual] \
    [-c] \
    [-f fusion_probe] \
    [-t time] \
    [-e SampleInfo]
```

### Options

| Option | Long name | Required | Description |
|--------|-----------|:--------:|-------------|
| `-i` | `input` | ✅ | List file storing the FASTQ file names |
| `-d` | `fq` | ✅ | Directory containing the FASTQ files |
| `-b` | `ontar_bed` | ✅ | Absolute path of the BED file used for on-target calculation |
| `-a` | `allreport` | ✅ | Directory holding the summary of all sample analysis results |
| `-o` | `output` | ✖ | Output directory (default: `Results_<YYYY>_<MM>_<DD>`) |
| `-n` | `num_p` | ✖ | Maximal number of samples processed in parallel (default: `3`) |
| `-q` | `avg_qual` | ✖ | `--min-avg-qual` threshold for VarScan (default: `15`) |
| `-c` | `cut` | ✖ | Run `cutadapt` before VarScan and probe analysis; not used by default |
| `-f` | `fusionP` | ✖ | Fusion probe TXT file |
| `-t` | `time` | ✖ | Date used for generating machine learning data |
| `-e` | `SampleInfo` | ✖ | Sample information TXT file |
| `-h` | `help` | ✖ | Print the help information of the pipeline |

### Input file format

The FASTQ list file (`-i`) is **tab separated**:

```text
IonXpress_003_R_*.fastq	probe1,probe2,probe3,probe4,probe5
IonXpress_004_R_*.fastq	probe1,probe2,probe3,probe4,probe5
```

---

## Directory layout

```text
SABEL_0.9.1.0/
├── Main/
│   ├── README.md        # This document
│   └── SABEL_0.9.1.0.pl # Pipeline entry point
├── lib/                 # Perl / Python / R helper scripts and configurations
└── bed/                 # BED files, probe lists and reference annotation tables
```

---

## License

Internal use only.