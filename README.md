# Penny Wise 🦉💰

Penny Wise is an AI-powered grocery tracking application that helps you monitor your spending and track price changes over time. By simply uploading a photo of your receipt, Penny Wise uses the **Gemini API** to extract item details, prices, and quantities, storing them in your choice of database (SQLite or MongoDB) for long-term analytics.

## ✨ Features

- **User Authentication**: Secure register and login system with JWT tokens.
- **Automated Receipt Extraction**: Powered by Gemini API for high-accuracy OCR and data structuring.
- **Price History Tracking**: Monitor how the prices of your favorite items change over months, specific to your user account.
- **Database Agnostic**: Easily swap between **SQLite** and **MongoDB** via configuration.
- **FastAPI Backend**: High-performance API for fast processing and extensibility.

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLModel (SQLAlchemy)
- **Database**: SQLite (default) or MongoDB (via Motor)
- **AI**: Gemini API (`google-genai`)
- **Authentication**: JWT, Passlib (PBKDF2)
- **Package Management**: [uv](https://github.com/astral-sh/uv)

## 🚀 Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed.
- A Gemini API Key (Get one at [Google AI Studio](https://aistudio.google.com/)).

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd penny-wise
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   GEMINI_API_KEY=your_api_key_here
   SECRET_KEY=your_random_secret_key_for_jwt
   
   # Database Configuration
   DATABASE_TYPE=sqlite  # Options: sqlite, mongodb
   
   # Required only if using MongoDB
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=pennywise
   ```

3. **Install Dependencies**:
   ```bash
   uv sync
   ```

### Running the App

Start the FastAPI server using `uv`:

```bash
# Standard run
uv run python -m app.main

# Development mode with hot-reload
uv run uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` in your browser to access the interactive API documentation (Swagger UI).

### 🐳 Running with Docker

1. **Build the image**:
   ```bash
   docker build -t penny-wise .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 --env-file .env penny-wise
   ```

## 📁 Project Structure

```text
penny-wise/
├── app/
│   ├── main.py              # FastAPI entry point & routes
│   ├── models.py            # Database models (SQLModel)
│   ├── schemas.py           # Pydantic validation schemas
│   ├── database.py          # DB connection management (SQL/NoSQL)
│   ├── auth.py              # JWT and Password logic
│   ├── repositories/        # Database abstraction layer
│   │   ├── base.py          # Repository Interface
│   │   ├── sql_repository.py # SQLite Implementation
│   │   └── mongodb_repository.py # MongoDB Implementation
│   └── services/
│       └── gemini_service.py # Gemini API integration
├── pyproject.toml           # Project dependencies
└── database.db              # Local SQLite database (auto-generated)
```

## 📊 Analytics

You can check the price history of any item via the API:
`GET /price-history/{item_name}`

Example: `http://127.0.0.1:8000/price-history/Milk`

---
*Penny Wise - Stop guessing, start tracking.*
