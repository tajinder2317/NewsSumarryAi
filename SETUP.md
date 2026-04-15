# Quick Setup Guide

## Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create data directory**
   ```bash
   mkdir data
   mkdir data\logs
   ```

5. **Configure environment**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` file with your settings.

6. **Start backend server**
   ```bash
   python run.py
   ```

## Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start frontend server**
   ```bash
   npm start
   ```

## Test the Application

1. Backend API will be available at: http://localhost:8000
2. API Documentation: http://localhost:8000/docs
3. Frontend Application: http://localhost:3000

## First Steps

1. Click "Collect News" on the home page to gather articles
2. View the dashboard for statistics and trends
3. Use the search page to find specific articles
4. Try the analysis page to perform AI-powered analysis

## Troubleshooting

- **Backend won't start**: Ensure all dependencies are installed and port 8000 is available
- **Frontend won't start**: Ensure Node.js 14+ is installed and port 3000 is available
- **No articles collected**: Check RSS feed URLs and internet connection
- **Analysis fails**: Ensure articles have been collected first
