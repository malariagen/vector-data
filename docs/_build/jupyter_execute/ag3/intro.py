# Introduction to Ag1000G phase 3 (Ag3)

The [*Anopheles gambiae* 1000 Genomes Project (Ag1000G)](https://www.malariagen.net/ag1000g) is a collaborative project using whole-genome sequencing to study genetic variation and evolution in natural populations of mosquitoes in the *Anopheles gambiae* species complex. 

This page provides an introduction to open data resources released as part of the third phase of the Ag1000G project, known as "Ag3" for short. We hope the data from Ag3 will be a valuable resource for research and surveillance of malaria vectors. If you have any questions about this guide or how to use the data, please [start a new discussion](https://github.com/malariagen/vector-public-data/discussions/new) on the malariagen/vector-open-data repo on GitHub. If you find any bugs, please [raise an issue](https://github.com/malariagen/vector-public-data/issues/new/choose).


## Terms of use

Data from Ag3 are released openly and can be downloaded and analysed for any purpose. The data have been released prior to publication by the Ag1000G Consortium, and are currently subject to a publication embargo described further in the [Ag1000G terms of use](https://www.malariagen.net/data/terms-use/ag1000g-terms-use). If you have any questions about the terms of use, please email data@malariagen.net.


## Contributing studies

The Ag1000G project is coordinated by a consortium of partners from a range
of different research institutions and countries. This includes consortium members
who are carrying out independent research studies in malaria-endemic regions, and
who have contributed mosquito specimens or mosquito DNA samples collected in
the course of their own research. In total, 26 studies contributed samples to Ag3, including wild-caught specimens from 19 countries. 


For further information about these contributing studies, the researchers involved, and the collection sites and methods, please see the [contributing studies document](https://storage.googleapis.com/vo_agam_release/v3/ag1000g-phase3-contributing-studies.pdf). 


## Population sampling

Ag3 includes data from 3,081 individual mosquitoes, including 2,784 mosquitoes collected from natural populations in 19 countries. Three species are represented within the cohort: *Anopheles gambiae*, *Anopheles coluzzii* and *Anopheles arabiensis*. The map below provides an overview of the collection locations and the numbers of samples broken down by species. 

```{image} ../images/ag3-map.png
:alt: Ag3 map of sampling sites
:class: bg-primary
:width: 700px
:align: center
```

In addition to these wild-caught samples, a further 297 samples are included from 15 lab crosses.


## Whole-genome sequencing and variant calling

All samples in Ag3 have been sequenced individually to high coverage using Illumina technology at the Wellcome Sanger Institute. These sequence data have then been analysed to identify genetic variants such as single nucleotide polymorphisms (SNPs). After variant calling, both the samples and the variants have been through a range of quality control analyses, to ensure the data are of high quality. Both the raw sequence data and the curated variant calls are openly available for download and analysis. 


For further information about the sequencing and variant calling methods used, please see the [SNP calling methods document](https://storage.googleapis.com/vo_agam_release/v3/ag1000g-phase3-snp-calling-methods.pdf).


## Data hosting

Data from Ag3 are hosted by several different services. 

Raw sequence reads, sequence read alignments and SNP calls are available for download from the European Nucleotide Archive (ENA). Further information on how to find and download these data is provided in the [data download guide](download).

The SNP data have also been uploaded to Google Cloud, and can be analysed directly within the cloud without having to download or copy any data, including via free interactive computing services such as [MyBinder](https://gke.mybinder.org/) and [Google Colab](https://colab.research.google.com/). Further information about analysing these data in the cloud is provided in the [cloud data access guide](cloud).


## Sample sets

The samples included in Ag3 have been organised into 26 sample sets. Each of these sample sets corresponds to a set of mosquito specimens from a contributing study. Depending on your objectives, you may want to access data from only specific sample sets, or all sample sets. Here is a list of the sample sets included in Ag3:

import malariagen_data
ag3 = malariagen_data.Ag3("gs://vo_agam_release/")
df_sample_sets = ag3.sample_sets()
df_sample_sets

The sample set identifiers all start with "AG1000G-" followed by the two-letter code of the country from which samples were collected (e.g., "AO" is Angola). Where there are multiple sample sets from the same country, these have been given alphabetical suffixes, e.g., "AG1000G-BF-A", "AG1000G-BF-B" and "AG1000G-BF-C" are three sample sets from Burkina Faso.

These country code suffixes are just a convenience to help remember which sample sets contain which data, please see the sample metadata for more precise location information. Note also that sample set AG1000G-GN-B contains samples from both Guinea and Mali.

Here is a more detailed breakdown of the samples contained within each sample set, summarised by country, year of collection, and species:

df_samples = ag3.sample_metadata()
df_summary = df_samples.pivot_table(
    index=["sample_set", "country", "year"], 
    columns=["species"],
    values="sample_id", 
    aggfunc=len,
    fill_value=0)
df_summary

Note that there are also multiple sampling sites represented within some sample sets.

## Further reading

Hopefully this page has provided a useful introduction to the Ag3 data resource. If you would like to start working with these data, please visit the [cloud data access guide](snp-cloud) or the [data download guide](snp-download) or continue browsing the other documentation on this site.

If you have any questions about the data and how to use them, please do get in touch by [starting a new discussion](https://github.com/malariagen/vector-public-data/discussions/new) on the malariagen/vector-open-data repo on GitHub.