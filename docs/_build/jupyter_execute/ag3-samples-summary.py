# Ag1000G phase 3 - summary of samples

This notebook provides a summary of which samples are available as part of the [Ag1000G phase 3 SNP data release](https://www.malariagen.net/data/ag1000g-phase3-snp).

This notebook assumes you have read either the [data download guide](@@TODO) or the [cloud access guide](@@TODO). This notebook reads data from the cloud, but to use locally downloaded data replace "gs://vo_agam_release" with the local file system path where data have been downloaded.

# install packages
!pip install -q --pre malariagen_data

# imports
import pandas as pd

# setup cloud access
import malariagen_data
ag3 = malariagen_data.Ag3("gs://vo_agam_release/")

# read in sample metadata for all sample sets containing wild-caught samples (excludes sample set AG1000G-X which contains lab crosses)
df_samples = ag3.sample_metadata(cohort="v3_wild")

# apply grouping
summ = df_samples.groupby(["sample_set", "country", "year", "species"]).size()
summ.name = "count"

# make pivot table
df_summary = pd.pivot_table(
    summ.reset_index(),
    values="count", 
    index=["sample_set", "country", "year"], 
    columns=["species"], fill_value=0)
df_summary