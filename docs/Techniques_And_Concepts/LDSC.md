# Linkage Disequilibrium Score Regression
Linkage Disequilibrium Score Regression (LDSC) is a technique for estimating  [Heritability](Heritability.md) from GWAS summary statistics.  LDSC is ubiquitous, but its usefulness depends strongly on the validity certain modeling assumptions. To use LDSC correctly it is necessary to understand these assumptions.

## Model

LDSC assumes the following data generating equation:

$$
\phi = X\beta + \epsilon
$$

where:
- There are $M$ genotypes.
- There are $N$ individuals.  
- $\phi\in\mathbb{R}^N$ is the vector of phenotypes
- $X\in\mathbb{R}^{N\times M}$ is the matrix of genotypes, standardized to have columns with sample mean 0 and sample variance 1.
- $\epsilon\in\mathbb{R}^N$ is the vector non-genetic effects 

Furthermore, we model all three of these objects as random variables with the following properties:

- $\mathrm{Var}(\epsilon)= (1-h^2)I$ where $h^2$ is the heritability of the phenotype
- $\mathrm{Var}(\beta)=\frac{h^2}{M}I$
- $\mathrm{E}(\epsilon)=0$
- $\mathrm{E}(\beta)=0$ 
- The rows of $X$ are independent.
- $\beta,\epsilon,X$ are all mutually independent.
1
- Each random matrix entry $X_{i,j}$ has mean zero.
## Immediate consequences of these assumptions
We can compute the variance matrix of the genetic effects:
$$
\begin{align}
\mathrm{Var}(X\beta)&=\mathrm{E} X \beta \beta^T X^T\\
&=\frac{h^2}{M} \mathrm{E} X X^T & \text{Tower law of expectation}\\
&=h^2I & \text{By independence of rows, zero mean of $X_{i,j}$}
\end{align}
$$
We can also compute the variance of the phenotypes
$$
\begin{align}
\mathrm{Var}(\phi) &= \mathrm{Var}(X\beta) + \mathrm{Var}(\epsilon) & \text{ By Independence}\\
&=h^2I + (1-h^2)I\\
&= I.
\end{align}
$$

## Critique of assumptions


## Derivation of method

- Work in progress

## References

Main Reference:
S