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
pipelines are also available from GitHub. Following successful
completion of these pipelines, samples entered the sample quality
control (QC) process described below.


## Sample QC

The following subsections describe analyses performed to identify and
exclude samples from the final dataset.


### Coverage

For each sample, depth of coverage was computed at all genome
positions. Samples were excluded if median coverage across all
chromosomes was less than 10×, or if less than 50% of the reference
genome was covered by at least 1×.


### Cross-contamination

To identify samples affected by cross-contamination, we implemented
the model for detecting contamination in NGS alignments described in
[Jun et
al. (2012)](https://doi.org/10.1016/j.ajhg.2012.09.004). Briefly, the
method estimates the likelihood of the observed alternate and
reference allele counts under different contamination fractions, given
approximate population allele frequencies. Population allele
frequencies were estimated from the [Ag1000G phase 2 data
release](https://www.malariagen.net/resource/27). The model computes a
maximum likelihood value for a parameter *alpha* representing
percentage contamination. Samples were excluded if *alpha* was 4.5% or
greater.


### Technical replicates

A number of samples were sequenced more than once within this project
phase (technical replicates). To create a final dataset without any
replicates suitable for population genetic analysis, we performed an
analysis to confirm all technical replicates, and to choose the sample
within each replicate with the best sequencing data. We computed
pairwise genetic distance between all sample pairs within a sample
set. The distance metric used was city block distance between genotype
allele counts, to allow for handling of multiallelic SNPs.  So, e.g.,
distance between genotypes of 0/1 and 0/1 is 0, distance between 0/0
and 0/1 is 2, distance between 0/1 and 1/2 is 2, distance between 0/0
and 1/1 is 4, etc. For each pair of samples, distance was averaged
over all sites where both samples had a non-missing genotype
call. Computations were initially carried out on a down-sampled set of
10 x 100,000 contiguous genomic sites, to be computationally
feasible. Where a pair of samples fell beneath a conservative
threshold of 0.012, the genetic distance was then recomputed across
all genomic sites (i.e., without down-sampling).  For each pair of
samples that were expected to be technical replicates according to our
metadata records, we excluded both members of the pair if genetic
distance was above 0.006.  Where an expected replicate pair had
genetic distance below 0.006, we retained only one sample in the pair.
We also identified and excluded both samples in any pair where genetic
distance was below 0.006, but the samples were not expected to be
replicates.


### Population outliers and anomaly detection

We used principal component analysis (PCA) to identify and exclude
individual samples that were population outliers. SNPs were
down-sampled to use 100,000 segregating non-singleton sites from
chromosomes 3R and 3L, to avoid regions complicated by known
introgression loci or paracentric inversions. PCA was computed using
scikit-allel version 1.2.0. We iteratively identified and excluded any
individual samples that were outliers along a single principal
component. We then identified and excluded any individual samples or
small sample groups that clustered together with other samples in a
way that was not plausible given metadata regarding their collection
location.


### Colony crosses

Samples in the AG1000G-X sample set were parents and progeny from
colony crosses and were subject to a slightly different set of QC
steps. For each cross, we performed an analysis of Mendelian
inheritance and consistency to confirm the true parents and the
validity of the cross. Not all crosses were able to be successfully
resolved, and samples that were not in a resolved cross were excluded.
From the samples originally submitted in the AG1000G-X sample set, 297
samples from 15 crosses were retained for release. We did not include
the colony crosses in the population outlier analysis due to their
relatedness.


### Sex calling

We called the sex of all samples based on the modal coverage ratio
between the X chromosome and the autosomal chromosome arm 3R. The
sample was classed as male where the coverage ratio was between
0.4-0.6, and female between 0.8-1.2. Where the ratio was outside these
limits, the sample was excluded. One of the sample sets from The
Gambia, AG1000G-GM-B, included whole-genome amplified (WGA) samples
which displayed some skew in their coverage ratios, which meant that
sex could not be called via the same process. These samples received a
sex call where possible, but no samples were excluded based on
uncertain sex call.


## Species assignment

We assigned a species to each individual that passed sample QC using
their genomic data, via two independent methods: ancestry-informative
markers (AIMs) and principal components analysis (PCA).


### Species calling via ancestry-informative markers (AIMs)

We derive AIMs between *An. arabiensis* and *An. gambiae* using
publicly available data from the *Anopheles* 16 genomes project
([Neafsey et
al. 2015](https://doi.org/10.1126/science.1258522)). Whole genome
SNP calls for 12 *An. arabiensis* and 38 *An. gambiae* individuals
were used. Alleles were mapped onto the same alternate allele space,
and allele frequencies were computed for both species. Sites that were
multiallelic in either group were excluded, as well as sites where any
genotypes were missing. 565,329 SNPs were identified as potentially
informative, where no shared alleles were present between
groups. These were spread throughout the genome, but were concentrated
on the X chromosome (63.2%), particularly around the Xag inversion. We
randomly down-sampled these SNPs to a set of 50,000 AIMs, then
computed the fraction of alleles at these SNPs that were
arabiensis-like for each individual in the Ag1000G phase 3 cohort.
Given the relatively small number of *An. arabiensis* samples in the
16 genomes project, it was clear that a significant proportion of
putative AIMs were not likely to be truly informative across the
broader sampling in Ag1000G phase 3. Individuals in Ag1000G were
classed as *An. arabiensis* where a fraction >0.6 of alleles were
arabiensis-like.

To resolve the non-arabiensis individuals into *An. gambiae* and
*An. coluzzii*, we applied the AIMs previously used in [Ag1000G phase
2](https://www.malariagen.net/resource/27). For each individual, we
computed the fraction of coluzzii-like alleles at these
AIMs. Individuals were called as *An. gambiae* where this fraction was
<0.12 and *An. coluzzii* where this fraction was >0.9, with
individuals in between classed as intermediate.


### Species calling via PCA

To provide a complementary view of species assignments, we also used
the results of the principal components analysis of Chromosome 3
computed during the outlier analysis described above. Based on a
comparison with the AIM species calls, it was apparent that the first
two principal components could be used to assign species. Individuals
where PC1 >150 were called as *An. arabiensis*.  Individuals where PC1
<0 and PC2 >-7 were called as *An. gambiae*.  Individuals where PC1 <0
and PC2 <-24 were called as *An. coluzzii*.  All other individuals
were called as intermediate. The results of the PCA and AIM species
calls were highly concordant in most sample sets, except for the Far
West (Guinea-Bissau, The Gambia) and Far East (Kenya,
Tanzania). Further investigation is required to resolve the species
status of these individuals.


## Site filtering

We developed filters that identify genomic sites where SNP calling and
genotyping is likely to be less reliable in one or more mosquito
species. To guide the design and calibration of the site filters, we
made use of the 15 colony crosses included in Ag1000G phase 3. Each
cross comprises two parents and up to 20 progeny, and thus it is
possible to identify sites where genotypes in one or more progeny are
not consistent with Mendelian inheritance (Mendelian errors). A small
number of Mendelian errors may be due to *de novo* mutation, but the
vast majority of Mendelian errors are likely to be due to errors in
sequencing, alignment or SNP calling. The general approach we took
was to use Mendelian consistency to identify sets of positive and
negative training sites, then used these to train a machine learning
model that classified all genomic sites as either PASS or FAIL.


### Site filters for use with *An. gambiae* and/or *An. coluzzii*

All the 15 crosses involved *An. gambiae* and/or *An. coluzzii*
parents, and none of the crosses involved *An. arabiensis*, so we used
the crosses to first develop site filters suitable for use with
*An. gambiae* and/or *An. coluzzii*. Hereafter we refer to these
filters as the "gamb_colu" site filters. Five of the 15 crosses were
held out for validation, so performance could be evaluated
objectively. Sites were assigned to the positive training set where
all genotypes across all 10 crosses were called, and no Mendelian
errors were observed. Sites were assigned to negative training set
where one or more Mendelian errors were observed in any cross. All
other sites were not considered eligible for inclusion in model
training. A balanced training set was then generated containing
100,000 autosomal sites from each of the positive and negative
training sets.


The inputs to the machine learning model were a set of per-site
summary statistics computed from the sequence read alignments and SNP
genotypes across all wild-caught *An. gambiae* and *An. coluzzii*
individuals. These input summary statistics are described further in
the appendix. Male individuals were excluded from the summary
statistic calculations, so that the model could also be applied
without modification to the X chromosome. We used these summary
statistics, together with the positive and negative training sites, to
train a decision tree model. We initially trained a set of trees with
different hyperparameter values, exploring the depth of trees, and the
number of samples allowed at a terminal node. Each of these trees was
evaluated on an unbalanced set of sites randomly sampled from the
whole genome (2% of all sites, without replacement). Leaves of these
trees contained different proportions of positive and negative
training sites, and by increasing the cutoff for these proportions
required to label a leaf as PASS, we were able to compute the area
under the receiver operating curve (AUROC) for each set of
hyperparameter values. The best performing hyperparameter set based on
AUROC was selected as the final model, and the leaf classification
cutoff used was optimised based on the Youden statistic. The resulting
model was a decision tree of depth 8, where leaves were assigned to
PASS where > 0.533 of training data in that leaf were positive
training sites. All sites in the genome were then assigned to PASS or
FAIL via this model.

The 5 remaining cross pedigrees were used to perform a final
evaluation of the approach. For each of these crosses, we computed the
Mendelian error rate (fraction of variants with one or more Mendelian
errors among progeny) before and after applying the site filters, to
provide five independent evaluation results. We also evaluated
performance on the X chromosome using heterozygote calls in males as
an error indicator. The fraction of variants with a heterozygous
genotype call in or more males was computed before and after applying
site filters. Male error rates were estimated from genotype calls with
a minimum Genotype Quality (GQ) value of 30. Performance of the
decision tree model was better than the hand-crafted site filters
created during the previous project phase (Ag1000G phase 2), with
lower Mendelian error rates, and a larger number of sites passing the
filter. Full performance metrics will be reported in a future
publication.


### Site filters for use with *An. arabiensis*

To generate site filters for use with *An. arabiensis*, we recomputed
site summary statistics using only wild-caught *An. arabiensis*
individuals, then applied the decision tree model described
above. These filters, which we refer to as the "arab"" site filters,
are appropriate when working with *An. arabiensis* samples only.


### Site filters for joint analyses of all three species

We created site filters suitable for joint analysis of individuals
from all three species by taking the intersection of the "gamb_colu"
and the "arab" site filters. We refer to these filters as the
"gamb_colu_arab"" site filters.


## CNV calling

Copy number variant (CNV) calling methods followed those described in
[Lucas et
al. (2019)](https://genome.cshlp.org/content/29/8/1250.full#sec-8)
with some adaptations to accommodate the different mosquito species
being analysed, described further below.


### Calculation and normalization of coverage

For each individual, we used
[pysam](https://github.com/pysam-developers/pysam) to count the number
of aligned reads (coverage) in non-overlapping 300 bp windows over the
nuclear genome. The position of each read was considered to be its
alignment start point; thus, each read was only counted once.

Sequencing coverage can be biased by variation in local nucleotide
composition. To account for this, we computed a normalized coverage
from the read counts based on the expected coverage of each window
given its GC content ([Abyzov et
al. 2011](https://doi.org/10.1101/gr.114876.110)). For each 300 bp
window we computed the percentage of (G+C) nucleotides to the nearest
percentage point within the reference sequence and then divided the
read counts in each window by the median read count over all autosomal
windows with the same (G+C) percentage. To minimize the impact of copy
number variation when calculating these normalizing constants, we
excluded windows from the calculation of mean read counts with <90%
sites passing site filters or with >50% reads aligned with zero
mapping quality. The normalized coverage values were then multiplied
by a factor of 2, so that genome regions with a normal diploid copy
number should have an expected normalized coverage of 2.

Before examining the normalized coverage data for evidence of copy
number variation, we applied two filters to exclude windows for which
coverage may be an unreliable indicator of copy number. The first
filter removed windows in which >50% of reads were aligned with
mapping quality 0, which indicates that a read is mapped ambiguously
and could be mapped equally well to a different genomic location. This
filter was calculated separately for *An. arabiensis* and
(*An. gambiae* + *An. coluzzii*). The second filter removed windows
for which the percentage (G+C) content was extreme and rarely
represented within the accessible reference sequence, that is, fewer
than 100 accessible windows with the same (G+C) percentage, because
the small number of windows makes the calculation of a (G+C)
normalizing constant unreliable. Windows retained for analysis were
referred to as "filtered windows". The filtered windows were computed
separately for *An. arabiensis* and for (*An. gambiae* +
*An. coluzzii*), based on the AIM species calls, to account for
differences between the species.  One individual with an intermediate
species call between these two groups were excluded.


### HMM inference of copy number state

To infer the most likely copy number state (CN) at each window in each
individual, we applied a Gaussian hidden Markov model (HMM) to the
individual's normalized windowed coverage data, following a similar
approach to [Miles et
al. (2016)](https://doi.org/10.1101/gr.203711.115) and [Leffler et
al. (2017)](https://doi.org/10.1126/science.aam6393). The HMM was
implemented using the `GaussianHMM` function from
[hmmlearn](https://hmmlearn.readthedocs.io/en/latest/). The HMM
contained 13 hidden states (*c*), representing CN from 0 to 12 in
increments of 1, allowing the detection of up to 6-fold amplication of
a genetic region (the normal diploid complement of two copies of a
genetic region is represented by a CN of 2, a single duplication on
one chromosome is represented by 3, and so on). The Gaussian emission
probability distribution for each copy number state *n* had a mean
*c<sub>n</sub>* (*c<sub>n</sub>* = *n*), with variance *v<sub>n</sub>*
= 0.01 + *a<sub>n</sub>c<sub>n</sub>*, where *a<sub>n</sub>* is the
variance in normalised coverage for all autosomal windows, excluding
the top 1% of windows with the highest normalised coverage. We
determined the variance empirically for each individual because
variance in coverage can differ between individuals, presumably due to
stochastic variation in library preparation and/or sequencing
runs. Following [Lucas et
al. (2019)](https://genome.cshlp.org/content/29/8/1250.full#sec-8) we
set the HMM transition probability *t* = 0.00001. After parameter
calibration, we fitted a Gaussian HMM to normalised windowed coverage
data for each individual, to obtain a predicted copy number state
within each window.


### Genome-wide CNV discovery and filtering ("coverage calls")

Using the results of the HMM, we obtained a set of CNV calls for each
individual by locating contiguous runs of at least five windows with
amplified copy number (CN > 2, or CN > 1 for Chromosome X in
males). This set of per-individual CNV calls was filtered by computing
likelihoods for each CNV call for both the copy number state predicted
by the HMM and for a null model of copy number = 2, and removing CNV
calls for which the likelihood ratio was <1000.

From the per-individual CNV call set, we created a merged set CNV
calls. We first removed individuals with high coverage variance, where
the variance in normalized coverage was greater than 0.2, because high
variance could lead to erratic CNV calls. We then clustered the CNV
calls across individuals, merging two CNV calls into the same variant
if their breakpoints (inferred from the change in CN state) occurred
within one 300 bp window of each other. Merged CNVs were annotated to
record a confidence interval for the start and end breakpoints,
calculated as the 5-95 percentiles within each cluster. A filter
annotation was added to the final output VCF file where this
confidence interval was greater than 1200 bp for either the start or
end breakpoint.

The CNV merging process was performed separately for wild-caught
*An. arabiensis*, wild-caught (*An. gambiae* + *An. coluzzii*), and
the crosses, producing three sets of "CNV coverage calls".


### Identifying CNV alleles at insecticide resistance loci ("discordant read calls")

We characterized in detail the different duplication events (CNV
alleles) at six loci containing genes of particular interest
(Cyp6aa1–Cyp6p2, Gstu4–Gste3, Cyp6m2–Cyp6m4, Cyp6z3–Cyp6z1, Cyp9k1,
Ace1) using their unique patterns of discordant read pairs and reads
crossing the CNV breakpoint ("breakpoint reads"). We manually
inspected the six regions of interest in all individuals to identify
patterns of discordant and breakpoint reads ("diagnostic reads")
consistently associated with changes in coverage. The start and end
point of each CNV allele could usually be precisely determined by the
breakpoint reads and was otherwise determined by discordant read pairs
or the point of change in coverage. Once the diagnostic reads were
identified for a CNV allele, we recorded the presence of that allele
in all samples with at least four supporting diagnostic reads.


## Acknowledgments

We would like to thank the staff of the Wellcome Sanger Institute
Sample Logistics, Sequencing and Informatics facilities for their
contributions to the production of this data release.

We would like to thank the members of the Data Engineering team of the
Broad Institute of Harvard and MIT for their work on open source
implementations of the alignment and SNP calling pipelines used in
Ag1000G phase 3.


## Appendices


### Summary statistics used as input to site filter models

* **No Coverage** -- Number of samples with no coverage whatsoever at
  the given position.

* **Low Coverage** -- Number of samples with low depth of coverage at
  the given position (less than half modal coverage for whole
  chromosome).

* **Low Coverage GC normalised** -- Number of samples with low depth
  of GC-normalised coverage at the given position (less than half
  modal GC-normalised coverage for whole chromosome).

* **High Coverage** -- Number of samples with high depth of coverage
  at the given position (more than twice modal coverage for the whole
  chromosome).

* **High Coverage GC normed** -- Number of samples with high depth of
  GC-normalised coverage at the given position (more than twice modal
  GC-normalised coverage for the whole chromosome).

* **Mean GQ** -- Mean of genotype quality across samples.

* **Median GQ** -- Median of genotype quality across samples.

* **Variance GQ** -- Variance of genotype quality across samples.

* **Low GQ 30** -- Number of samples with a genotype quality <30.

* **Low GQ 10** -- Number of samples with a genotype quality <10.

* **Low MQ** -- Number of samples with root-mean-square mapping
  quality <30.

* **Median MQ** -- Median of root-mean-square mapping quality across
  samples.

* **Mean MQ** -- Mean of root-mean-square mapping quality across
  samples.

* **Variance MQ** -- Variance of root-mean-square mapping quality
  across samples.

* **Error Fraction** -- Fraction of samples with an allele not called
  in the genotype.

* **Allele Balance Het** -- Product of binomial probability of read
  counts at het calls.