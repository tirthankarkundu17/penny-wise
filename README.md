# Penny Wise 🦉💰

Penny Wise is an AI-powered grocery tracking application that helps you monitor your spending and track price changes over time. By simply uploading a photo of your receipt, Penny Wise uses the **Gemini API** to extract item details, prices, and quantities, storing them in your choice of database (SQLite or MongoDB) for long-term analytics.

## ✨ Features

- **User Authentication**: Secure register and login system with JWT tokens.
- **Automated Receipt Extraction**: Powered by Gemini API for high-accuracy OCR and data structuring.
- **Advanced Price Search**: Search for any item to see its price history across different stores, now with a detailed UI showing **item names** and **descriptions**.
- **Price History Tracking**: Monitor how the prices of your favorite items change over months, specific to your user account.
- **Database Agnostic**: Easily swap between **SQLite** and **MongoDB** via configuration.
- **Modern Web Dashboard**: A premium, responsive dashboard built with React and Framer Motion.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy)
- **Database**: SQLite (default) or MongoDB (via Motor)
- **AI**: Gemini API (`google-genai`)
- **Authentication**: JWT, Passlib (PBKDF2)
- **Package Management**: [uv](https://github.com/astral-sh/uv)

### Frontend
- **Framework**: React 18 (Vite)
- **Styling**: Vanilla CSS with Glassmorphism
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **HTTP Client**: Axios

## 🚀 Getting Started

### Prerequisites

- [uv](https://github.com/astral-sh/uv) installed.
- [Node.js](https://nodejs.org/) installed.
- A Gemini API Key (Get one at [Google AI Studio](https://aistudio.google.com/)).

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd penny-wise
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the `backend` directory:
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
   # Install backend dependencies
   make install-backend

   # Install frontend dependencies
   make install-frontend
   ```

### Running the App

You can run both parts of the application using the `Makefile`:

```bash
# Start backend (Development mode)
make dev-backend

# Start frontend (Development mode)
make dev-frontend
```

- Backend API: `http://127.0.0.1:8000/docs`
- Frontend Dashboard: `http://localhost:5173`

## 📁 Project Structure

```text
penny-wise/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic validation schemas
│   │   ├── db/                  # Database management
│   │   └── services/            # Gemini API integration
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components (SearchOverlay, etc.)
│   │   ├── pages/               # Dashboard and Login pages
│   │   ├── services/            # API client
│   │   └── App.jsx
│   ├── Dockerfile
│   └── package.json
├── Makefile                     # Unified project management
└── README.md
```

## 📊 Analytics & Search

The **Search Overlay** in the dashboard allows you to:
- Search for items by name (e.g., "Milk", "Bread").
- View detailed **item names** as recorded on the receipt.
- Read **item descriptions** for better context (e.g., "Full Cream", "1 Liter").
- Track price trends across different stores and dates.

---
*Penny Wise - Stop guessing, start tracking.*
