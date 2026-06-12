# VeriSight AI Health & Verification Manual

This guide outlines startup verification procedures, environment variables, deployment checklists, and troubleshooting protocols for the VeriSight AI MVP stack.

---

## 1. Startup Verification Guide

### Backend (FastAPI API Server)
1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```
2. **Activate the virtual environment**:
   * Windows:
     ```powershell
     .venv312\Scripts\activate
     ```
   * macOS / Linux:
     ```bash
     source .venv/bin/activate
     ```
3. **Run the API server**:
   ```bash
   uvicorn app.main:app --port 8005 --reload
   ```
4. **Expected Output (Diagnostics Report)**:
   ```text
   ============================================================
    VERISIGHT AI BACKEND STARTUP DIAGNOSTICS
   ============================================================
   App Name:        Fake Review Detection API
   Database URL:    sqlite:///./fake_reviews.db
   Model Directory: ../model/saved_model
   Frontend Origin: http://localhost:3000
   Database Status:  OK (Connection successful & verified)
   Classifier Model: LOADED (High-fidelity Neural Transformer Active)
   ============================================================
   ```
5. **Verify Endpoint**: Check health status at `http://localhost:8005/health`.

### Frontend (Next.js Dashboard UI)
1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Start the development server**:
   ```bash
   npm run dev
   ```
4. **Open in browser**: Visit `http://localhost:3000`.

---

## 2. Required Environment Variables

### Backend Configuration (`backend/.env`)
* `DATABASE_URL`: Connection string for the database (Default: `sqlite:///./fake_reviews.db`). Retained for future data expansion.
* `MODEL_DIR`: Path to the trained NLP transformer model (Default: `../model/saved_model`).
* `FRONTEND_ORIGIN`: Allowed origin for CORS requests (Default: `http://localhost:3000`).

### Frontend Configuration (`frontend/.env.local`)
* `NEXT_PUBLIC_API_BASE_URL`: Base address of the running backend API (Default: `http://localhost:8005`).

---

## 3. Production Deployment Checklist

- [ ] **Transformer Model Exists**: Check that the model is present in `model/saved_model` or compile it into the build. Note: Large model files might require Git LFS or external cloud storage.
- [ ] **Rate Limiting Setup**: Verify the backend is using the sliding window limiter (`SlidingWindowRateLimiter`).
- [ ] **FastAPI Origins Configured**: Update `FRONTEND_ORIGIN` inside `backend/.env` with the URL of the deployed frontend.
- [ ] **Next.js API Base URL Configured**: Set `NEXT_PUBLIC_API_BASE_URL` to the public backend API url in Vercel settings.
- [ ] **Database Connection Health**: Verify database connection status resolves to OK on backend startup.

---

## 4. Troubleshooting Steps

### 1. "Unable to connect to the VeriSight AI backend" (Frontend Error)
* **Cause**: Backend server is offline, running on a different port, or blocked by CORS.
* **Resolution**:
  * Verify uvicorn is running on port 8005.
  * Check that `frontend/.env.local` contains `NEXT_PUBLIC_API_BASE_URL=http://localhost:8005`.
  * Inspect the browser developer console (F12) for CORS blocks. Ensure `FRONTEND_ORIGIN` matches the exact client URL.

### 2. "Classifier Model: WARNING (Model folder not found...)"
* **Cause**: The relative path configured in `MODEL_DIR` does not point to a valid transformer model package directory.
* **Resolution**:
  * Ensure `saved_model` directory exists under `model/` and contains `config.json` and weight files.
  * Verify `MODEL_DIR` in `backend/.env` is set correctly (e.g. `../model/saved_model` or absolute path).

### 3. Database Connection Failures
* **Cause**: SQLite database path is invalid or lacks directory creation permissions.
* **Resolution**:
  * Make sure the backend process has write permissions for the directory containing the SQLite db file.
