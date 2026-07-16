# SurveilAMR: Vivli AMR 2026 Data Challenge

**Surveillance Intelligence for Antimicrobial Resistance Trends**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Data Challenge](https://img.shields.io/badge/Vivli-AMR-2026%20Challenge-blue)](https://amr.vivli.org)

**Data Request ID:** 00013370  
**Data Request DOI:** [https://doi.org/10.25934/PR00013370](https://doi.org/10.25934/PR00013370)  
**Repository:** [https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR](https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR)

---

## Overview / Abstract

SurveilAMR is an open analytics pipeline for the **2026 Vivli AMR Surveillance Data Challenge**. It transforms structured bacterial, mycobacterial, and novel-agent surveillance data from the Vivli AMR Register into actionable intelligence for clinicians, antimicrobial stewardship programs, and public health authorities—particularly in low- and middle-income settings such as Ghana.

We analyzed four approved datasets: Pfizer **ATLAS Antibiotics** (1,011,168 isolates; 83 countries; 2004–2024), Paratek **KEYSTONE** omadacycline surveillance (96,302 isolates; 2015–2025), Johnson & Johnson **DREAM** MDR-TB (5,928 isolates; 2011–2019), and Venus Remedies **GASAR Study III** (496 isolates; India; 2022–2023). Key findings include a ~5-fold rise in *K. pneumoniae* meropenem resistance (4.2% → 20.7%, 2007–2024), elevated African *A. baumannii* carbapenem resistance (75.9%), retained omadacycline potency against *S. aureus* (MIC90 0.25 µg/mL), low overall bedaquiline MICs in DREAM (median 0.03 µg/mL), and frequent NDM/VIM co-carriage in GASAR.

> **Note:** Raw industry surveillance datasets cannot be publicly shared due to Vivli data access agreements. Place approved raw files in `data/raw/` after obtaining access from [https://amr.vivli.org](https://amr.vivli.org). Processed summary tables and figures are included in this repository.

## Research Team

| Role | Name | Affiliation | Email |
|------|------|-------------|-------|
| Lead Researcher | Nana Safo Duker | GeneHus, Ghana | freshsafoduker3@gmail.com |
| Team Member | Dr. Agnes Achiamaa Anane | Ghana Health Service | agnes.anane@ghs.gov.gh |
| Team Member | Dr. Marwin Afari | Ghana Health Service | marwinafari@yahoo.com |

## Datasets

| Dataset | Contributor | Role in SurveilAMR |
|---------|-------------|--------------------|
| ATLAS_Antibiotics | Pfizer Inc. | Primary spatiotemporal bacterial AMR trends |
| KEYSTONE | Paratek Pharmaceuticals, Inc. | Omadacycline/comparator MIC surveillance |
| Bedaquiline DREAM | Johnson & Johnson | MDR-TB bedaquiline MIC and subtype patterns |
| GASAR (Study III) | Venus Remedies Limited | Gram-negative mechanisms and polymyxin MICs |

## Objectives

1. **Country and regional AMR trends** — Quantify resistance trajectories across 83 countries (2004–2024)
2. **Pathogen-specific surveillance** — Characterize ESKAPE pathogens and priority Gram-negatives
3. **Resistance mechanism profiling** — Map beta-lactamase gene detection and GASAR gene/phenotype combinations
4. **Temporal early-warning signals** — Detect rising carbapenem and cephalosporin resistance for stewardship alerts
5. **Cross-dataset decision support** — Integrate ATLAS, KEYSTONE, DREAM, and GASAR for LMIC stewardship use

## Repository Structure

```
SurveilAMR/
├── data/
│   ├── raw/                         # Vivli-approved raw data (not in repo)
│   └── processed/                   # Aggregated resistance summaries (included)
├── docs/
│   ├── SurveilAMR_Report.md         # Challenge submission report
│   ├── SurveilAMR_Report.pdf
│   ├── SurveilAMR_Report.docx
│   └── Research Data Request_*.md
├── notebooks/
│   └── 01_eda_surveilamr.ipynb
├── outputs/
│   └── figures/                     # Publication figures
├── scripts/
│   ├── run_analysis.py              # ATLAS analysis pipeline
│   ├── analyze_supplementary.py     # KEYSTONE / DREAM / GASAR
│   ├── generate_figures.py          # ATLAS figures
│   ├── eda_surveilamr.py            # Exploratory analysis
│   └── export_report.py             # MD → DOCX/PDF export
├── requirements.txt
├── LICENSE
└── README.md
```

## Quick Start

```bash
git clone https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR.git
cd Vivli-AMR-2026-Data-Challenge-SurveilAMR
pip install -r requirements.txt
```

After Vivli approval, place raw files:

```
data/raw/atlas_vivli_2004_2024.csv
data/raw/Omadacycline_2015 to 2025_Surveillance_data.xlsx
data/raw/BEDAQUILINE DREAM DATASET FOR VIVLI - 06-06-2022.xlsx
data/raw/GASAR Study III (n=494)_updated.xlsx
```

Run the full pipeline:

```bash
python scripts/run_analysis.py
python scripts/analyze_supplementary.py
python scripts/generate_figures.py
python scripts/eda_surveilamr.py
python scripts/export_report.py
```

Interactive exploration:

```bash
jupyter notebook notebooks/01_eda_surveilamr.ipynb
```

## Methodology

### Data preprocessing
- Standardized susceptibility labels (Susceptible, Intermediate, Resistant)
- Parsed MIC inequality strings for DREAM and KEYSTONE
- Minimum isolate thresholds (n ≥ 20 / n ≥ 50) for stable ATLAS resistance estimates
- Normalized DREAM TB subtypes and GASAR phenotype buckets

### Analytical modules
1. Chunked exploratory data analysis over ATLAS (~387 MB)
2. Year-over-year resistance rates for priority antibiotic–pathogen pairs
3. Country-level heatmaps and African regional stratification
4. Beta-lactamase gene prevalence and MDR proxy scoring
5. KEYSTONE omadacycline MIC50/90 by pathogen and year
6. DREAM bedaquiline MIC by continent/year/subtype
7. GASAR phenotype and gene-combination profiles

## Key Findings

| Metric | Value |
|--------|-------|
| ATLAS isolates | 1,011,168 (83 countries, 400 species) |
| African ATLAS isolates | 29,387 (12 countries) |
| KEYSTONE isolates | 96,302 (2015–2025) |
| DREAM isolates | 5,928 MDR-TB |
| GASAR isolates | 496 (India) |

**Notable trends**
- *K. pneumoniae* meropenem resistance: 4.2% (2007) → **20.7%** (2024)
- *E. coli* meropenem resistance: <1% historically → **3.2%** (2024)
- *A. baumannii* meropenem resistance: ~65–71% globally; **75.9%** in Africa
- CTX-M-1 most frequent ATLAS gene marker (3.3%)
- Omadacycline MIC90 (*S. aureus*): 0.25 µg/mL
- DREAM BDQ median MIC: 0.03 µg/mL (Africa 0.06)
- GASAR: frequent ESBL/MBL phenotypes; VIM-1+NDM-1 co-detection common

## Impact

SurveilAMR provides open, reusable dashboards and tables for empiric therapy support, ASP early-warning triggers, MDR-TB bedaquiline monitoring, and mechanism-aware stewardship in LMIC health systems. Full narrative report: [`docs/SurveilAMR_Report.md`](docs/SurveilAMR_Report.md).

## Publication Acknowledgement

> This publication or presentation is based on research using data from Johnson & Johnson, Paratek, Pfizer, Venus Remedies Limited, obtained through [https://amr.vivli.org](https://amr.vivli.org)

## License

MIT License — see [LICENSE](LICENSE).

## References

- Vivli AMR Register: [https://amr.vivli.org](https://amr.vivli.org)
- 2026 Vivli AMR Surveillance Data Challenge: [https://amr.vivli.org/tag/datachallenge/](https://amr.vivli.org/tag/datachallenge/)
- Methodological inspiration: [Vivli-AMR-data-challenge-2025-VIT-](https://github.com/Belindaharyini/Vivli-AMR-data-challenge-2025-VIT-)

## Contact

Nana Safo Duker — freshsafoduker3@gmail.com
