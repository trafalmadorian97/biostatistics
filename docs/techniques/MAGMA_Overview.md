# MAGMA Overview
## The Initial Gene-specific model
[MAGMA](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004219) starts with the following gene-specific model:

$$
Y=X\beta + \epsilon 
$$
where:
- $Y$, taking values in $\mathbb{R}^{N}$ is the random vector of observed phenotypes for all $N$ participants in a GWAS study.
- $X\in\mathbb{R}^{N\times m}$ is the matrix of genotypes for all $m$ SNPs associated with a specific gene of interest. $X_{i,j}$ is the number of copies of SNP $j$ in individual $i$.  (Remember that we are not considering all SNPs here, just SNPS associated with the gene of interest)
- $\beta\in\mathbb{R}^m$ is the vector of true regression coefficients for the joint-regression of $Y$ on the $m$ gene-associated SNPs.
- $\epsilon \sim N(0, \sigma I)$ is the random vector of error.


Note also that in the above, only $Y$ and $\epsilon$ are random.  $X$ and $\beta$ are viewed as fixed.

Ideally, we would like to compute a test statistic for a statistical test with null hypothesis that $\beta=0$. The magnitude of this test statistic would quantify the strength of the evidence for the gene of interest affecting the phenotype.


A  natural test to choose would be the [score test](https://en.wikipedia.org/wiki/Score_test).  

The test statistic for the score test in this case is 

$$
\frac{1}{\sigma^2}Y^TX(X^TX)^{-1}X^TY
$$

Unfortunately, we cannot direclty compute this test statistic, since 