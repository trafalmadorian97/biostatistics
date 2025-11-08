# MAGMA
## MAGMA Overview
[MAGMA](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004219) is a tool for the analysis of GWAS results. MAGMA can operate on GWAS summary statistics and does not require raw GWAS data.


[MAGMA](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004219) performs two main steps:

1. Gene analysis,
2. Gene-set analysis.


## Gene Analysis
### Purpose
GWAS summary statistics consist of SNP-level regression coefficients and standard errors. The purpose of the MAGMA gene-analysis step is to convert these SNP-level statistics to gene-level statistics, so we can judge which genes are likely to affect the phenotype.

### Requirements
Gene analysis requires:

1.  GWAS summary statistics,
2. A rule associating SNPs with genes (often just proximity),
3. Data describing the [linkage disequilibrium](https://en.wikipedia.org/wiki/Linkage_disequilibrium) structure of the SNPs studied by the GWAS.

### Mathematical Overview


 Let $Y$ be the phenotype of interest in a GWAS.  Let $X_i$ be the ith SNP.


In a GWAS, we estimate

$$
Y= \beta_i X_i +\epsilon_i,
$$

for all $i$, where $\beta_i$ is the regression coefficient of $Y$ on $X_i$, and $\epsilon_i$ is the regression error. 


Let $G$ be the set of SNPs associated with a gene of interest.  We wish to measure the strength of the evidence that $\beta_i\ne 0$ for some $i\in G$. That is, we wish to judge how likely it is that the gene affects the phenotype.


To evaluate the evidence, [MAGMA uses as its test statistic](https://vu.data.surfsara.nl/s/VeuWKUwd0rz6AZD?dir=/&editing=false&openfile=true) $\sum_{i\in G}Z_i^2$, where $Z_i$ is the Z-statistic of the ith GWAS regression. 

This test statistic has a [generalized chi-squared distribution](https://en.wikipedia.org/wiki/Generalized_chi-squared_distribution) under the null hypothesis.  The details of its distribution depend on the correlations between the individual $Z$-statistics, which in turn depends on the linkage disequilibrium structure of the SNPs under study.  This is why MAGMA gene analysis requires linkage disequilibrium reference data.

MAGMA converts the test-statistic to a p-value via a[ numerical-integration procedure](https://vu.data.surfsara.nl/s/VeuWKUwd0rz6AZD?dir=/&editing=false&openfile=true). A small p value indicates strong evidence that the gene affects the phenotype.




## References

[//]: # ( [Generalized chi-squared distribution]&#40;https://en.wikipedia.org/wiki/Generalized_chi-squared_distribution&#41;)

[MAGMA Paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004219) 

[Note on Magma SNP-wise model](https://vu.data.surfsara.nl/s/VeuWKUwd0rz6AZD?dir=/&editing=false&openfile=true)


