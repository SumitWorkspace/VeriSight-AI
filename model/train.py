from __future__ import annotations

import argparse
import json
from pathlib import Path

import evaluate
import numpy as np
from datasets import Dataset, DatasetDict
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EvalPrediction,
    Trainer,
    TrainingArguments,
)

from preprocess import load_dataset, split_dataset


def build_hf_dataset(data_dir: str, tokenizer_name: str, max_length: int) -> tuple[DatasetDict, object]:
    dataset = load_dataset(data_dir)
    train, validation, test = split_dataset(dataset)
    hf_dataset = DatasetDict(
        {
            "train": Dataset.from_pandas(train),
            "validation": Dataset.from_pandas(validation),
            "test": Dataset.from_pandas(test),
        }
    )
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def tokenize(batch: dict[str, list[str]]) -> dict[str, object]:
        return tokenizer(batch["text"], truncation=True, max_length=max_length)

    tokenized = hf_dataset.map(tokenize, batched=True)
    tokenized = tokenized.remove_columns(["text"])
    tokenized = tokenized.rename_column("label", "labels")
    tokenized.set_format("torch")
    return tokenized, tokenizer


def compute_metrics_factory() -> object:
    accuracy = evaluate.load("accuracy")
    precision = evaluate.load("precision")
    recall = evaluate.load("recall")
    f1 = evaluate.load("f1")

    def compute_metrics(eval_prediction: EvalPrediction) -> dict[str, float]:
        logits = eval_prediction.predictions
        labels = eval_prediction.label_ids
        predictions = np.argmax(logits, axis=-1)
        return {
            "accuracy": accuracy.compute(predictions=predictions, references=labels)["accuracy"],
            "precision": precision.compute(predictions=predictions, references=labels, zero_division=0)["precision"],
            "recall": recall.compute(predictions=predictions, references=labels, zero_division=0)["recall"],
            "f1": f1.compute(predictions=predictions, references=labels)["f1"],
        }

    return compute_metrics


def train(args: argparse.Namespace) -> None:
    tokenized, tokenizer = build_hf_dataset(args.data_dir, args.model_name, args.max_length)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name,
        num_labels=2,
        id2label={0: "Genuine", 1: "Fake"},
        label2id={"Genuine": 0, "Fake": 1},
    )

    output_dir = Path(args.output_dir)
    training_args = TrainingArguments(
        output_dir=str(output_dir / "checkpoints"),
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        logging_steps=20,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
        compute_metrics=compute_metrics_factory(),
    )
    trainer.train()
    metrics = trainer.evaluate(tokenized["test"])

    output_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    with (output_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fine-tune RoBERTa for fake review detection.")
    parser.add_argument("--data-dir", default="../dataset/raw")
    parser.add_argument("--output-dir", default="./saved_model")
    parser.add_argument("--model-name", default="roberta-base")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--max-length", type=int, default=256)
    return parser.parse_args()


if __name__ == "__main__":
    train(parse_args())
