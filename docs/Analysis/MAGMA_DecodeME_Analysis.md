## MAGMA DecodeME Analysis
I applied [MAGMA](../Techniques/MAGMA_Overview.md) to [DecodeME](../Data_Sources/MECFS/DecodeME.md), partially reproducing analysis from the DecodeME preprint.  

## Gene Analysis

As an initial step, I applied MAGMA gene analysis under its default settings to the summary statistics from DECODE ME GWAS.  

In this step,
 

- Data from the 1000 genomes projects was used for a linkage disequilibrium reference.
- Data from the [SNP151 database](https://hgw2.soe.ucsc.edu/cgi-bin/hgTables?hgsid=2912494930_cRufLdpdc1ynRc2sCM3g1WGAWAgH&hgta_doSchemaDb=hg19&hgta_doSchemaTable=snp151Flagged
) was used to assign RSIDs to SNPs.
- Magma's default proximity based rules were used to assign SNPs to Genes.

The code corresponding to the gene analysis asset can be found [here](/src_new/assets/gwas/me_cfs/decode_me/processed_gwas_data/magma/decode_me_gwas_1_build_37_magma_ensembl_gene_analysis.py).


## GTEx data.