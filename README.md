# VeriSight AI - Review Trust Analysis Platform

VeriSight AI is an AI-powered review trust analysis platform that evaluates customer reviews and generates trust scores using a combination of NLP techniques, sentiment analysis, linguistic signals, and evidence-based scoring.

The platform helps identify potentially suspicious reviews while providing explainable insights into how trust scores are calculated.

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
* FastAPI backend with Next.js frontend

## Tech Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* FastAPI
* Python
* SQLite

### AI / NLP

* Transformer-based text classification
* Sentiment Analysis
* Rule-based linguistic analysis
* Evidence scoring engine

## Project Structure

```text
frontend/
├── app/
├── components/
├── lib/

backend/
├── app/
│   ├── api/
│   ├── services/
│   ├── schemas/
│   └── core/
```

## How It Works

1. User submits a review.
2. The backend analyzes sentiment, linguistic patterns, and contextual evidence.
3. Multiple signals are combined into a trust score.
4. The system generates confidence estimates and explainable indicators.
5. Results are displayed through the dashboard.

## API Endpoints

### Health Check

```http
GET /health
```

### Analyze Review

```http
POST /predict
```

### Batch Analysis

```http
POST /batch-predict
```

### Dashboard Information

```http
GET /dashboard
```

## Local Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8005
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8005
```

API Documentation:

```text
http://localhost:8005/docs
```

## Deployment

### Frontend

Deploy on Vercel.

### Backend

Deploy on Render.

Required environment variable:

```env
NEXT_PUBLIC_API_BASE_URL=<backend-url>
```

## Screenshots

### Review Analyzer

Add screenshot here.

### Dashboard

Add screenshot here.

## Future Improvements

* User authentication
* PostgreSQL support
* Advanced transformer models
* Enhanced explainability visualizations
* Expanded batch auditing capabilities

## Author

Sumit Kumar

GitHub: <your-github-profile>

Live Demo: <your-vercel-url>

API Docs: <your-render-url>/docs
