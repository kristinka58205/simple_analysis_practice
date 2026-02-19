# src/config.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class AppConfig:
    """
    Конфигурация приложения (практика SimpleAnalysis).

    n: количество чисел (по заданию 1000)
    low/high: диапазон целых чисел (по заданию -10000..10000)
    seed: фиксируем для воспроизводимости (можно None)
    """
    n: int = 1000
    low: int = -10000
    high: int = 10000
    seed: Optional[int] = 42

    # Имена/пути
    series_name: str = "x"
    output_dir: Path = Path("outputs")

    # Файлы результатов
    stats_file: str = "stats.txt"

    # Графики
    plot_series_line: str = "series_line.png"
    plot_hist_rounded_100: str = "hist_rounded_100.png"
    plot_sorted_compare: str = "sorted_compare.png"

    # (Опционально) сохранять DataFrame в CSV
    save_csv: bool = True
    csv_file: str = "dataset.csv"
