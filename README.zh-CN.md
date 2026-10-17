# Lingang Temperature Trend Analysis

[运行记录](https://github.com/John-J-ai/project-01-env-trend/actions) · [English](README.md)

![Analysis workflow](https://github.com/John-J-ai/project-01-env-trend/actions/workflows/rebuild.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> Data analysis & visualization project — Shanghai Lingang, 2024–2026.
> Coursework for the *Introduction to Artificial Intelligence* programme (Python fundamentals track).

> **关于数据。** `output/` 下的图表由 GitHub Actions 在每次 push 时自动重新生成，
> 所以图永远对应当前代码。数据集为合成数据 —— 在得出任何现实结论前请先看
> [Data](#data) 一节说明的理由。

## Question

What are the seasonal characteristics of near-surface air temperature in Lingang, Shanghai?
How large is the day-to-day fluctuation within each month? And does precipitation have any
relationship with air quality (AQI)?

## Tech stack

Python 3.13 · pandas · numpy · matplotlib

## Quick start

```bash
pip install -r requirements.txt
python make_dataset.py   # generates the dataset (run once)
python main.py           # analysis + figures
```

Figures are written to `output/`:

| File | Content |
|---|---|
| `01_monthly_temperature.png` | Monthly mean temperature with 10–90% quantile band |
| `02_rain_vs_aqi.png` | Daily precipitation vs AQI scatter plot |

## Data

`data/lingang_daily_temp.csv` is **synthetic data**, 1,004 daily records spanning
2024-01-01 to 2026-09-30, generated from Shanghai Lingang climate normals
(annual mean 16.8 °C, peak in July, trough in January).

> ⚠️ **The synthetic dataset is a pipeline demonstration, not evidence.**
> `rain_mm` and `aqi` are drawn from independent random distributions, so no physical
> relationship can appear in the scatter plot. Real-world data behaves the *opposite*
> way — precipitation scavenges particulate matter and lowers AQI. Replace this file
> with an observational source (China Meteorological Data Service Centre, or ECMWF ERA5)
> before drawing any real conclusion. Field contract:
> `date, month, mean_temp, rain_mm, aqi`.

## Findings

**Figure 1 — monthly mean temperature (valid)**
- Annual mean 17.3 °C, seasonal amplitude roughly ±12 °C.
- The 10–90% quantile band spans only 2–4 °C: inter-annual variation is much smaller
  than intra-seasonal variation.
- The seasonal curve is remarkably stable across the three years.

**Figure 2 — precipitation vs AQI (null result, reported as such)**
- No discernible correlation in the synthetic data, for the reason stated above.
- The useful takeaway is methodological: **an analytical conclusion is bound to its data
  source.** Running the same pipeline on observational data reverses the sign of the
  relationship.

## Why this project is worth doing

The analysis itself is a standard exercise. The value is in the engineering discipline
around it:

- Non-GUI rendering (`matplotlib.use("Agg")`) so the pipeline runs on a locked-down lab machine.
- Explicit CJK font registration — otherwise every Chinese label renders as tofu boxes.
- Reproducibility: fixed random seed, one-command data generation, no manual steps.
- Honest reporting: the null result is documented instead of being replaced by a
  fabricated narrative. A null result is a result.

## Possible extensions

- Add ERA5 reanalysis data and compute seasonal anomalies against the 1991–2020 baseline.
- Fit a linear model of AQI on precipitation and daily wind speed (this is where
  `scikit-learn` enters the stack).
- Compare Lingang against other Shanghai stations to examine the urban heat island effect.

## Licence

MIT
