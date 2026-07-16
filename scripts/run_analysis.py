"""SurveilAMR: Comprehensive ATLAS dataset analysis pipeline."""
import json
import os
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "atlas_vivli_2004_2024.csv"
if not DATA_PATH.exists():
    DATA_PATH = ROOT / "atlas_vivli_2004_2024.csv"

OUT_DIR = ROOT / "outputs"
PROC_DIR = ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROC_DIR.mkdir(parents=True, exist_ok=True)

PRIORITY_SPECIES = [
    "Escherichia coli",
    "Klebsiella pneumoniae",
    "Pseudomonas aeruginosa",
    "Staphylococcus aureus",
    "Acinetobacter baumannii",
    "Enterococcus faecalis",
]

KEY_ABX = {
    "Escherichia coli": ["Meropenem", "Ceftriaxone", "Ciprofloxacin"],
    "Klebsiella pneumoniae": ["Meropenem", "Ceftriaxone", "Ciprofloxacin"],
    "Pseudomonas aeruginosa": ["Meropenem", "Ciprofloxacin", "Ceftazidime"],
    "Staphylococcus aureus": ["Oxacillin", "Vancomycin", "Ciprofloxacin"],
    "Acinetobacter baumannii": ["Meropenem", "Ciprofloxacin", "Colistin"],
    "Enterococcus faecalis": ["Vancomycin", "Ampicillin", "Linezolid"],
}

GENE_COLS = ["KPC", "NDM", "IMP", "VIM", "OXA", "CTX-M-1", "CTX-M-9", "SHV", "TEM"]

AFRICA_COUNTRIES = [
    "Ghana", "Nigeria", "Kenya", "South Africa", "Egypt", "Morocco", "Tunisia",
    "Algeria", "Ethiopia", "Uganda", "Tanzania", "Cameroon", "Senegal",
    "Ivory Coast", "Zimbabwe", "Zambia", "Mozambique", "Angola", "Libya",
    "Sudan", "Rwanda", "Mali", "Burkina Faso", "Benin", "Togo", "Gabon",
    "Congo", "Namibia", "Botswana", "Mauritius", "Madagascar",
]


def main():
    total_rows = 0
    species_counts = {}
    country_counts = {}
    year_counts = {}
    study_counts = {}
    resistance_by_year = {sp: {} for sp in PRIORITY_SPECIES}
    resistance_by_country = {sp: {} for sp in PRIORITY_SPECIES}
    resistance_by_abx_year = {}
    gene_counts = {g: 0 for g in GENE_COLS}
    gene_total = 0
    africa_rows = 0
    africa_species = {}
    africa_resistance = {sp: {"res": 0, "n": 0} for sp in PRIORITY_SPECIES}
    mdr_by_species = {
        sp: {"mdr": 0, "total": 0}
        for sp in ["Escherichia coli", "Klebsiella pneumoniae", "Acinetobacter baumannii"]
    }

    for chunk in pd.read_csv(DATA_PATH, chunksize=100_000, low_memory=False):
        total_rows += len(chunk)

        for s, c in chunk["Species"].value_counts().items():
            species_counts[s] = species_counts.get(s, 0) + c
        for s, c in chunk["Country"].value_counts().items():
            country_counts[s] = country_counts.get(s, 0) + c
        for y, c in chunk["Year"].value_counts().items():
            year_counts[y] = year_counts.get(y, 0) + c
        for s, c in chunk["Study"].value_counts().items():
            study_counts[s] = study_counts.get(s, 0) + c

        africa_chunk = chunk[chunk["Country"].isin(AFRICA_COUNTRIES)]
        africa_rows += len(africa_chunk)
        for s, c in africa_chunk["Species"].value_counts().items():
            africa_species[s] = africa_species.get(s, 0) + c

        for sp in PRIORITY_SPECIES:
            sub = chunk[chunk["Species"] == sp]
            primary_ab = KEY_ABX[sp][0]
            ic = primary_ab + "_I"
            if ic in sub.columns:
                for yr, grp in sub.groupby("Year"):
                    vals = grp[ic].dropna()
                    if len(vals) > 0:
                        resistance_by_year[sp].setdefault(yr, {"res": 0, "n": 0})
                        resistance_by_year[sp][yr]["res"] += (vals == "Resistant").sum()
                        resistance_by_year[sp][yr]["n"] += len(vals)
                for ct, grp in sub.groupby("Country"):
                    vals = grp[ic].dropna()
                    if len(vals) >= 20:
                        resistance_by_country[sp].setdefault(ct, {"res": 0, "n": 0})
                        resistance_by_country[sp][ct]["res"] += (vals == "Resistant").sum()
                        resistance_by_country[sp][ct]["n"] += len(vals)

            for ab in KEY_ABX[sp]:
                ic = ab + "_I"
                if ic not in sub.columns:
                    continue
                key = (sp, ab)
                resistance_by_abx_year.setdefault(key, {})
                for yr, grp in sub.groupby("Year"):
                    vals = grp[ic].dropna()
                    if len(vals) > 0:
                        resistance_by_abx_year[key].setdefault(yr, {"res": 0, "n": 0})
                        resistance_by_abx_year[key][yr]["res"] += (vals == "Resistant").sum()
                        resistance_by_abx_year[key][yr]["n"] += len(vals)

            afr_sub = africa_chunk[africa_chunk["Species"] == sp]
            primary_ic = KEY_ABX[sp][0] + "_I"
            if len(afr_sub) > 0 and primary_ic in afr_sub.columns:
                vals = afr_sub[primary_ic].dropna()
                africa_resistance[sp]["res"] += (vals == "Resistant").sum()
                africa_resistance[sp]["n"] += len(vals)

        for g in GENE_COLS:
            if g in chunk.columns:
                gene_counts[g] += chunk[g].notna().sum()
        gene_total += len(chunk)

        for sp in mdr_by_species:
            sub = chunk[chunk["Species"] == sp]
            if len(sub) == 0:
                continue
            res_cols = [a + "_I" for a in KEY_ABX[sp] if a + "_I" in sub.columns]
            if not res_cols:
                continue
            rc = sub[res_cols].apply(lambda row: sum(row == "Resistant"), axis=1)
            mdr_by_species[sp]["mdr"] += (rc >= 2).sum()
            mdr_by_species[sp]["total"] += len(sub)

    summary = {
        "total_rows": total_rows,
        "n_countries": len(country_counts),
        "n_species": len(species_counts),
        "year_range": [int(min(year_counts)), int(max(year_counts))],
        "studies": study_counts,
        "top_countries": dict(sorted(country_counts.items(), key=lambda x: -x[1])[:15]),
        "top_species": dict(sorted(species_counts.items(), key=lambda x: -x[1])[:15]),
        "africa_rows": africa_rows,
        "africa_countries_present": {
            c: country_counts[c] for c in AFRICA_COUNTRIES if country_counts.get(c, 0) > 0
        },
        "africa_top_species": dict(sorted(africa_species.items(), key=lambda x: -x[1])[:10]),
    }

    trends = {}
    for sp in PRIORITY_SPECIES:
        ab = KEY_ABX[sp][0]
        entry = {
            "antibiotic": ab,
            "yearly_resistance_pct": {
                int(yr): round(v["res"] / v["n"] * 100, 2)
                for yr, v in sorted(resistance_by_year[sp].items())
                if v["n"] >= 30
            },
            "top_resistant_countries": {
                c: {"pct": round(v["res"] / v["n"] * 100, 2), "n": v["n"]}
                for c, v in sorted(
                    resistance_by_country[sp].items(),
                    key=lambda x: -x[1]["res"] / x[1]["n"],
                )[:10]
                if v["n"] >= 50
            },
        }
        if africa_resistance[sp]["n"] > 0:
            entry["africa_resistance_pct"] = round(
                africa_resistance[sp]["res"] / africa_resistance[sp]["n"] * 100, 2
            )
            entry["africa_n"] = africa_resistance[sp]["n"]
        trends[sp] = entry

    summary["resistance_trends"] = trends
    summary["gene_detection_pct"] = {
        g: round(100 * gene_counts[g] / gene_total, 4) for g in GENE_COLS
    }
    summary["multidrug_resistance_proxy"] = {
        sp: round(v["mdr"] / v["total"] * 100, 2) for sp, v in mdr_by_species.items()
    }

    yearly_records = []
    for (sp, ab), yrs in resistance_by_abx_year.items():
        for yr, v in yrs.items():
            if v["n"] >= 20:
                yearly_records.append(
                    {
                        "Species": sp,
                        "Antibiotic": ab,
                        "Year": int(yr),
                        "Total_Isolates": v["n"],
                        "Resistant": v["res"],
                        "Resistance_Pct": round(v["res"] / v["n"] * 100, 2),
                    }
                )
    pd.DataFrame(yearly_records).to_csv(
        PROC_DIR / "surveilamr_resistance_by_year.csv", index=False
    )

    country_records = []
    for sp in PRIORITY_SPECIES:
        for ct, v in resistance_by_country[sp].items():
            if v["n"] >= 50:
                country_records.append(
                    {
                        "Species": sp,
                        "Country": ct,
                        "Antibiotic": KEY_ABX[sp][0],
                        "Total_Isolates": v["n"],
                        "Resistant": v["res"],
                        "Resistance_Pct": round(v["res"] / v["n"] * 100, 2),
                    }
                )
    pd.DataFrame(country_records).to_csv(
        PROC_DIR / "surveilamr_resistance_by_country.csv", index=False
    )

    with open(PROC_DIR / "dataset_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
