
# src/analysis.py
from __future__ import annotations

import numpy as np
import pandas as pd


def count_duplicates(series: pd.Series) -> int:
    """
    Количество повторяющихся значений в Series.

    Здесь считаем так:
    - если значение встретилось k раз, то "повторами" считаем (k - 1)
      (т.е. сколько элементов являются лишними повторениями).
    Пример: [5, 5, 5, 7] -> для 5 повторы = 2, итого 2.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("series должен быть pandas.Series.")
    if len(series) == 0:
        return 0

    counts = series.value_counts(dropna=False)
    duplicates = int((counts[counts > 1] - 1).sum())
    return duplicates


def compute_stats(series: pd.Series) -> dict:
    """
    Считает статистики по Series согласно заданию:
    - min
    - max
    - sum
    - std (среднеквадратическое отклонение)
    - количество повторяющихся значений

    Примечание по std:
    Используем "популяционное" стандартное отклонение (ddof=0),
    что соответствует формуле σ = sqrt( (1/n) * Σ(x_i - x̄)² ).
    """
    if not isinstance(series, pd.Series):
        raise TypeError("series должен быть pandas.Series.")
    if len(series) == 0:
        raise ValueError("series не должен быть пустым.")

    # Приводим к числам на всякий случай (для этой практики данные целые)
    s = pd.to_numeric(series, errors="coerce")

    stats = {
        "n": int(s.size),
        "min": int(s.min()),
        "max": int(s.max()),
        "sum": int(s.sum()),
        "std": float(s.std(ddof=0)),
        "duplicates_count": int(count_duplicates(s)),
    }
    return stats


def round_to_hundreds(series: pd.Series) -> pd.Series:
    """
    Округление значений до сотен по математическому правилу.
    Например:
      149 -> 100
      150 -> 200
      -149 -> -100
      -150 -> -200

    Используем numpy.rint(x/100)*100 (округление к ближайшему, .5 к чётному),
    но для целевых значений кратных 50 может отличаться от "школьного" в редких случаях.
    Поэтому реализуем явно через деление + floor/ceil.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("series должен быть pandas.Series.")
    if len(series) == 0:
        return series

    x = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)

    # "Школьное" округление: половины (±0.5) округляем от нуля.
    # Делим на 100 -> округляем -> умножаем.
    scaled = x / 100.0
    rounded_scaled = np.where(
        scaled >= 0,
        np.floor(scaled + 0.5),
        np.ceil(scaled - 0.5),
    )
    rounded = (rounded_scaled * 100.0).astype(int)

    return pd.Series(rounded, name=f"{series.name}_rounded_100" if series.name else "rounded_100")
