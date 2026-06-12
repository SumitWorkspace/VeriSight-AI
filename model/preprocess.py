from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.model_selection import train_test_split


TEXT_COLUMNS = ("review", "text", "review_text", "content")
LABEL_COLUMNS = ("label", "deceptive", "class", "polarity")


def clean_review_text(text: str) -> str:
    """Normalize review text while preserving useful punctuation."""
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    text = re.sub(r"[^a-z0-9\s.,!?'-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _find_column(columns: Iterable[str], candidates: tuple[str, ...]) -> str:
    normalized = {column.lower().strip(): column for column in columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    raise ValueError(f"Expected one of columns {candidates}, found {list(columns)}")


def normalize_label(value: object) -> int:
    raw = str(value).strip().lower()
    fake_values = {"1", "fake", "deceptive", "spam", "false", "lie", "negative"}
    genuine_values = {"0", "genuine", "truthful", "real", "true", "honest", "positive"}
    if raw in fake_values:
        return 1
    if raw in genuine_values:
        return 0
    raise ValueError(f"Unsupported label value: {value!r}")


def load_dataset(data_dir: str | Path) -> pd.DataFrame:
    data_path = Path(data_dir)
    csv_files = sorted(data_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_path.resolve()}")

    frames: list[pd.DataFrame] = []
    for csv_file in csv_files:
        frame = pd.read_csv(csv_file)
        text_column = _find_column(frame.columns, TEXT_COLUMNS)
        label_column = _find_column(frame.columns, LABEL_COLUMNS)
        frames.append(
            pd.DataFrame(
                {
                    "text": frame[text_column].map(clean_review_text),
                    "label": frame[label_column].map(normalize_label),
                }
            )
        )

    dataset = pd.concat(frames, ignore_index=True).dropna()
    dataset = dataset[dataset["text"].str.len() > 0].drop_duplicates()
    return dataset.reset_index(drop=True)


def split_dataset(
    dataset: pd.DataFrame,
    test_size: float = 0.15,
    validation_size: float = 0.15,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train_val, test = train_test_split(
        dataset,
        test_size=test_size,
        stratify=dataset["label"],
        random_state=random_state,
    )
    relative_validation = validation_size / (1 - test_size)
    train, validation = train_test_split(
        train_val,
        test_size=relative_validation,
        stratify=train_val["label"],
        random_state=random_state,
    )
    return train.reset_index(drop=True), validation.reset_index(drop=True), test.reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Preprocess fake-review dataset.")
    parser.add_argument("--data-dir", default="../dataset/raw")
    parser.add_argument("--output-dir", default="../dataset/processed")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    dataset = load_dataset(args.data_dir)
    train, validation, test = split_dataset(dataset)
    train.to_csv(output_dir / "train.csv", index=False)
    validation.to_csv(output_dir / "validation.csv", index=False)
    test.to_csv(output_dir / "test.csv", index=False)
    print(f"Wrote {len(train)} train, {len(validation)} validation, {len(test)} test rows.")


if __name__ == "__main__":
    main()
