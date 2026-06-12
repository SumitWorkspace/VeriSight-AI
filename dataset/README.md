# Dataset

Use the Deceptive Opinion Spam Corpus from Kaggle.

Recommended layout:

```text
dataset/
  raw/
    deceptive-opinion.csv
```

The training pipeline accepts CSV files with flexible column names. It looks for:

- review text: `review`, `text`, `review_text`, or `content`
- label: `label`, `deceptive`, `class`, or `polarity`

Labels are normalized to:

- `0`: Genuine Review
- `1`: Fake Review

Large raw data files are intentionally ignored by Git.
