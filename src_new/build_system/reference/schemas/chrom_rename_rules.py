CHROM_RENAME_RULES = {
    "chrX": 23,
    "chrY": 24,
    "chrM": 25,
} | {f"chr{i}": i for i in range(1, 25)}
