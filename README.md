# VeriSight AI - AI-Powered Review Trust Analysis Platform

VeriSight AI is a full-stack AI application that analyzes customer reviews and generates trust scores using a hybrid approach that combines NLP classification, sentiment analysis, linguistic signals, and evidence-based scoring.

The platform helps identify potentially suspicious reviews while providing explainable insights into how trust scores are calculated.

## Live Links

* Live Demo: https://veri-sight-ai.vercel.app/
* API Documentation: https://verisight-ai-6i41.onrender.com/docs
* GitHub Repository: https://github.com/SumitWorkspace/VeriSight-AI

---

## Features

* AI-powered review trust analysis
* Trust score generation with confidence estimates
* Sentiment analysis
* Linguistic pattern detection
* Suspicious phrase identification
* Evidence strength assessment
* Explainable AI indicators
* Interactive dashboard
* Batch review analysis via CSV upload
* FastAPI REST API
* Responsive modern UI

---

## Tech Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* FastAPI
* Python

### Database

* SQLite

### AI & NLP

* Hybrid Model + Rule Engine
* Transformer-based text classification
* VADER Sentiment Analysis
* Linguistic Feature Analysis
* Evidence Scoring Engine

---

## How It Works

1. User submits a review.
2. The backend analyzes sentiment, linguistic patterns, and contextual evidence.
3. Multiple signals are combined into a calibrated trust score.
4. Confidence levels and explainable indicators are generated.
5. Results are displayed through the dashboard.

---

## API Endpoints

### Health Check

```http
GET /health
```

### Analyze Single Review

```http
POST /predict
```

### Batch Review Analysis

```http
POST /batch-predict
```

### Dashboard Information

```http
GET /dashboard
```

---

## Project Structure

```text
VeriSight-AI
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   └── lib/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── schemas/
│   │   └── services/
│   └── requirements.txt
│
├── README.md
└── render.yaml
```

---

## Local Setup

### Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8005
```

Backend URL:

```text
http://localhost:8005
```

API Documentation:

```text
http://localhost:8005/docs
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Create a `.env.local` file inside `frontend`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8005
```

Frontend URL:

```text
http://localhost:3000
```

---

## Deployment

### Frontend

* Hosted on Vercel

### Backend

* Hosted on Render

### Production Environment Variable

```env
NEXT_PUBLIC_API_BASE_URL=https://verisight-ai-6i41.onrender.com
```
---

## Future Improvements

* User authentication
* PostgreSQL support
* Advanced transformer models
* Enhanced explainability visualizations
* Multi-user analytics

---

## Author

Sumit Kumar

GitHub: https://github.com/SumitWorkspace
