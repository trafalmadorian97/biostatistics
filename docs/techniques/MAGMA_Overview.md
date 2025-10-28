# MAGMA Concepts Overview
## MAGMA
The [MAGMA](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004219)  tool performs two main steps:
1. Gene analysis
2. Gene-set analysis


A key advantage of MAGMA is that it can operate on GWAS summary statistics combined with linkage disequilibrium data, and does not require raw GWAS data.
## Gene Analysis
 Let $Y$ be the phenotype of interest in  a GWAS.  Let $X_i$ be the ith SNP.


In a GWAS, we estimate the $\beta_i$ in

$$Y= \beta_i X_i +\epsilon_i.$$

where $\beta_i$ is the regression coefficient of $Y$ on $X_i$, and $\epsilon_i$ is the regression error.


Let $G$ be the set of SNPs associated with a gene of interest.  We wish to evaluate the strength of the evidence that $\beta_i\ne 0$ for some $i\in G$.  If this were so, it would suggest that the gene of interest is associated with the phenotype.


To evaluate this strength-of-evidence, [MAGMA uses as its test statistic](https://vu.data.surfsara.nl/s/VeuWKUwd0rz6AZD?dir=/&editing=false&openfile=true) $\sum_{j\in G}Z_j^2$, where $Z_j$ is the Z-statistic of the jth GWAS regression. 

This test statistics has a [generalized chi-squared distribution](https://en.wikipedia.org/wiki/Generalized_chi-squared_distribution).  The details of this distribution depend on the correlations between the individual $Z$-statistics, which in turn depends on the linkage disequilibrium structure of the SNPs under study.  This is why MAGMA requires linkage disequilibrium reference data.

MAGMA converts this test-statistic to a p-value via a[ numerical-integration procedure.](https://vu.data.surfsara.nl/s/VeuWKUwd0rz6AZD?dir=/&editing=false&openfile=true)

The resulting p-value offers a measure of the strength of the evidence that the gene of interest affects the phenotype.




## References
 [Generalized chi-squared distribution](https://en.wikipedia.org/wiki/Generalized_chi-squared_distribution)

[MAGMA Paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004219) 

[Note on Magma SNP-wise model](https://vu.data.surfsara.nl/s/VeuWKUwd0rz6AZD?dir=/&editing=false&openfile=true)


