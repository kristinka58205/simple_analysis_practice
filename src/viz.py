
# src/viz.py
from __future__ import annotations

from pathlib import Path
from typing import Union, Optional

import matplotlib.pyplot as plt
import pandas as pd


PathLike = Union[str, Path]


def plot_series_line(
    series: pd.Series,
    save_path: Optional[PathLike] = None,
    show: bool = False,
) -> None:
    """
    Линейный график по исходной Series (по индексам).
    """
    if not isinstance(series, pd.Series):
        raise TypeError("series должен быть pandas.Series.")
    if len(series) == 0:
        raise ValueError("series не должен быть пустым.")

    plt.figure()
    plt.plot(series.index, series.values)
    plt.title("Линейный график исходной последовательности")
    plt.xlabel("Индекс")
    plt.ylabel("Значение")

    if save_path is not None:
        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(p, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    plt.close()


def plot_histogram(
    series_rounded: pd.Series,
    save_path: Optional[PathLike] = None,
    bins: int = 50,
    show: bool = False,
) -> None:
    """
    Гистограмма по Series (ожидается уже округлённая до сотен).
    """
    if not isinstance(series_rounded, pd.Series):
        raise TypeError("series_rounded должен быть pandas.Series.")
    if len(series_rounded) == 0:
        raise ValueError("series_rounded не должен быть пустым.")

    plt.figure()
    plt.hist(series_rounded.values, bins=bins)
    plt.title("Гистограмма (значения округлены до сотен)")
    plt.xlabel("Значение")
    plt.ylabel("Частота")

    if save_path is not None:
        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(p, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    plt.close()


def plot_sorted_comparison(
    df: pd.DataFrame,
    col_asc: str = "asc",
    col_desc: str = "desc",
    save_path: Optional[PathLike] = None,
    show: bool = False,
) -> None:
    """
    На одном графике строит 2 линии:
    - сортировка по возрастанию
    - сортировка по убыванию

    Ожидается DataFrame, содержащий указанные колонки.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df должен быть pandas.DataFrame.")
    if col_asc not in df.columns or col_desc not in df.columns:
        raise ValueError(f"В df должны быть колонки '{col_asc}' и '{col_desc}'.")

    plt.figure()
    plt.plot(df.index, df[col_asc].values, label="По возрастанию")
    plt.plot(df.index, df[col_desc].values, label="По убыванию")
    plt.title("Сравнение отсортированных последовательностей")
    plt.xlabel("Индекс")
    plt.ylabel("Значение")
    plt.legend()

    if save_path is not None:
        p = Path(save_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(p, dpi=150, bbox_inches="tight")

    if show:
        plt.show()

    plt.close()
