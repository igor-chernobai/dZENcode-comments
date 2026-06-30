# dZENcode Comments — SPA Comment System

A full-featured SPA comment application built with Django, DRF, WebSockets, Celery, Redis, and Docker.

## Features

- Nested (threaded) comments with unlimited depth (django-mptt)
- Real-time updates with WebSocket (django-channels)
- Sorting by username, email, date (asc/desc)
- Pagination — 25 comments per page
- CAPTCHA protection on comment form
- Image upload with async resize to 320×240 with Celery
- Text file upload (TXT, max 100kb)
- Allowed HTML tags in comments: `<a>`, `<code>`, `<i>`, `<strong>`
- XSS protection with bleach
- Redis caching with automatic invalidation on new comment
- JWT authentication
- LIFO ordering by default

## Stack

- **Backend:** Python 3.13, Django 6, Django REST Framework
- **Async:** Django Channels, Daphne / Gunicorn + Uvicorn worker
- **Queue:** Celery + Redis
- **Database:** PostgreSQL 16
- **Cache/Broker:** Redis 7
- **Frontend:** Vanilla JS (single HTML file, no build step)
- **Infrastructure:** Docker, Docker Compose, Nginx

## Quick Start

### Requirements

- Docker
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/dZENcode-comments.git
cd dZENcode-comments
```

### 2. Create `.env` file

```bash
cp .env.example .env
```

### 3. Run with Docker Compose

**Development:**
```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Open `http://localhost:8000/`

### 4. Load sample data (optional)

```bash
docker compose exec web python manage.py loaddata fixtures/comments.json
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/comments/` | List comments (supports `?ordering=` and `?page=`) |
| POST | `/api/comments/` | Create a comment |
| GET | `/api/captcha/` | Get CAPTCHA image and key |
| WS | `/ws/comments/` | WebSocket for real-time updates |

### Sorting examples

```
GET /api/comments/?ordering=username        # A→Z by username
GET /api/comments/?ordering=-username       # Z→A by username
GET /api/comments/?ordering=email           # A→Z by email
GET /api/comments/?ordering=-created_at     # newest first (default)
```

## Project Structure

```
dZENcode-comments/
├── core/               # Django project settings, urls, asgi, celery
├── comments/           # Comments app: models, views, serializers, tasks
├── templates/          # Frontend (index.html)
├── fixtures/           # Sample data
├── nginx/              # Nginx config for production
├── compose.yaml        # Development docker-compose
├── compose.prod.yaml   # Production docker-compose
├── Dockerfile
└── requirements.txt
```

## Live Demo

http://164.92.166.86/