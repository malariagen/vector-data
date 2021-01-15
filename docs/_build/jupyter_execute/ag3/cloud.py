# Ag3 cloud data access guide

This page provides information about how to access data from [*Anopheles gambiae* 1000 Genomes project (Ag1000G) phase 3](intro) via Google Cloud. This includes sample metadata and single nucleotide polymorphism (SNP) calls.

## About this guide

This guide is written as a Jupyter notebook. It illustrates how to read data directly from the cloud, without having to first download any data locally. This notebook can be run from any computer, but will work best when run from a compute node within Google Cloud, because it will be physically closer to the data and so data transfer is faster. For example, this notebook can be run via [MyBinder](https://gke.mybinder.org) or [Google Colab](https://colab.research.google.com/) which are free interactive computing service running in the cloud.

To launch this notebook in the cloud and run it for yourself, click the rocket icon at the top of the page and select one of the cloud computing services available.

## Data hosting

All data required for this notebook is hosted on Google Cloud Storage (GCS). Data are hosted in the `vo_agam_release` bucket, which is a multi-region bucket located in the United States. All data hosted in GCS are publicly accessible and do not require any authentication to access. 

## Setup

Running this notebook requires the following Python packages to be installed: numpy, dask, zarr, gcsfs, fsspec, scikit-allel. These packages can be installed via pip or conda. E.g.:

!pip install numpy dask[array] zarr gcsfs fsspec scikit-allel

To make accessing these data more convenient, we've also created a [malariagen_data Python package](https://github.com/malariagen/malariagen-data-python), which is available from PyPI. This is experimental so please let us know if you find any bugs or have any suggestions. The `malariagen_data` package can be installed via pip, e.g.:

!pip install malariagen-data

Once installed, data access from GCS is set up with the following code:

import malariagen_data
ag3 = malariagen_data.Ag3("gs://vo_agam_release/")

## Sample sets

Data in this release are organised into 26 sample sets. Each of these sample sets corresponds to a set of mosquito specimens contributed by a collaborating study. Depending on your objectives, you may want to access data from only specific sample sets, or all sample sets.

To see which sample sets are available, load the sample set manifest into a pandas dataframe:

df_sample_sets = ag3.sample_sets()
df_sample_sets

For more information about these sample sets, see the section on sample sets in the [introduction to Ag1000G phase 3](intro).

## Sample metadata

Data about the samples that were sequenced to generate this data resource are available, including the time and place of collection, the gender of the specimen, and our call regarding the species of the specimen. These are organised by sample set.

E.g., load sample metadata for the AG1000G-BF-A and AG1000G-BF-B sample sets into a pandas dataframe:

df_samples = ag3.sample_metadata(sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"])
df_samples

The `sample_id` column gives the sample identifier used throughout all Ag1000G analyses.

The `country`, `location`, `latitude` and `longitude` columns give the location where the specimen was collected.

The `year` and `month` columns give the approximate date when the specimen was collected.

The `sex_call` column gives the gender as determined from the sequence data.

To load metadata for all wild-caught samples, you can use the shortcut "v3_wild", e.g.:

df_samples = ag3.sample_metadata(sample_sets="v3_wild")
df_samples

Pandas can be used to explore and query the sample metadata in various ways. E.g., here is a summary of the numbers of samples by species:

df_samples.groupby("species").size()

Note that samples within a sample set may belong to different species. For convenience, we have made a species call for all samples in Ag1000G phase 3, using the genomic data. Calling species is not always straightforward, and we have used two different methods for species calling, ancestry informative markers (AIM) and principal components analysis (PCA). When loading the sample metadata, the AIM species calls are included by default. The results of these two different methods generally agree, although there are some populations where results are different, particularly in Guinea-Bissau, The Gambia, Kenya and Tanzania. If you have any questions about how to interpret these species calls, please get in touch.

## SNP sites and alleles

We have called SNP genotypes in all samples at all positions in the genome where the reference allele is not "N". Data on this set of genomic positions and alleles for a given chromosome arm (e.g., 3R) can be accessed as dask arrays as follows: 

pos, ref, alt = ag3.snp_sites("3R")
pos

ref

alt

Data can be loaded into memory as numpy arrays as shown in the following examples.

# read first 10 SNP positions into a numpy array
p = pos[:10].compute()
p

# read first 10 SNP reference alleles
r = ref[:10].compute()
r

# read first 10 SNP alternate alleles
a = alt[:10].compute()
a

Note that we have chosen to genotype all samples at all sites in the genome, assuming all possible SNP alleles. Not all of these alternate alleles will actually have been observed in the Ag3 samples. To determine which sites and alleles are segregating, an allele count can be performed over the samples you are interested in. See the example below. 

## Site filters

SNP calling is not always reliable, and we have created some site filters to allow excluding low quality SNPs. 

Because different species may have different genome accessibility issues, we have created three separate site filters:

* The "gamb_colu" filter is design for working only with *An. gambiae* and/or *An. coluzzii* samples. 
* The "arab" filter is designed for working with *An. arabiensis* samples. 
* The "gamb_colu_arab" filter is suitable for when analysing samples of any species together. 

Each set of site filters provides a "filter_pass" Boolean mask for each chromosome arm, where True indicates that the site passed the filter and is accessible to high quality SNP calling.

The site filters data can be accessed as dask arrays as shown in the examples below. 

# access gamb_colu_arab site filters for chromosome arm 3R as a dask array
filter_pass = ag3.site_filters("3R", mask="gamb_colu_arab")
filter_pass

# read filter values for first 10 SNPs (True means the site passes filters)
f = filter_pass[:10].compute()
f

## SNP genotypes

SNP genotypes for individual samples are available. Genotypes are stored as a three-dimensional array, where the first dimension corresponds to genomic positions, the second dimension is samples, and the third dimension is ploidy (2). Values coded as integers, where -1 represents a missing value, 0 represents the reference allele, and 1, 2, and 3 represent alternate alleles.

SNP genotypes can be accessed as dask arrays as shown below.

gt = ag3.snp_genotypes("3R", sample_sets="v3_wild")
gt

Note that the columns of this array (second dimension) match the rows in the sample metadata, if the same sample sets were loaded. I.e.:

seq_id = '3R'
df_samples = ag3.sample_metadata(sample_sets="v3_wild")
gt = ag3.snp_genotypes(seq_id=seq_id, sample_sets="v3_wild")
len(df_samples) == gt.shape[1]

You can use this correspondance to apply further subsetting operations to the genotypes by querying the sample metadata. E.g.:

import dask.array as da
loc_gambiae = df_samples.query("species == 'gambiae'").index.values
print(f"found {len(loc_gambiae)} gambiae samples")
gt_gambiae = da.take(gt, loc_gambiae, axis=1)
gt_gambiae

Data can be read into memory as numpy arrays, e.g., read genotypes for the first 5 SNPs and the first 3 samples:

g = gt[:5, :3, :].compute()
g

If you want to work with the genotype calls, you may find it convenient to use [scikit-allel](http://scikit-allel.readthedocs.org/). E.g., this code sets up a genotype array:

# use the scikit-allel wrapper class for genotype calls
import allel
gt = ag3.snp_genotypes("3R", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"])
gt = allel.GenotypeDaskArray(gt)
gt

Here's an example computation to count the number of segregating SNPs on chromosome arm 3R that also pass gamb_colu_arab site filters. This will take a little while, because it is scanning millions of genotype calls in hundreds of samples:

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