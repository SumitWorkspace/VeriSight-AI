# Deployment

## Docker Compose

```bash
docker compose up --build
```

## Backend Environment

- `DATABASE_URL`: SQLite URL
- `MODEL_DIR`: path to saved Hugging Face model
- `FRONTEND_ORIGIN`: allowed CORS origin

## Frontend Environment

- `NEXT_PUBLIC_API_BASE_URL`: FastAPI base URL

## Production Notes

- Train the model before deployment and mount/copy `model/saved_model`.
- Replace SQLite with PostgreSQL for high-volume multi-user traffic.
- Serve the frontend through a platform such as Vercel, Netlify, or a Node container.
- Serve the backend through a Python platform with persistent storage for the model and database.
