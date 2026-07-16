# SurveilAMR: AI-Enabled Surveillance Intelligence for Global Antimicrobial Resistance Trends

**2026 Vivli AMR Surveillance Data Challenge Submission**

Nana Safo Duker¹, Dr. Agnes Achiamaa Anane², Dr. Marwin Afari²

¹GeneHus, Ghana | ²Ghana Health Service, Ghana

**Repository:** [https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR](https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR)

**Data Request ID:** 00013370 | **DOI:** [https://doi.org/10.25934/PR00013370](https://doi.org/10.25934/PR00013370)

---

## Abstract

Antimicrobial resistance (AMR) continues to erode the effectiveness of essential antibiotics, yet industry surveillance data in the Vivli AMR Register are still underused for decision support in low- and middle-income countries (LMICs). **SurveilAMR** delivers a reproducible analytics pipeline across four approved Vivli datasets—Pfizer ATLAS Antibiotics (1,011,168 isolates; 83 countries; 2004–2024), Paratek KEYSTONE/omadacycline surveillance (96,302 isolates; 2015–2025), Johnson & Johnson DREAM MDR-TB (5,928 isolates; 2011–2019), and Venus Remedies GASAR Study III (496 Gram-negative isolates; India, 2022–2023). We quantified spatiotemporal resistance for ESKAPE pathogens, profiled beta-lactamase and carbapenemase markers, assessed bedaquiline MIC distributions in MDR-TB, and summarized omadacycline potency. *Klebsiella pneumoniae* meropenem resistance rose from 4.2% (2007) to 20.7% (2024). African ATLAS isolates (n = 29,387; 12 countries) showed elevated *Acinetobacter baumannii* meropenem resistance (75.9%). DREAM bedaquiline MICs remained low overall (median 0.03 µg/mL), with slightly higher African medians (0.06 µg/mL). GASAR revealed frequent ESBL/MBL phenotypes and NDM/VIM co-carriage. Code, aggregated tables, and figures are openly available for stewardship reuse.

---

## Objectives

1. **Country and regional AMR trends** — Compare resistance trajectories across geographic strata to inform empiric therapy and guideline updates.
2. **Pathogen-specific surveillance** — Characterize priority organisms (*E. coli*, *K. pneumoniae*, *P. aeruginosa*, *S. aureus*, *A. baumannii*, *E. faecalis*) against WHO-priority antibiotic classes.
3. **Resistance mechanism profiling** — Map ESBL and carbapenemase gene markers (CTX-M, KPC, NDM, OXA, SHV, TEM) and GASAR gene/phenotype combinations.
4. **Temporal early-warning signals** — Detect accelerating carbapenem and cephalosporin resistance suitable for antimicrobial stewardship program (ASP) alerts.
5. **Cross-dataset stewardship intelligence** — Integrate ATLAS bacterial trends with KEYSTONE (novel tetracycline), DREAM (MDR-TB/bedaquiline), and GASAR (polymyxin/mechanisms) for LMIC-relevant decision support, including Ghana Health Service partners.

---

## Methods

### Data sources

Primary analysis used **ATLAS_Antibiotics** (Pfizer Inc.): isolate metadata (species, country, age group, specimen source, year, study arm) with MIC values and Susceptible/Intermediate/Resistant labels for up to 47 antibiotics and 23 resistance gene markers. Complementary datasets from Data Request 00013370 included **KEYSTONE** (Paratek; omadacycline and comparator MICs), **DREAM** (Johnson & Johnson; MDR-TB bedaquiline broth/MGIT MICs and companion drugs), and **GASAR Study III** (Venus Remedies; Gram-negative isolates with phenotypic/genotypic combinations and polymyxin B MICs). Raw industry files are not redistributed; processed aggregates are published in the repository: [https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR](https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR).

### Preprocessing and quality control

Susceptibility labels were standardized to S/I/R. ATLAS analyses required minimum stratum sizes (n ≥ 20 year–species–drug; n ≥ 50 country–species). MIC strings containing inequality symbols were parsed to numeric values for DREAM and KEYSTONE. GASAR phenotypes were bucketed into Non-ESBL/Non-MBL, ESBL, MBL, ESBL+MBL, Carbapenemase, and Other. DREAM MDR-TB subtypes were normalized to MDR, Pre-XDR, XDR, RR/RIF-R, and Other.

### Analytical pipeline

Analyses were implemented in **Python 3.10+** (Pandas, NumPy, SciPy, Matplotlib, Seaborn). Modular scripts perform chunked ATLAS EDA, yearly/country resistance estimation, gene prevalence, MDR proxy scoring (≥2 resistant classes), and supplementary-dataset summaries (`scripts/run_analysis.py`, `scripts/analyze_supplementary.py`, `scripts/generate_figures.py`). Methods follow reproducible practices from the 2025 Vivli Grand Prize VIT repository, adapted for bacterial/TB stewardship use cases.

### Statistical considerations

Resistance proportions are reported with isolate denominators. Temporal patterns are primarily descriptive. Limitations include surveillance sampling bias (ATLAS/KEYSTONE over-represent North America and Europe), incomplete gene testing coverage in ATLAS, heterogeneous DREAM subtype labeling, and absence of patient-level treatment outcomes.

---

## Results

### Dataset overview (multi-source)

**Table 1. SurveilAMR Vivli Datasets Analyzed**

| Dataset | Contributor | Isolates | Years | Geography |
|---------|-------------|----------|-------|-----------|
| ATLAS Antibiotics | Pfizer | 1,011,168 | 2004–2024 | 83 countries |
| KEYSTONE | Paratek | 96,302 | 2015–2025 | 20 countries (NA/EU) |
| DREAM (MDR-TB) | Johnson & Johnson | 5,928 | 2011–2019 | 11 countries |
| GASAR Study III | Venus Remedies | 496 | 2022–2023 | India |

ATLAS top contributors were the United States (165,880), Spain (65,418), and France (62,065). Dominant species were *S. aureus* (172,883), *E. coli* (125,878), *P. aeruginosa* (115,807), and *K. pneumoniae* (106,946). African ATLAS representation totaled 29,387 isolates (South Africa 14,958; Morocco 5,310; Nigeria 4,824; Ghana 210).

![Top 15 pathogens](../outputs/figures/fig1_species_distribution.png)

**Figure 1.** Top 15 pathogens in ATLAS Antibiotics surveillance (2004–2024).

### Temporal resistance trends (ATLAS)

*K. pneumoniae* meropenem resistance increased from **4.2% (2007)** to **20.7% (2024)**. *E. coli* meropenem resistance rose from <1% historically to **3.2% (2024)**. *A. baumannii* meropenem resistance remained **65–71%**. *P. aeruginosa* stabilized near 18–22%. *S. aureus* oxacillin resistance declined from ~60% (2012–2017) to **25.7% (2024)**.

![ESKAPE resistance trends](../outputs/figures/fig3_resistance_trends.png)

**Figure 2.** Year-over-year resistance for priority antibiotic–pathogen pairs.

**Table 2. Selected Resistance Rates — Global vs African ATLAS Subset**

| Pathogen | Antibiotic | Global 2024 | Africa |
|----------|------------|-------------|--------|
| *K. pneumoniae* | Meropenem | 20.7% | 12.8% (n=4,131) |
| *E. coli* | Meropenem | 3.2% | 1.4% (n=4,469) |
| *P. aeruginosa* | Meropenem | 18.0% | 20.1% (n=3,547) |
| *A. baumannii* | Meropenem | 68.5% | 75.9% (n=1,496) |
| *S. aureus* | Oxacillin | 25.7% | 31.0% (n=3,657) |

### Geographic and mechanism patterns

Country heatmaps highlighted *A. baumannii* meropenem non-susceptibility hotspots (Ukraine 93.8%, Jordan 93.0%, Greece 91.5%) and *K. pneumoniae* carbapenem resistance (Ukraine 60.9%, India 53.6%, Greece 50.4%). ATLAS gene detection was highest for CTX-M-1 (3.32%), TEM (2.88%), and SHV (2.76%); KPC/NDM/OXA were each ~0.5%. MDR proxy rates reached 29.1% (*A. baumannii*), 9.7% (*K. pneumoniae*), and 0.9% (*E. coli*).

![Country resistance heatmap](../outputs/figures/fig4_country_resistance_heatmap.png)

**Figure 3.** Country-level resistance heatmap for priority pathogens.

![Beta-lactamase gene prevalence](../outputs/figures/fig5_gene_prevalence.png)

**Figure 4.** Beta-lactamase and carbapenemase gene detection (ATLAS).

### KEYSTONE, DREAM, and GASAR findings

In KEYSTONE, omadacycline retained potent activity against *S. aureus* (MIC50/90 0.12/0.25 µg/mL) and *S. pneumoniae* (0.06/0.12), with higher MICs for *K. pneumoniae* (2.0/4.0). DREAM bedaquiline broth MICs were low overall (median 0.03 µg/mL; >0.25 µg/mL in 0.6% of isolates); African isolates (South Africa, n=978) had a higher median (0.06 µg/mL). GASAR (India) showed Non-ESBL/Non-MBL (n=200), ESBL (99), and MBL (77) as leading phenotypes; VIM-1+NDM-1 co-detection was frequent (n=41), and polymyxin B MIC ≥4 µg/mL occurred in 3.0% of isolates.

![DREAM bedaquiline](../outputs/figures/fig7_dream_bdq.png)

**Figure 5.** DREAM bedaquiline MIC distributions by continent and year.

![GASAR mechanisms](../outputs/figures/fig8_gasar_mechanisms.png)

**Figure 6.** GASAR phenotypic classes and top gene combinations (India).

---

## Impact of the Work

SurveilAMR converts restricted Vivli surveillance assets into **open, reproducible intelligence** for Ghana Health Service stewardship and the 2026 Vivli challenge goals.

**Clinical decision support.** Country- and pathogen-specific resistance views support empiric selection when cultures are delayed—critical where microbiology capacity is limited.

**Antimicrobial stewardship.** Rising *K. pneumoniae* carbapenem resistance and African *A. baumannii* burden provide quantifiable ASP triggers. KEYSTONE MIC summaries inform positioning of newer agents; DREAM BDQ distributions support MDR-TB program monitoring; GASAR mechanism maps highlight NDM/VIM co-carriage risk.

**Public health policy.** Temporal early-warning metrics align with WHO GLASS-style reporting and national guideline revision.

**Research infrastructure.** The repository ([https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR](https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR)) provides chunked-analysis templates, processed CSVs, and figure scripts that lower barriers for Vivli data reuse, following the reproducibility standard of the 2025 VIT Grand Prize winners.

Future work will add interactive dashboards and time-series forecasting for African sentinel sites, including Ghana.

---

## References

1. Naghavi M, Vollset SE, Ikuta KS, et al. Global burden of bacterial antimicrobial resistance 1990–2021: a systematic analysis with forecasts to 2050. *Lancet*. 2024;404:1199–1226.

2. World Health Organization. WHO bacterial priority pathogens list, 2024. Geneva: WHO; 2024.

3. Vivli AMR Register. 2026 Vivli AMR Surveillance Data Challenge. Available at: https://amr.vivli.org/tag/datachallenge/

4. Haryini SS, Karve S, Priya Doss CG, et al. Temporal links between ambient air pollutants and antifungal drug resistance in *Candida glabrata*. *Wellcome Open Res*. 2026. Code: https://github.com/Belindaharyini/Vivli-AMR-data-challenge-2025-VIT-

5. Pfizer Inc. ATLAS Global Antimicrobial Surveillance Program. Data via Vivli AMR Register (ATLAS_Antibiotics).

6. SurveilAMR Team. SurveilAMR: Vivli AMR 2026 Data Challenge Repository. 2026. https://github.com/Nana-Safo-Duker/Vivli-AMR-2026-Data-Challenge-SurveilAMR

7. Prestinaci F, Pezzotti P, Pantosti A. Antimicrobial resistance: a global multifaceted phenomenon. *Pathog Glob Health*. 2015;109(7):309–318.

8. Tadesse BT, Ashley EA, Ongarello S, et al. Antimicrobial resistance in Africa: a systematic review. *BMC Infect Dis*. 2017;17(1):616.

9. World Health Organization. WHO consolidated guidelines on tuberculosis. Module 4: treatment — drug-resistant tuberculosis treatment. Geneva: WHO; 2022.

10. Johnson & Johnson; Paratek Pharmaceuticals; Pfizer Inc.; Venus Remedies Limited. Vivli AMR Register industry surveillance datasets. Accessed via https://amr.vivli.org (Data Request 00013370).

---

> **Acknowledgement:** This publication is based on research using data from Johnson & Johnson, Paratek, Pfizer, Venus Remedies Limited, obtained through https://amr.vivli.org
