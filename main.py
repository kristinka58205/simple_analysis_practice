# main.py
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import AppConfig
from src.data_gen import DatasetConfig, generate_dataset
from src.analysis import compute_stats, round_to_hundreds
from src.io_utils import ensure_dir, save_stats_report, save_dataframe_csv
from src.viz import plot_series_line, plot_histogram, plot_sorted_comparison


def main() -> None:
    cfg = AppConfig()

    # 1) Папка outputs/
    out_dir: Path = ensure_dir(cfg.output_dir)

    # 2) Генерация данных: Series + DataFrame (original/asc/desc)
    ds_cfg = DatasetConfig(
        n=cfg.n,
        low=cfg.low,
        high=cfg.high,
        seed=cfg.seed,
        series_name=cfg.series_name,
    )
    series, df = generate_dataset(ds_cfg)

    # 3) Статистика
    stats = compute_stats(series)

    # Печать в консоль
    print("Статистические характеристики (SimpleAnalysis):")
    for k, v in stats.items():
        print(f"{k}: {v}")

    # Сохранение в файл
    stats_path = out_dir / cfg.stats_file
    save_stats_report(stats, stats_path)

    # 4) Визуализация: линейный график исходной Series
    plot_series_line(series, save_path=out_dir / cfg.plot_series_line, show=False)

    # 5) Гистограмма: округление до сотен по математическому правилу
    series_rounded = round_to_hundreds(series)
    plot_histogram(
        series_rounded,
        save_path=out_dir / cfg.plot_hist_rounded_100,
        bins=60,
        show=False,
    )

    # 6) График сравнения двух сортировок (на одном plt)
    plot_sorted_comparison(
        df,
        col_asc="asc",
        col_desc="desc",
        save_path=out_dir / cfg.plot_sorted_compare,
        show=False,
    )

    # 7) (Опционально) сохранить DataFrame в CSV
    if cfg.save_csv:
        save_dataframe_csv(df, out_dir / cfg.csv_file, index=False)

    print("\nГотово. Результаты сохранены в папке:", out_dir.resolve())


if __name__ == "__main__":
    main()
