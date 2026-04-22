# News Analyzer AI

AI-powered news collection + analysis with a FastAPI backend and a React (MUI) frontend. Designed to run locally, or deploy on Vercel (frontend + backend) with a real database for persistent articles.

## Live

- Frontend: `https://news-sumarry-ai.vercel.app`
- Backend: `https://news-sumarry-ai-backend.vercel.app`
- Backend API docs: `https://news-sumarry-ai-backend.vercel.app/docs`

## What You Get

- Global RSS coverage (Asia, Europe, Americas, Middle East, Africa) + on-demand collection
- Article storage in a database (SQLite locally, Postgres in production)
- Sentiment + lightweight NLP analysis per article
- “Fresh” feed (last 5 minutes) + time ranges: Today / Yesterday / This Week / This Month / This Year
- Server-side pagination (50 articles/page) with total counts
- Futuristic, minimal UI with Light/Dark mode toggle

## Repo Layout

```
backend/   FastAPI app + collectors + database models
frontend/  React app (MUI) consuming the API
```

## Quick Start (Local)

Prereqs:
- Python `3.12+`
- Node.js `18+`

Backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 run.py
```

Frontend:

```bash
cd frontend
npm install
npm start
```

Defaults:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000` (docs at `http://localhost:8000/docs`)

## Environment Variables

Backend (`backend/.env`):

```env
# Local dev (SQLite)
DATABASE_URL=sqlite:///./data/database.db

# Production (Postgres)
# DATABASE_URL=postgresql://...
# POSTGRES_PRISMA_URL=postgresql://...   # common Vercel naming

LOG_LEVEL=INFO
```

Frontend (`frontend/.env`):

```env
# If deployed separately, point to backend URL.
REACT_APP_API_URL=http://localhost:8000
```

Notes:
- In production on Vercel, set `DATABASE_URL` (or `POSTGRES_PRISMA_URL`) on the backend project.
- If frontend + backend are deployed as separate projects, set `REACT_APP_API_URL` on the frontend project.

## API Highlights

News:
- `POST /api/v1/news/collect` Collect latest articles from configured feeds
- `GET /api/v1/news/latest?minutes=5&refresh=true` Fresh feed (optionally triggers a lightweight refresh)
- `GET /api/v1/news/paged?page=1&page_size=50&date_from=...&date_to=...` Paged news with total counts
- `GET /api/v1/news/stats/summary` High-level counts and distribution

Trends:
- `GET /api/v1/trends/topics?hours=24` Trending topics window

## Vercel Deploy

Deploy backend:

```bash
cd backend
vercel --prod
```

Deploy frontend:

```bash
cd frontend
vercel --prod
```

Recommended:
- Use Vercel Postgres (or any Postgres provider) and set `DATABASE_URL` (and/or `POSTGRES_PRISMA_URL`) on the backend project.

## Performance Tips

- Use `GET /api/v1/news/paged` for the main feed (it avoids downloading huge lists).
- Keep collection small per source in serverless (the collector is tuned for short timeouts).
- If you need “always-fresh” updates, schedule a cron job to hit `POST /api/v1/news/collect` every few minutes (Vercel Cron or external).

## Troubleshooting

- Frontend can’t reach backend:
  - Set `REACT_APP_API_URL` on the frontend Vercel project to your backend URL.
- Backend returns `503 Database unavailable`:
  - Set `DATABASE_URL` (or `POSTGRES_PRISMA_URL`) on the backend Vercel project and redeploy.
- “Today” looks off:
  - Time-range filters are computed in the browser (local time) and sent as ISO datetimes to the backend.

## License

MIT
