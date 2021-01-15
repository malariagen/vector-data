# Ag3 data download guide

This notebook provides information about how to download data from the [*Anopheles gambiae* 1000 Genomes project (Ag1000G) phase 3](intro). This includes sample metadata, raw sequence reads, sequence read alignments, and single nucleotide polymorphism (SNP) calls.

## About this guide

This guide is written as a Jupyter notebook. Code examples that are intended to be run via a Linux command line are prefixed with an exclamation mark (!). If you are running these commands directly from a terminal, remove the exclamation mark.

Examples in this guide assume you are downloading data to a local folder within your home directory at the path `~/vo_agam_release/`. Change this if you want to download to a different folder on the local file system.

## Data hosting

Ag3 data are hosted by several different services.

Raw sequence reads in FASTQ format, sequence read alignments in BAM format, and SNP calls in VCF format are hosted by the European Nucleotide Archive (ENA). This guide provides examples of downloading data from ENA via FTP using the `wget` command line tool, but please note that there are several other options for downloading data, see the [ENA documentation on how to download data files](https://ena-docs.readthedocs.io/en/latest/retrieval/file-download.html) for more information.  

Sample metadata in CSV format and SNP calls in Zarr format are hosted on Google Cloud Storage (GCS) in the `vo_agam_release` bucket, which is a multi-region bucket located in the United States. All data hosted on GCS are publicly accessible and do not require any authentication to access. This guide provides examples of downloading data from GCS to a local computer using the `gsutil` command line tool. For more information about `gsutil`, see the [gsutil tool documentation](https://cloud.google.com/storage/docs/gsutil).

## Sample sets

Data in this release are organised into 26 sample sets. Each of these sample sets corresponds to a set of mosquito specimens contributed by a collaborating study. Depending on your objectives, you may want to download data from only specific sample sets, or all sample sets. For convenience there is a tab-delimited manifest file listing all sample sets in the release. Here is a direct download link for the sample set manifest:

* https://storage.googleapis.com/vo_agam_release/v3/manifest.tsv

The sample set manifest can also be downloaded via `gsutil` to a directory on the local file system, e.g.:

!mkdir -pv ~/vo_agam_release/v3/
!gsutil cp gs://vo_agam_release/v3/manifest.tsv ~/vo_agam_release/v3/

Here are the file contents:

!cat ~/vo_agam_release/v3/manifest.tsv

For more information about these sample sets, see the section on sample sets in the [introduction to Ag1000G phase 3](intro).

## Sample metadata

Data about the samples that were sequenced to generate this data resource are available, including the time and place of collection, the gender of the specimen, and our call regarding the species of the specimen.

### Specimen collection metadata

Specimen collection metadata can be downloaded from GCS. E.g., here is the download link for the sample metadata for sample set AG1000G-BF-A:

* https://storage.googleapis.com/vo_agam_release/v3/metadata/general/AG1000G-BF-A/samples.meta.csv

Sample metadata for all sample sets can also be downloaded using `gsutil`:

!mkdir -pv ~/vo_agam_release/v3/metadata/
!gsutil -m rsync -r gs://vo_agam_release/v3/metadata/ ~/vo_agam_release/v3/metadata/

Here are the first few rows of the sample metadata for sample set AG1000G-BF-A:

!head ~/vo_agam_release/v3/metadata/general/AG1000G-BF-A/samples.meta.csv

The `sample_id` columns gives the sample identifier used throughout all Ag1000G analyses.

The `country`, `location`, `latitude` and `longitude` columns give the location where the specimen was collected.

The `year` and `month` columns give the approximate date when the specimen was collected.

The `sex_call` column gives the gender as determined from the sequence data.

### Species calls

We have made a call for each specimen as to which species it belongs to (*Anopheles gambiae*, *Anopheles coluzzii*, *Anopheles arabiensis*) based on the genotypes of the samples. These calls were made from the sequence data, and there are cases where the species is not easy to determine. We report species calls using two methods, principal components analysis (PCA) and ancestry informative markers (AIMs). 

Species calls can be downloaded from GCS, e.g., for sample set AG1000G-BF-A:

* PCA species calls - https://storage.googleapis.com/vo_agam_release/v3/metadata/species_calls_20200422/AG1000G-BF-A/samples.species_pca.csv
* AIM species calls - https://storage.googleapis.com/vo_agam_release/v3/metadata/species_calls_20200422/AG1000G-BF-A/samples.species_aim.csv

Alternatively if you ran the `gsutil rsync` command above to download sample metadata then this file will already be present on your local file system.

Here are the first few rows of the AIM species calls for sample set AG1000G-BF-A:

!head ~/vo_agam_release/v3/metadata/species_calls_20200422/AG1000G-BF-A/samples.species_aim.csv

The `species_gambcolu_arabiensis` column provides a call as to whether the specimen is arabiensis or not (gamb_colu).

The `species_gambiae_coluzzii` column applies to samples that are not arabiensis, and differentiates gambiae versus coluzzii.

## Raw sequence reads (FASTQ format)

The raw sequence reads used in this data release can be downloaded from ENA. Note that for most samples there were multiple sequencing runs, and hence there are usually multiple ENA run accessions per sample. For most samples there were 3 sequencing runs, but some samples have 4 and some have a single sequencing run.

To find the ENA run accessions for a given sample, first download the catalog of run accessions:

* https://storage.googleapis.com/vo_agam_release/v3/metadata/ena_runs.csv

Alternatively if you ran the `gsutil rsync` command above to download sample metadata then this file will already be present on your local file system. Inspect the file:

!head ~/vo_agam_release/v3/metadata/ena_runs.csv

For example, the sequence reads for sample AR0001-C are available from three ENA accessions: ERR347035, ERR347047 and ERR352136. To download the sequence reads, visit the ENA website and search for these accessions. E.g., links to download sequence reads for run ERR352136 are available from this web page: https://www.ebi.ac.uk/ena/browser/view/ERR352136. To download the FASTQ files for this run via `wget`:

!wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR352/ERR352136/ERR352136_1.fastq.gz
!wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR352/ERR352136/ERR352136_2.fastq.gz

Note that FASTQ files are relatively large, several GB per sample, so they may take a long time to download, and may require a substantial amount of disk space on your local system.

## Sequence read alignments (BAM format)

Analysis-ready sequence read alignments are available in BAM format for all samples in the release and can be downloaded from ENA. A catalog file mapping sample identifiers to ENA accessions is available at this link:

* https://storage.googleapis.com/vo_agam_release/v3/metadata/ena_alignments.csv

Alternatively if you ran the `gsutil rsync` command above to download sample metadata then this file will already be present on your local file system. Here are the first few rows:

!head ~/vo_agam_release/v3/metadata/ena_alignments.csv

Each row in this file provides a mapping from Ag1000G sample identifiers to ENA analysis accessions. To find links for downloading the data, visit the ENA website and search for the corresponding analysis accession. E.g., the analysis-ready BAM file for sample AR0001-C can be downloaded from this web page: https://www.ebi.ac.uk/ena/browser/view/ERZ1695275. To download the BAM file via `wget`:

!wget ftp://ftp.sra.ebi.ac.uk/vol1/ERZ169/ERZ1695275/AR0001-C.bam

Note that BAM files are relatively large, approximately 10G per sample, so they may take a long time to download, and may require a substantial amount of disk space on your local system.

## SNP calls (VCF format)

### SNP genotypes

SNP genotypes for individual mosquitoes in VCF format will shortly be available from EVA. Please check back soon.

<!--

SNP calls in VCF format are available from EVA. There is one VCF file for each individual sample. A catalog file mapping sample identifiers to EVA accessions is available at this link:

* https://storage.googleapis.com/vo_agam_release/v3/metadata/eva_snp_genotypes.csv (@@TODO)

Alternatively if you ran the `gsutil rsync` command above to download sample metadata then this file will already be present on your local file system. Inspect the file:

!head ~/vo_agam_release/v3/metadata/ena_snp_genotypes.csv

Each row in this file provides a mapping from Ag1000G sample identifiers to EVA analysis accessions. To find links for downloading the data, visit the EVA website and search for the corresponding analysis accession. E.g., the VCF file for sample @@TODO can be downloaded from this web page: @@TODO

Note that each sample has been genotyped at all genome positions (except for those where the reference sequence is 'N') and considering all possible SNP alleles. It is possible to combine VCF files for multiple samples if you need to analyse a multi-sample VCF. E.g., here are commands to download VCFs for three samples then merge them into a single multi-sample VCF:

!@@TODO download and merge VCFs

-->

### Site filters

SNP calling is not always reliable, and we have created some site filters to allow excluding low quality SNPs. We have created some sites-only VCF files with site filter information in the `FILTER` column. These VCF files are hosted on GCS. 

Because different species may have different genome accessibility issues, we have created three separate site filters:

* The "gamb_colu" site filter is designed for working only with samples that are not *An. arabiensis*.
* The "arab" filter is designed for when only working with samples that are *An. arabiensis*.
* The "gamb_colu_arab" filter is suitable for when analysing samples of any species together.

Each filter is available as a set of VCF files, one per chromosome arm. E.g., here is the direct download link for the gamb_colu_arab filters on chromosome arm 3R:

* https://storage.googleapis.com/vo_agam_release/v3/site_filters/dt_20200416/vcf/gamb_colu_arab/3R_sitefilters.vcf.gz

Alternatively, all site filters VCFs can be downloaded using `gsutil`, e.g.:

<!--

@@TODO describe how to use site filters VCFs with the genotypes VCF.

-->

!mkdir -pv ~/vo_agam_release/v3/site_filters/dt_20200416/vcf/
!gsutil -m rsync -r \
    gs://vo_agam_release/v3/site_filters/dt_20200416/vcf/ \
    ~/vo_agam_release/v3/site_filters/dt_20200416/vcf/

## SNP calls (Zarr format)

SNP data are also available in Zarr format, which can be convenient and efficient to use for certain types of analysis. These data can be analysed directly in the cloud without downloading to the local system, see the [Ag3 cloud data access guide](cloud) for more information. The data can also be downloaded to your own system for local analysis if that is more convenient. Below are examples of how to download the Zarr data to your local system.

The data are organised into several Zarr hierarchies. 

### SNP sites and alleles

Data on the genomic positions (sites) and reference and alternate alleles that were genotyped can be downloaded as follows:

!mkdir -pv ~/vo_agam_release/v3/snp_genotypes/all/sites/
!gsutil -m rsync -r \
    gs://vo_agam_release/v3/snp_genotypes/all/sites/ \
    ~/vo_agam_release/v3/snp_genotypes/all/sites/

### Site filters

SNP calling is not always reliable, and we have created some site filters to allow excluding low quality SNPs. To download site filters data in Zarr format, excluding some parts of the data that you probably won't need:

!mkdir -pv ~/vo_agam_release/v3/site_filters/
!gsutil -m rsync -r \
    -x '.*vcf.*|.*crosses_stats.*|.*[MG]Q10.*|.*[MG]Q30.*|.*[MG]Q_mean.*|.*[MG]Q_std.*|.*/lo_.*|.*/hi_.*|.*no_cov.*|.*allele_consistency.*|.*heterozygosity.*' \
    gs://vo_agam_release/v3/site_filters/ \
    ~/vo_agam_release/v3/site_filters/

### SNP genotypes

SNP genotypes are available for each sample set separately. E.g., to download SNP genotypes in Zarr format for sample set AG1000G-BF-A, excluding some data you probably won't need:

!mkdir -pv ~/vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-A/
!gsutil -m rsync -r \
        -x '.*/calldata/(AD|GQ|MQ)/.*' \
        gs://vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-A/ \
        ~/vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-A/

## Accessing downloaded data from Python

There are a wide variety of tools available for analysing the data from Ag1000G phase 3 once downloaded to your local system. If you would like to ask about possible approaches for a given analysis, please feel free to [start a new discussion](https://github.com/malariagen/vector-public-data/discussions/new) on the malariagen/vector-public-data repo on GitHub. 

Within the MalariaGEN vector genomics team we primarily use the Python programming language for analysing the SNP data, making use of software packages in the Scientific Python / PyData ecosystem. This section gives some simple examples illustrating how to use these tools to read downloaded data.

These examples use data from two sample sets, AG1000G-BF-A and AG1000G-BF-B. 

Firstly, here are all the commands again to download the data needed to run these examples (requires about 10G of local storage):

# download sample set manifest
!mkdir -pv ~/vo_agam_release/v3/
!gsutil cp gs://vo_agam_release/v3/manifest.tsv ~/vo_agam_release/v3/

# download sample metadata
!mkdir -pv ~/vo_agam_release/v3/metadata/
!gsutil -m rsync -r gs://vo_agam_release/v3/metadata/ ~/vo_agam_release/v3/metadata/

# download sites data
!mkdir -pv ~/vo_agam_release/v3/snp_genotypes/all/sites/
!gsutil -m rsync -r \
    gs://vo_agam_release/v3/snp_genotypes/all/sites/ \
    ~/vo_agam_release/v3/snp_genotypes/all/sites/

# download site filters data
!mkdir -pv ~/vo_agam_release/v3/site_filters/
!gsutil -m rsync -r \
    -x '.*vcf.*|.*crosses_stats.*|.*[MG]Q10.*|.*[MG]Q30.*|.*[MG]Q_mean.*|.*[MG]Q_std.*|.*/lo_.*|.*/hi_.*|.*no_cov.*|.*allele_consistency.*|.*heterozygosity.*' \
    gs://vo_agam_release/v3/site_filters/ \
    ~/vo_agam_release/v3/site_filters/

# download SNP genotype data for two sample sets
!mkdir -pv ~/vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-A/
!gsutil -m rsync -r \
        -x '.*/calldata/(AD|GQ|MQ)/.*' \
        gs://vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-A/ \
        ~/vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-A/
!mkdir -pv ~/vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-B/
!gsutil -m rsync -r \
        -x '.*/calldata/(AD|GQ|MQ)/.*' \
        gs://vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-B/ \
        ~/vo_agam_release/v3/snp_genotypes/all/AG1000G-BF-B/


The following Python packages need to be installed on the local system: numpy, dask, zarr, gcsfs, fsspec, scikit-allel. These packages can be installed via pip or conda. E.g.:

!pip install numpy dask[array] zarr gcsfs fsspec scikit-allel

To make accessing these data more convenient, we've also created a [malariagen_data Python package](https://github.com/malariagen/malariagen-data-python), which is available from PyPI. This is experimental so please let us know if you find any bugs or have any suggestions. The `malariagen_data` package can be installed via pip, e.g.:

!pip install malariagen-data

Set up access to the Ag1000G phase 3 data, at the local path where data were downloaded:

import malariagen_data
ag3 = malariagen_data.Ag3("~/vo_agam_release/")

Examples of reading/opening various files:

# read sample set manifest into a pandas dataframe
df_sample_sets = ag3.sample_sets()
df_sample_sets

# read sample metadata for AG1000G-BF-A and AG1000G-BF-B into a pandas dataframe
df_samples = ag3.sample_metadata(sample_sets=['AG1000G-BF-A', 'AG1000G-BF-B'])
df_samples

# inspect number of samples by species
df_samples.groupby("species").size()

# access SNP positions and alleles for chromosome arm 3R as dask arrays
pos, ref, alt = ag3.snp_sites("3R")
pos

ref

alt

# read first 10 SNP positions into a numpy array
p = pos[:10].compute()
p

# read first 10 SNP reference alleles
r = ref[:10].compute()
r

# read first 10 SNP alternate alleles
a = alt[:10].compute()
a

# access gamb_colu_arab site filters for chromosome arm 3R as a dask array
filter_pass = ag3.site_filters("3R", mask="gamb_colu_arab")
filter_pass

# read filter values for first 10 SNPs (True means the site passes filters)
f = filter_pass[:10].compute()
f

# access SNP genotypes for AG1000G-BF-A and AG1000G-BF-B as a dask array
gt = ag3.snp_genotypes("3R", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"])
gt

Genotypes are stored as a three-dimensional array, where the first dimension corresponds to genomic positions, the second dimension is samples, and the third dimension is ploidy (2). Values coded as integers, where -1 represents a missing value, 0 represents the reference allele, and 1, 2, and 3 represent alternate alleles.

# e.g., read genotypes for the first 5 SNPs and the first 3 samples
g = gt[:5, :3, :].compute()
g

Here's an example computation to count the number of segregating SNPs on chromosome arm 3R that also pass gamb_colu_arab site filters:

# import scikit-allel
import allel

# import dask progress bar
from dask.diagnostics.progress import ProgressBar

# import numpy
import numpy as np

# choose chromosome arm
seq_id = "3R"

# choose site filter mask
mask = "gamb_colu_arab"

# choose sample sets
sample_sets = ["AG1000G-BF-A", "AG1000G-BF-B"]

# locate pass sites
loc_pass = ag3.site_filters(seq_id=seq_id, mask=mask).compute()

# perform an allele count over genotypes
gt = ag3.snp_genotypes(seq_id=seq_id, sample_sets=sample_sets)
gt = allel.GenotypeDaskArray(gt)
with ProgressBar():
    ac = gt.count_alleles(max_allele=3).compute()
    
# locate segregating sites
loc_seg = ac.is_segregating()

# count segregating and pass sites
np.count_nonzero(loc_pass & loc_seg)

## Further reading

We will hopefully be able to write up further examples of analysing data soon, so please follow [@malariagenomics](https://twitter.com/malariagenomics) on Twitter or keep an eye on the [malariagen/vector-public-data GitHub discussion board](https://github.com/malariagen/vector-public-data/discussions).