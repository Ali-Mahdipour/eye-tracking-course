# Instructor-only — Food Decision Making full analysis

**Not for students.** Use this notebook to prepare presentations and answer Q&A.

- Notebook: `Food_Decision_Making_Full_Analysis.ipynb`
- Outputs: `figures/`, `tables/`

Canonical complete data (local):  
`C:\Users\snapp\Desktop\Food Decision Making Data Export.tsv`  
→ place a copy at `Data/food_decision_making/Food Decision Making Data Export.tsv` before running
(that TSV itself is gitignored because it is large). If missing, the notebook extracts it from
`Data/decision making/Food Decision Making Data Export.zip`.

## Teaching extras (fixation filters)

| Section | What it does | Key outputs |
|---------|--------------|-------------|
| **6b DIY I-VT** | Re-implement I-VT; assert 100% match to `ivt_classify`; compare to Tobii | `tables/diy_ivt_coincidence.csv`, `figures/diy_ivt_velocity_demo.png` |
| **6c I-DT** | Dispersion-threshold alternative; compare I-VT vs I-DT vs Tobii | `tables/fixation_filter_comparison.csv`, `tables/idt_fix_summary.csv`, `figures/ivt_vs_idt_mean_fix.png` |
| **Appendix** | Function & argument encyclopedia for live student Q&A | (markdown only) |
