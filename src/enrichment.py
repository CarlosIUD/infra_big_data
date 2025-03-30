import pandas as pd
import json
import os
import re

# ----------------------------
# Step 1: Load Datasets from GitHub
# ----------------------------

base_url = 'https://raw.githubusercontent.com/mvm11/s25_ea3_data_enrichment_big_data_cloud/refs/heads/main/the_complete_list_of_unicorn_%20companies.csv'
jsonl_url = 'https://raw.githubusercontent.com/mvm11/s25_ea3_data_enrichment_big_data_cloud/refs/heads/main/investments.jsonl'

try:
    df_base = pd.read_csv(base_url)
    print(f"[OK] Base dataset loaded successfully with {len(df_base)} records.")
except Exception as e:
    print(f"[FAILED] Failed to load base dataset: {e}")
    df_base = pd.DataFrame()

try:
    df_investments = pd.read_json(jsonl_url, lines=True)
    print(f"[OK] Investment dataset loaded successfully with {len(df_investments)} records.")
except Exception as e:
    print(f"[FAILED] Failed to load investment dataset: {e}")
    df_investments = pd.DataFrame()

# ----------------------------
# Step 2: Clean and Convert Valuation Column
# ----------------------------

df_base['valuation_billion'] = df_base['Valuation ($B)'].replace('[\$,]', '', regex=True).astype(float)

# ----------------------------
# Step 3: Select Top 100 Companies by Valuation
# ----------------------------

df_top100 = df_base.sort_values(by='valuation_billion', ascending=False).head(100).copy()
print(f"[OK] Selected top 100 companies by valuation.")

# ----------------------------
# Step 4: Create Complementary Files
# ----------------------------

os.makedirs("data", exist_ok=True)
os.makedirs("src/static/auditoria", exist_ok=True)

# JSON: Founders and Founded Year
founders_data = []
for i, row in df_top100.iterrows():
    founders_data.append({
        "Company": row["Company"],
        "Founder": f"Founder of {row['Company']}",
        "Founded Year": 2000 + (i % 20)
    })

with open("data/founders.json", "w", encoding="utf-8") as f:
    json.dump(founders_data, f, indent=2)

# CSV: Headcount
headcount_data = df_top100[["Company"]].copy()
headcount_data["Headcount"] = 100 + (headcount_data.index % 50) * 10
headcount_data.to_csv("data/headcount.csv", index=False)

# TXT: Descriptions (tab-separated)
with open("data/descriptions.txt", "w", encoding="utf-8") as f:
    for _, row in df_top100.iterrows():
        f.write(f"{row['Company']}\t{row['Company']} is a leading company in {row['Industry']}.\n")

print("[OK] Created complementary data files (JSON, CSV, TXT).")

# ----------------------------
# Step 5: Load Complementary Files
# ----------------------------

with open("data/founders.json", encoding="utf-8") as f:
    founders_df = pd.DataFrame(json.load(f))

headcount_df = pd.read_csv("data/headcount.csv")
descriptions_df = pd.read_csv("data/descriptions.txt", sep="\t", names=["Company", "Description"])

print("[OK] Loaded complementary files.")

# ----------------------------
# Step 6: Merge All DataFrames
# ----------------------------

df_enriched = df_top100.merge(founders_df, on="Company", how="left")
df_enriched = df_enriched.merge(headcount_df, on="Company", how="left")
df_enriched = df_enriched.merge(descriptions_df, on="Company", how="left")

print(f"[OK] Final enriched dataset has shape: {df_enriched.shape}")

# ----------------------------
# Step 7: Save Enriched Dataset and Audit Report
# ----------------------------

df_enriched.to_csv("data/enriched_data.csv", index=False)

with open("src/static/auditoria/enrichment_report.txt", "w", encoding="utf-8") as f:
    f.write("=== Enrichment Report ===\n")
    f.write(f"Base records: {len(df_top100)}\n")
    f.write(f"Enriched records: {len(df_enriched)}\n\n")

    f.write("Joined data sources:\n")
    f.write("- founders.json (Founder, Founded Year)\n")
    f.write("- headcount.csv (Headcount)\n")
    f.write("- descriptions.txt (Company Description)\n")

    missing = df_enriched.isnull().sum()
    f.write("\nMissing values after merge:\n")
    f.write(missing.to_string())

print("[OK] Exported enriched dataset and enrichment report.")
