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
- The rows of $X$ are independent.
- The distributions of columns of $X$ are "not too similar".
- $\beta,\epsilon,X$ are all mutually independent.
1
- Each random matrix entry $X_{i,j}$ has mean zero.
## Immediate consequences of these assumptions
- We can compute the variance matrix of the genetic effects:
$$
\begin{align}
\mathrm{Var}(X\beta)&=\mathrm{E} X \beta \beta^T X^T\\
&=\frac{h^2}{M} \mathrm{E} X X^T & \text{Tower law of expectation}\\
&=h^2I & \text{By independence of rows, zero mean of $X_{i,j}$}
\end{align}
$$
- We can also compute the variance matrix of the phenotypes:
$$
\begin{align}
\mathrm{Var}(\phi) &= \mathrm{Var}(X\beta) + \mathrm{Var}(\epsilon) & \text{ By Independence}\\
&=h^2I + (1-h^2)I\\
&= I.
\end{align}
$$
- As well as the expectation of the phenotypes:

$$
\begin{align}
\mathrm{E} (\phi) &= \mathrm{E}(X \beta) + \mathrm{E} (\epsilon)\\
&= 0 & \text{By tower law and $\mathrm{E}\beta =\mathrm{E} \epsilon=0$ }
\end{align}
$$

- In a GWAS, it is typical to run a single-variant regression for each variant. For variant $i$, the regression coefficient resulting from this single-variant regression is

$$
\begin{align}
\mathbb{R} \ni \hat{\beta}_i &= \frac{\frac{1}{N}(\phi-\overline{\phi})^T(X_{:,i} -\overline{X_{:,i}} )}{\frac{1}{N}  (X_{:,i} -\overline{X_{:,i}} )^T (X_{:,i} -\overline{X_{:,i}} ) }    & \text{ By OLS formula}\\
&= \frac{\frac{1}{N}(\phi-\overline{\phi})^TX_{:,i}  }{  \frac{1}{N}X_{:,i}^TX_{:,i}  } & \text{Since columns of $X$ are normalized}\\
&\approx \frac{\frac{1}{N}\phi^TX_{:,i}  }{\frac{1}{N}X_{:,i}^TX_{:,i}} & \text{Since $\mathrm{E}\phi=0$ and $N$ is large}\\
&=\frac{1}{N}\phi^TX_{:,i}  & \text{Since columns of $X$ are normalized}
\end{align}
$$

- The squared regression errors of the $i$th GWAS regression are given by $\lVert\phi- \frac{1}{N}\phi^T X_{:,i} X_{:,i} \rVert^2$. We have assumed that $M$ is large, that columns of $X$ are not too similar, and that the components of $\beta$ are iid. Thus typically, GWAS regression $i$ will not explain any significant proportion of the variance of the phenotype.  So  $\lVert\phi- \frac{1}{N}\phi^T X_{:,i} X_{:,i} \rVert^2\approx 1$.
- The standard error of the $i$th GWAS regression coefficient is

$$
\begin{align}
\mathrm{SE}(\hat{\beta}_i) &\approx \sqrt{\frac{\lVert\phi- \frac{1}{N}\phi^T X_{:,i} X_{:,i} \rVert^2}{(X_{:,i} -\overline{X_{:,i}} )^T (X_{:,i} -\overline{X_{:,i}} )}} & \text{Formula for OLS SE}\\
&=\sqrt{\frac{1}{N}} & \text{Above + Normalization of $X$}
\end{align}
$$

- By the definition of the [Wald Test Statistic](https://en.wikipedia.org/wiki/Wald_test) we have

$$
\begin{align}
\chi^2&= \frac{\hat{\beta_i}^2}{\mathrm{SE}(\hat{\beta_i})^2}\\
&\approx N \hat{\beta_i} & \text{by above}
\end{align}
$$



## Derivation of method

- Work in progress


## Critique of assumptions

## References

Main Reference:
S