# Ag3 sequencing and variant calling methods

This page contains a brief description of sequencing and variant
calling methods used in phase 3 of the *Anopheles gambiae* 1000
Genomes Project (Ag1000G). This is a preliminary version of methods
that will be released in final form as part of a future publication by
the Ag1000G Consortium.


## Whole-genome sequencing

All library preparation and sequencing was performed at the Wellcome
Sanger Institute. Paired-end multiplex libraries were prepared using
the manufacturer's protocol, with the exception that genomic DNA was
fragmented using Covaris Adaptive Focused Acoustics rather than
nebulization. Multiplexes comprised 12 tagged individual mosquitoes
and three lanes of sequencing were generated for each multiplex to
even out variations in yield between sequencing runs. Cluster
generation and sequencing were undertaken according to the
manufacturer's protocol for paired-end sequence reads with insert size
in the range 100--200 bp. 4,693 individual mosquitoes were sequenced
in total, of which 3,130 were sequenced using the Illumina HiSeq 2000
platform and 1,563 were sequenced using the Illumina HiSeq X platform.
All individuals were sequenced to a target coverage of 30×.  The HiSeq
2000 sequencing runs generated 100 bp paired-end reads, and the HiSeq
X sequencing runs generated 150 bp paired-end reads.


## Alignment and SNP calling

Reads were aligned to the AgamP4 reference genome using BWA version
0.7.15. Indel realignment was performed using GATK version 3.7-0
`RealignerTargetCreator` and `IndelRealigner`. Single nucleotide
polymorphisms were called using GATK version 3.7-0
`UnifiedGenotyper`. Genotypes were called for each sample
independently, in genotyping mode, given all possible alleles at all
genomic sites where the reference base was not "N". Coverage was
capped at 250× by random down-sampling. Complete specifications of the
[alignment](https://github.com/malariagen/pipelines/blob/v0.0.4/docs/specs/short-read-alignment-vector.md)
and
[genotyping](https://github.com/malariagen/pipelines/blob/v0.0.4/docs/specs/snp-genotyping-vector.md)
pipelines are available from the [malariagen/pipelines GitHub
repository](https://github.com/malariagen/pipelines). Open source WDL
implementations of the
[alignment](https://github.com/malariagen/pipelines/tree/v0.0.4/pipelines/short-read-alignment-vector)
and
[genotyping](https://github.com/malariagen/pipelines/tree/v0.0.4/pipelines/SNP-genotyping-vector)
pipelines are also available from GitHub.

Following successful completion of these pipelines, samples entered
the sample quality control (QC) process described below.
