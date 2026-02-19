# src/data_gen.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DatasetConfig:
    """Параметры генерации набора данных."""
    n: int = 1000
    low: int = -10000
    high: int = 10000
    seed: Optional[int] = 42
    series_name: str = "x"


def generate_series(
    n: int,
    low: int,
    high: int,
    seed: Optional[int] = None,
    name: str = "x",
) -> pd.Series:
    """
    Генерирует pandas.Series из n целых чисел в диапазоне [low; high] (включительно).

    Args:
        n: количество значений (например, 1000)
        low: нижняя граница (например, -10000)
        high: верхняя граница (например, 10000)
        seed: seed для воспроизводимости (None -> случайно)
        name: имя Series

    Returns:
        pd.Series длины n
    """
    if n <= 0:
        raise ValueError("n должно быть положительным числом.")
    if low > high:
        raise ValueError("low не может быть больше high.")

    rng = np.random.default_rng(seed)
    # np.random.integers: верхняя граница не включается, поэтому high + 1
    data = rng.integers(low=low, high=high + 1, size=n, dtype=np.int64)

    s = pd.Series(data, name=name)
    return s


def make_analysis_dataframe(series: pd.Series) -> pd.DataFrame:
    """
    Формирует DataFrame с исходными данными и двумя доп. столбцами:
    - сортировка по возрастанию
    - сортировка по убыванию

    Важно: длины одинаковые, индексы выровнены по 0..n-1.

    Columns:
        original, asc, desc
    """
    if series is None:
        raise ValueError("series не должен быть None.")
    if not isinstance(series, pd.Series):
        raise TypeError("series должен быть pandas.Series.")
    if len(series) == 0:
        raise ValueError("series не должен быть пустым.")

    values = series.to_numpy(copy=False)

    asc = np.sort(values)
    desc = asc[::-1]

    df = pd.DataFrame(
        {
            "original": values,
            "asc": asc,
            "desc": desc,
        }
    )
    return df


def generate_dataset(cfg: DatasetConfig) -> tuple[pd.Series, pd.DataFrame]:
    """
    Удобный хелпер: сгенерировать Series и сразу DataFrame для анализа/графиков.
    """
    s = generate_series(
        n=cfg.n,
        low=cfg.low,
        high=cfg.high,
        seed=cfg.seed,
        name=cfg.series_name,
    )
    df = make_analysis_dataframe(s)
    return s, df
