from pathlib import Path
import dask.array as da
import zarr
import pandas as pd
import allel


class Data:
    
    def __init__(self, path):
        if not isinstance(path, Path):
            path = Path(path).expanduser()
        self.path = path

    def load_mask(self, seq_id, mask, filters_analysis="dt_20200416"):
        """Load a site filter mask.

        Parameters
        ----------
        seq_id : str
            Chromosome arm.
        mask : {"gamb_colu", "arab", "gamb_colu_arab"}
            Mask species combination.
        filters_analysis : str
            Filtering model.

        Returns
        -------
        filter_pass: numpy array
            Boolean array where True means pass.

        """ 

        store_path = self.path / f"site_filters/{filters_analysis}/{mask}"
        callset_filters = zarr.open(str(store_path), mode="r")
        filter_pass = callset_filters[seq_id]["variants/filter_pass"][:]

        return filter_pass
    
    def load_variants_array(self, seq_id, field, mask=None, filters_analysis="dt_20200416"):
        """Load sites data.

        Parameters
        ----------
        seq_id : str
            Chromosome arm.
        field : {"REF", "ALT", "POS"}
            Array to load.
        mask : {"gamb_colu", "arab", "gamb_colu_arab"}
            Mask species combination.
        filters_analysis : str
            Filtering model.

        Returns
        -------
        arr : numpy array

        """

        store_path = self.path / "snp_genotypes/all/sites"
        callset_sites = zarr.open(str(store_path), mode='r')
        arr = da.from_array(callset_sites[seq_id]["variants"][field])

        if mask is not None:
            filter_pass = self.load_mask(seq_id, mask, filters_analysis)
            arr = da.compress(filter_pass, arr, axis=0)

        return arr.compute()

    def load_calldata_array(self, seq_id, sample_set, field, mask=None, filters_analysis="dt_20200416", wrap=True):
        """Load SNP genotype calldata for a given sample set.

        Parameters
        ----------
        seq_id : str
            Chromosome arm.
        sample_set : str or list of str
            Sample set(s) to load. If multiple sample sets are given, data will be concatenated.
        field : {"GT", "GQ", "AD", "MQ"}
            Array to load.
        mask : {"gamb_colu", "arab", "gamb_colu_arab"}
            Mask species combination.
        filters_analysis : str
            Filtering model.
        wrap : bool
            If True, wrap with scikit-allel class.

        Returns
        -------
        arr : dask.Array

        """

        if isinstance(sample_set, str):
            # load data for a single sample set
            store_path = self.path / f"snp_genotypes/all/{sample_set}"
            callset_genotypes = zarr.open(str(store_path), mode='r')
            arr = da.from_array(callset_genotypes[f"{seq_id}/calldata/{field}"])

        elif isinstance(sample_set, (list, tuple)):
            # load data for multiple sample sets
            arr = da.concatenate(
                [self.load_calldata_array(
                    seq_id=seq_id, 
                    sample_set=x, 
                    field=field, 
                    mask=None,
                    wrap=False) for x in sample_set], 
                axis=1)

        else:
            raise TypeError("Type of `sample_set` must be string or list of strings")

        if mask is not None:

            filter_pass = self.load_mask(seq_id, mask, filters_analysis)
            arr = da.compress(filter_pass, arr, axis=0)

        if field == "GT" and wrap:
            arr = allel.GenotypeDaskArray(arr)

        return arr

    def load_sample_metadata(self,
                             sample_set, 
                             include_aim_species_calls=True, 
                             include_pca_species_calls=False, 
                             species_analysis="species_calls_20200422"):
        """Load sample metadata, optionally including species calls.

        Parameters
        ----------
        sample_set : str
            Sample set.
        include_aim_species_calls : bool
            If True, include AIM calls.
        include_pca_species_calls : bool
            If True, include PCA calls.
        species_analysis : str
            Species analysis.

        Returns
        -------
        df : pandas.DataFrame

        Notes
        -----
        If both AIMs and PCA are requested, species calls columns are appended with 
        "_aim" and "_pca" respectively.

        """

        if isinstance(sample_set, str):

            df = pd.read_csv(self.path / f"metadata/general/{sample_set}/samples.meta.csv")
            df["sample_set"] = sample_set

            if include_aim_species_calls:
                df_aim = pd.read_csv(self.path / f"metadata/species_calls_20200422/{sample_set}/samples.species_aim.csv")

            if include_pca_species_calls:
                df_pca = pd.read_csv(self.path / f"metadata/species_calls_20200422/{sample_set}/samples.species_pca.csv")

            df_species = None

            if include_aim_species_calls and include_pca_species_calls:
                df_species = df_aim.merge(df_pca, on="sample_id", lsuffix="_aim", rsuffix="_pca", sort=False)

            elif include_aim_species_calls:
                df_species = df_aim

            elif include_pca_species_calls:
                df_species = df_pca

            if df_species is not None:
                df = df.merge(df_species, on="sample_id", sort=False)

            return df

        elif isinstance(sample_set, (list, tuple)):

            return pd.concat(
                [self.load_sample_metadata(
                    sample_set=sample_set, 
                    include_aim_species_calls=include_aim_species_calls, 
                    include_pca_species_calls=include_pca_species_calls, 
                    species_analysis=species_analysis) 
                 for sample_set in sample_set],
                axis=0, sort=False).reset_index(drop=True)

        else:
            raise TypeError("Type of `sample_set` must be string or list of strings")
