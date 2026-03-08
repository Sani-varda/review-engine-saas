# The Review Engine

A production-grade Reputation Management SaaS built for small businesses.

## Overview

The Review Engine automates the process of collecting customer reviews and managing business reputation. It features a "Review Gating" mechanism that encourages happy customers to post public reviews while keeping negative feedback private.

## Features

- **Review Gating:** Intelligent routing based on star rating.
- **Messaging Service:** Integrated with Twilio and Resend for SMS/Email outreach.
- **Analytics Dashboard:** Track ratings, response rates, and customer sentiment.
- **Subscription Management:** Built-in Stripe integration for tiered access.
- **Owner Alerts:** Real-time notifications for low-rating feedback.

## Project Structure

- `src/backend`: FastAPI application with PostgreSQL/SQLite.
- `src/frontend`: Next.js dashboard and review landing pages.
- `infra/docker`: Containerization and deployment configuration.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local dev)
- Node.js 20+ (for local dev)

### Installation
1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in your keys.
3. Run `docker-compose up --build`.

## API Documentation

The backend provides a Swagger UI at `/docs`.

- `POST /auth/register`: Create a new business account.
- `GET /reviews/stats`: Get overview stats for the dashboard.
- `POST /reviews/request`: Send a review request to a customer.

## License

Proprietary - Developed by MoonLIT Arc.
