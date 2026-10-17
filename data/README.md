# 数据目录

`make_dataset.py` 会在此生成 `lingang_daily_temp.csv`。

该文件**不入库**（已在 .gitignore 中忽略），因为：

1. 由脚本一键生成，无需版本控制
2. 换成真实数据时体积可能达数十 MB

**换成真实数据**：从中国气象数据网（data.cma.cn）或 ECMWF ERA5 下载后，
按以下字段整理为同名 CSV 即可无缝替换：

```
date,month,mean_temp,rain_mm,aqi
```

`main.py` 会自动检测文件是否存在（不存在时会提示先跑 `make_dataset.py`）。
