"""生成一份模拟的临港近地面气温数据（2024-01 ~ 2026-09，日均）。

真实数据可从中国气象数据网 / NOAA 下载替换本文件，字段保持一致即可。
"""
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(20261016)

OUT = Path(__file__).parent / "data" / "lingang_daily_temp.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

start = date(2024, 1, 1)
end = date(2026, 9, 30)


def day_offset(d: date) -> int:
    return (d - start).days


# 上海临港气候参数（1991-2020 气候 normals 近似）
TEMP_MEAN = 16.8   # 年均气温 °C
TEMP_AMP = 11.8    # 年较差的一半，最冷月均≈5°C / 最热月均≈28.6°C
PEAK_DOY = 201     # 最热日在 7 月 20 日前后 (doy)

rows = []
d = start
while d <= end:
    doy = d.timetuple().tm_yday
    seasonal = TEMP_AMP * math.sin(2 * math.pi * (doy - PEAK_DOY + 91.25) / 365.25)
    noise = random.gauss(0, 2.6)
    rows.append(
        {
            "date": d.isoformat(),
            "month": d.month,
            "mean_temp": round(TEMP_MEAN + seasonal + noise, 1),
            "rain_mm": round(max(0.0, random.gauss(6, 9)), 1),
            "aqi": int(max(15, random.gauss(78, 32))),
        }
    )
    d += timedelta(days=1)

with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["date", "month", "mean_temp", "rain_mm", "aqi"])
    w.writeheader()
    w.writerows(rows)

print(f"wrote {len(rows)} rows -> {OUT}")
print(f"span: {rows[0]['date']} ~ {rows[-1]['date']} ({day_offset(end)} days)")
