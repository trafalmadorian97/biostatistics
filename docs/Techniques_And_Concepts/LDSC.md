# Linkage Disequilibrium Score Regression
Linkage Disequilibrium Score Regression (LDSC) is a technique for estimating  [Heritability](Heritability.md) from GWAS summary statistics.  LDSC is ubiquitous, but its usefulness depends strongly on the validity certain modeling assumptions. To use LDSC correctly it is necessary to understand these assumptions.

## Model

LDSC assumes the following data generating equation:

$$
\phi = X\beta + \epsilon
$$

where:
- There are $M$ genotypes.  We assume that $M$ is large.
- There are $N$ individuals.  We assume that $N$ is large.
- $\phi\in\mathbb{R}^N$ is the vector of phenotypes
- $X\in\mathbb{R}^{N\times M}$ is the matrix of genotypes, standardized to have columns with sample mean 0 and sample variance 1.
- $\epsilon\in\mathbb{R}^N$ is the vector non-genetic effects.

Furthermore, we model all three of these objects as random variables with the following properties:

- $\mathrm{Var}(\epsilon)= (1-h^2)I$ where $h^2$ is the heritability of the phenotype
- $\mathrm{Var}(\beta)=\frac{h^2}{M}I$
- $\mathrm{E}(\epsilon)=0$
- $\mathrm{E}(\beta)=0$ 
- The rows of $X$ are independent and identically distributed.
- The distributions of columns of $X$ are "not too similar".
- The SNP $X_{i,j}$ may be highly correlated with a few other SNPs, but is uncorrelated with most SNPs.
- $\beta,\epsilon,X$ are all mutually independent.
1
- Each random matrix entry $X_{i,j}$ has mean zero.

Furthermore, define the following quantities related to Linkage Disequilibrium (LD).

- The LD between SNP $j$ and SNP $k$ is defined to be $r_{j,}:=\mathrm{E}X_{i,j}X_{i,k}$, (which does not depend on the individual $i$ by our assumption that the rows of $X$ are iid).
- The empirical LD between $j$ and $k$ is defined to be $\tilde{r}_{jk}:=\frac{1}{N}X_{:,j}^T X_{:,k}$.
- The LD score for a SNP $j$ is defined to be $l_j:= \sum_k r_{jk}^2$



## Derivation of Method
### Properties of $\hat{\beta}_i$ and $\chi^2_i$
We begin by computing the variance matrix of the genetic effects:


$$
\begin{align}
\mathrm{Var}(X\beta)&=\mathrm{E} X \beta \beta^T X^T\\
&=\frac{h^2}{M} \mathrm{E} X X^T & \text{Tower law of expectation}\\
&=h^2I & \text{By independence of rows, zero mean of $X_{i,j}$}
\end{align}
$$

We can also compute the variance matrix of the phenotypes:

$$
\begin{eqnarray}
\mathrm{Var}(\phi) &= \mathrm{Var}(X\beta) + \mathrm{Var}(\epsilon) & \text{ By independence}\\
&=h^2I + (1-h^2)I\\
&= I.
\end{eqnarray}
$$

As well as the expectation of the phenotypes:

$$
\begin{align}
\mathrm{E} (\phi) &= \mathrm{E}(X \beta) + \mathrm{E} (\epsilon)\\
&= 0 & \text{By tower law and $\mathrm{E}\beta =\mathrm{E} \epsilon=0$ }
\end{align}
$$


In a GWAS, it is typical to run a single-variant regression for each variant. For variant $i$, the regression coefficient resulting from this single-variant regression is $\hat{\beta}_i$, which is given by

$$
\begin{align}
\mathbb{R} \ni \hat{\beta}_i &= \frac{\frac{1}{N}(\phi-\overline{\phi})^T(X_{:,i} -\overline{X_{:,i}} )}{\frac{1}{N}  (X_{:,i} -\overline{X_{:,i}} )^T (X_{:,i} -\overline{X_{:,i}} ) }    & \text{ By OLS formula}\\
&= \frac{\frac{1}{N}(\phi-\overline{\phi})^TX_{:,i}  }{  \frac{1}{N}X_{:,i}^TX_{:,i}  } & \text{Since columns of $X$ are normalized}\\
&\approx \frac{\frac{1}{N}\phi^TX_{:,i}  }{\frac{1}{N}X_{:,i}^TX_{:,i}} & \text{Since $\mathrm{E}\phi=0$ and $N$ is large}\\
&=\frac{1}{N}\phi^TX_{:,i}  & \text{Since columns of $X$ are normalized}
\end{align}
$$

The squared regression errors of the $i$th GWAS regression are given by $\lVert\phi- \frac{1}{N}\phi^T X_{:,i} X_{:,i} \rVert^2$. We have assumed that $M$ is large, that columns of $X$ are not too similar, and that the components of $\beta$ are iid. Thus typically, GWAS regression $i$ will not explain any significant proportion of the variance of the phenotype.  So  


$$
\begin{align}
\lVert\phi- \frac{1}{N}\phi^T X_{:,i} X_{:,i} \rVert^2\approx 1. \label{residuals}
\end{align}
$$


The standard error of the $i$th GWAS regression coefficient is

$$
\begin{align}
\mathrm{SE}(\hat{\beta}_i) &\approx \sqrt{\frac{\lVert\phi- \frac{1}{N}\phi^T X_{:,i} X_{:,i} \rVert^2}{(X_{:,i} -\overline{X_{:,i}} )^T (X_{:,i} -\overline{X_{:,i}} )}} & \text{Formula for OLS SE}\\
&=\sqrt{\frac{1}{N}} & \text{\ref{residuals} + Normalization of $X$} \label{sebeta}
\end{align}
$$

By the definition of the [Wald Test Statistic](https://en.wikipedia.org/wiki/Wald_test) for the $i$th SNP, $\chi^2_i$, we have

$$
\begin{align}
\chi_i^2&= \frac{\hat{\beta_i}^2}{\mathrm{SE}(\hat{\beta_i})^2}\\
&\approx N \hat{\beta_i} & \text{by \ref{sebeta}} \label{wald}
\end{align}
$$

### Expectation of empirical LD scores
The expectation of the square of the empirical LD between SNPs $j$ and $k$ is:

$$
\begin{align}
\mathrm{E} \tilde{r}_{jk}^2&\\
&=\mathrm{E}\frac{1}{N^2}\sum_i \sum_h X_{i,j}X_{i,k}X_{h,j}X_{h,k}\\
&=\frac{1}{N^2}\mathrm{E}(\sum_{i\ne h} X_{i,j}X_{i,k}X_{h,j}X_{h,k} + \sum_i X_{i,j}^2X_{i,k}^2)\\
&=\frac{1}{N^2}( \sum_{i\ne h} \mathrm{E}(X_{i,j} X_{i,k })\mathrm{E} (X_{h,j X_{h,k}}) + \sum_i \mathrm{E} X_{i,j}^2 X_{i,k}^2) &\text{Independence of rows of $X$}\\
&= \frac{N-1}{N}r_{jk}^2 + \frac{1}{N}\mathrm{E}X_{1j}^2X_{1k}^2
\end{align}
$$


We write, $\mathrm{E}X_{1j}^2X_{1k}^2=1+2r_{jk}^2+\nu$ where we have used[ Isserlis's Theorem](https://en.wikipedia.org/wiki/Isserlis%27s_theorem) to compute the expectation of the product of the squares of two normal random variables, and then added error term $\nu$ to account for the non-normality of $X$.
 
Thus we have 
$$
\begin{align}
\mathrm{E} \tilde{r}_{jk}^2 &\\
&=r_{jk}^2 + \frac{1}{N}(1+r_{jk^2}^2+\nu)\\
&=r_{jk}^2+ \frac{1}{N}(2r_{jk}^2+\nu)+ \frac{1}{N}(1-r_{jk}^2)
\end{align}
$$

The expectation of the sum of the squares of the empirical LD scores with SNP j is given by

$$
\begin{align}
\mathrm{E} \sum_k \tilde{r}_{jk}^2&\\
&=\sum_{k}r^2_{jk} + \sum_{k}\frac{1}{N}(2r_{jk}^2+\nu) + \sum_k  \frac{1}{N}(1-r_{jk}^2)\\
&=l_j + \sum_{k}\frac{1}{N}(2r_{jk}^2+\nu) + \sum_k  \frac{1}{N}(1-r_{jk}^2) & \text{Definition of $l_j$}\\
\end{align}
$$

At this stage we introduce another approximation.  We have assumed that SNP $j$ has high correlation with only a small number of SNPs.  Thus the first $O(1/N)$ term can be expected to be significantly smaller than the second.  We therefor neglect this term, resulting in:

$$
\mathrm{E}\sum_k \tilde{r}_{jk}^2 \approx l_j + \frac{1}{N}(M-l_j)
$$

### The LDSC Equation

With the preliminaries out of the way, now compute the expectation of the chi squared statistic of the $j$th SNP

$$
\begin{align}
\mathrm{E} (\chi^2_j)&\\
&=N \mathrm{Var(\hat{\beta}_j)} & \text{by \ref{wald}}\\
&=N \mathrm{E} \mathrm{Var}(\hat{\beta}_j | X) & \text{Law of Total Variance}\\
&= N \mathrm{E} ( \frac{h^2}{m}\sum_k \tilde{r}^2_{jk} + \frac{1}{N}  (1-h^2) )\\
&= \frac{h^2}{M}(Nl_j + M-j_j) + 1 - h^2\\
&= \frac{h^2}{M}l_j(N-1)+1\\
&\approx \frac{h^2}{M}l_jN+1\\
\end{align}
$$

This is the main Linkage Disequilibrium Score Regression equation.

## Usage


## Critique of assumptions

## References

Main Reference:
Bulik-Sullivan, Brendan K., et al. "LD Score regression distinguishes confounding from polygenicity in genome-wide association studies." Nature genetics 47.3 (2015): 291-295.