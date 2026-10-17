"""Project 01 - 气温趋势可视化

用法:
    python make_dataset.py     # 首次运行，生成模拟数据
    python main.py             # 分析并出图

输出: output/ 下两张图 + 控制台统计摘要
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # 无 GUI 环境（学校机房/远程）下出图
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager

BASE = Path(__file__).parent
DATA = BASE / "data" / "lingang_daily_temp.csv"
OUT = BASE / "output"

# 中文字体：Windows 用微软雅黑，macOS/Linux 回退自动探测
for _fp in [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "/System/Library/Fonts/PingFang.ttc",
]:
    if Path(_fp).exists():
        font_manager.fontManager.addfont(_fp)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=_fp).get_name()
        break
plt.rcParams["axes.unicode_minus"] = False

if not DATA.exists():
    raise SystemExit("缺少数据集，先运行: python make_dataset.py")

df = pd.read_csv(DATA, parse_dates=["date"]).sort_values("date")
df["year_month"] = df["date"].dt.to_period("M")

OUT.mkdir(exist_ok=True)

# --- 图1: 月均气温 + 上下限带 -------------------------------------------------
monthly = df.groupby("year_month").agg(
    mean=("mean_temp", "mean"),
    lo=("mean_temp", lambda s: s.quantile(0.1)),
    hi=("mean_temp", lambda s: s.quantile(0.9)),
    rain=("rain_mm", "sum"),
)

fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(monthly.index.to_timestamp(), monthly["mean"], lw=2, label="月均气温")
ax.fill_between(
    monthly.index.to_timestamp(), monthly["lo"], monthly["hi"],
    alpha=0.18, label="10%–90% 分位带",
)
ax.set_title("临港近地面月均气温与波动区间 (2024-01 ~ 2026-09)")
ax.set_ylabel("气温 (°C)")
ax.legend(frameon=False)
ax.grid(alpha=0.25, ls=":")
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(OUT / "01_monthly_temperature.png", dpi=160)
plt.close(fig)

# --- 图2: 降水 vs 空气质量 ----------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4))
ax.scatter(df["rain_mm"], df["aqi"], s=6, alpha=0.35, edgecolors="none")
ax.axhline(75, color="#A32D2D", lw=1, ls="--", label="AQI 良(75)")
ax.set_xlabel("日降水量 (mm)")
ax.set_ylabel("AQI")
ax.set_title("降水与空气质量的关系")
ax.legend(frameon=False)
ax.grid(alpha=0.25, ls=":")
fig.tight_layout()
fig.savefig(OUT / "02_rain_vs_aqi.png", dpi=160)
plt.close(fig)

# --- 控制台摘要 ---------------------------------------------------------------
print("== 数据概览 ==")
print(f"样本区间 : {df['date'].min().date()} ~ {df['date'].max().date()}")
print(f"总天数   : {len(df)}")
print(f"年均气温 : {df['mean_temp'].mean():.1f} °C")
print(f"最热日   : {df.loc[df['mean_temp'].idxmax(), 'mean_temp']} °C")
print("\n== 按年对比 ==")
print(df.groupby(df["date"].dt.year)["mean_temp"].agg(["mean", "min", "max"]).round(1))
print("\n== 分季统计 ==")
season = df.groupby(df["date"].dt.month)["aqi"].mean().round(1)
print("月均 AQI:", season.to_dict())
print(f"\n图表已保存 -> {OUT}")
print("提醒: 本数据集为模拟数据,rain 与 aqi 无物理关联,结论仅用于演示流程。")
