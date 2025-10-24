Welcome to the ME/CFS biostatistics repo!
# Overall Project Goal
[ME/CFS](https://en.wikipedia.org/wiki/Myalgic_encephalomyelitis/chronic_fatigue_syndrome) is a common, poorly understood, and highly disabling disease.  This repository is intended to facilitate scientific progress in the understanding of ME/CFS by maintaining code implementing the statistical analysis of ME/CFS datasets. 

# Goals for code structure
We aim to implement analysis in a clean and modular way, such that:
- It should be possible to fully reproduce an existing analysis by checking out this repo and running a single Linux command.
- Modifying an analysis should usually involve tweaking only a few lines of Python code.
- When possible, analyses should make extensive use of cacheing so that heavy pipeline steps do not need to repeatedly be rerun.