# Installation Guide

## Prerequisites

- Python 3.10-3.12
- Node.js 18+
- npm
- Optional: Docker Desktop

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Dataset Setup

Download the Kaggle Deceptive Opinion Spam Corpus and place the CSV files in `dataset/raw/`.

## Model Training

```bash
cd model
python train.py --data-dir ../dataset/raw --output-dir ./saved_model
```

After training, restart the backend so it loads the saved model.
