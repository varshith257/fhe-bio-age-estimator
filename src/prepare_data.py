import pandas as pd
import gzip
import re

# === 1. Extract GEO and Beta Matrix Sample IDs ===
geo_ids = []
beta_ids = []
characteristics_lines = []

with gzip.open("GSE40279_series_matrix.txt.gz", "rt") as f:
    for line in f:
        if line.startswith("!Sample_geo_accession"):
            geo_ids = [x.replace('"', '') for x in line.strip().split("\t")[1:]]
        if line.startswith("!Sample_title"):
            beta_ids = [x.replace('"', '') for x in line.strip().split("\t")[1:]]
        if line.startswith("!Sample_characteristics_ch1"):
            characteristics_lines.append(line.strip().split("\t")[1:])

print("\nFirst 5 GEO IDs:", geo_ids[:5])
print("First 5 beta matrix IDs:", beta_ids[:5])

# === 2. Build mapping DataFrame and extract short Beta IDs ===
id_map = pd.DataFrame({"Sample_ID": geo_ids, "Beta_ID": beta_ids})
# Extract numeric code from Beta_ID and prepend 'X' to match beta matrix index
id_map['Beta_ID_short'] = id_map['Beta_ID'].str.extract(r'(\d+)$')[0].apply(lambda x: f'X{x}')

# === 3. Extract Age for Each Sample ===
characteristics_per_sample = list(zip(*characteristics_lines))
ages = []
for char_list in characteristics_per_sample:
    age_val = None
    for s in char_list:
        s_lower = s.lower()
        match = re.search(r'age.*?:\s*"?(\d+)', s_lower)
        if match:
            try:
                age_val = int(match.group(1))
            except Exception:
                age_val = None
            break
    ages.append(age_val)

sample_key = pd.DataFrame({"Sample_ID": geo_ids, "Age": ages})
sample_key = sample_key.merge(id_map, on="Sample_ID")
print("\nSample key columns:", sample_key.columns.tolist())
print(sample_key.head())
print("Missing values in sample_key:\n", sample_key.isnull().sum())

# === 4. Extract Beta Values for Top CpGs ===
beta = pd.read_csv("GSE40279_average_beta.txt.gz", sep="\t", index_col=0)

selected_cpgs = [
    "cg16867657",  # ELOVL2
    "cg14361627",  # KLF14
    "cg07553761",  # TRIM59
    "cg24079702",  # FHL2
    "cg19283806"   # CCDC102B
]

# Check if CpGs are in index (rows) instead of columns
if any(cpg in beta.index for cpg in selected_cpgs):
    print("Transposing beta matrix...")
    beta = beta.transpose()
    print("After transpose, columns:", list(beta.columns[:20]))
    print("After transpose, index:", list(beta.index[:20]))

selected_cpgs = [cpg for cpg in selected_cpgs if cpg in beta.columns]
print("\nSelected CpGs present in beta matrix:", selected_cpgs)

beta_subset = beta[selected_cpgs].copy()
beta_subset["Beta_ID_short"] = beta_subset.index

print("\nBeta subset columns:", beta_subset.columns.tolist())
print(beta_subset.head())
print("Missing values in beta_subset:\n", beta_subset.isnull().sum())

# === 5. Merge Beta Values with Ages using Beta_ID_short ===
df = beta_subset.merge(sample_key, on="Beta_ID_short").drop(["Sample_ID", "Beta_ID", "Beta_ID_short"], axis=1)
print("\nMerged data columns:", df.columns.tolist())
print(df.head())
print("Missing values in merged data:\n", df.isnull().sum())

# === 6. Save Final Demo Dataset ===
df.to_csv("bio_age_demo_data.csv", index=False)
print(f"\nSaved bio_age_demo_data.csv with shape: {df.shape}")
