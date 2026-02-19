# src/io_utils.py
from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd


PathLike = Union[str, Path]


def ensure_dir(path: PathLike) -> Path:
    """
    Создаёт директорию, если её нет. Возвращает Path.
    """
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_text(path: PathLike, text: str, encoding: str = "utf-8") -> Path:
    """
    Записывает текст в файл (перезапись).
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding=encoding)
    return p


def append_text(path: PathLike, text: str, encoding: str = "utf-8") -> Path:
    """
    Добавляет текст в конец файла (создаёт файл при отсутствии).
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding=encoding) as f:
        f.write(text)
    return p


def save_dataframe_csv(
    df: pd.DataFrame,
    path: PathLike,
    index: bool = False,
    encoding: str = "utf-8",
) -> Path:
    """
    Сохраняет DataFrame в CSV (по желанию для отчёта/проверки).
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df должен быть pandas.DataFrame.")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=index, encoding=encoding)
    return p


def format_stats_report(stats: dict) -> str:
    """
    Формирует красивый текстовый отчёт со статистиками.

    Ожидаемые ключи (пример):
      - n, min, max, sum, std, duplicates_count
    """
    lines = []
    lines.append("ОТЧЁТ ПО СТАТИСТИЧЕСКОМУ АНАЛИЗУ (SimpleAnalysis)\n")
    for key, value in stats.items():
        lines.append(f"{key}: {value}")
    lines.append("")  # пустая строка в конце
    return "\n".join(lines)


def save_stats_report(stats: dict, path: PathLike) -> Path:
    """
    Сохраняет текстовый отчёт со статистикой в файл.
    """
    report = format_stats_report(stats)
    return write_text(path, report)
