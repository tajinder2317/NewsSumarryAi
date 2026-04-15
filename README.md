# News Analyzer AI

An AI-powered news analysis and summarization platform built with Python FastAPI backend and React frontend.

## Features

- **Real-time News Collection**: Automatically collect news from multiple RSS feeds and news APIs
- **AI-Powered Analysis**: Sentiment analysis, topic extraction, and automatic categorization
- **Trend Detection**: Identify trending topics and breaking news as they happen
- **Smart Summarization**: Get concise summaries of articles and topic clusters
- **Search & Filtering**: Advanced search capabilities with multiple filters
- **Interactive Dashboard**: Visualize trends and analytics with charts
- **Beginner-Friendly**: Clean, documented codebase with easy setup

## Technology Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (easy setup)
- **Newspaper3k** - News article extraction
- **TextBlob** - Text processing and sentiment analysis
- **Scikit-learn** - Machine learning for topic modeling
- **NLTK** - Natural language processing

### Frontend
- **React 18** - Modern UI framework
- **Material-UI** - React UI components
- **React Query** - Data fetching and caching
- **Chart.js** - Data visualization
- **Axios** - HTTP client

## Project Structure

```
NewsAnalyzerAI/
    backend/
        app/
            main.py              # FastAPI application
            config.py            # Configuration settings
            models/              # Database models and schemas
            services/            # Business logic (news collection, analysis)
            api/                 # API endpoints
            utils/               # Utility functions
        requirements.txt
        run.py
    frontend/
        src/
            components/         # React components
            pages/              # Page components
            services/           # API services
            hooks/              # Custom React hooks
            utils/              # Utility functions
        package.json
    data/
        database.db
        logs/
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Backend Setup

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

4. **Configure environment variables**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` file and configure:
   - `NEWS_API_KEY` (optional, get from https://newsapi.org/)
   - `RSS_FEEDS` (comma-separated list of RSS feed URLs)
   - Other settings as needed

5. **Create data directory**
   ```bash
   mkdir data
   mkdir data\logs
   ```

6. **Start the backend server**
   ```bash
   python run.py
   ```
   
   The API will be available at `http://localhost:8000`
   - API documentation: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the frontend development server**
   ```bash
   npm start
   ```
   
   The application will be available at `http://localhost:3000`

## Usage

### 1. Collect News
- Click "Collect News" on the home page to fetch articles from configured sources
- News is automatically analyzed for sentiment, topics, and categories

### 2. View Dashboard
- Navigate to `/dashboard` to see statistics and trending topics
- View sentiment distribution, source analysis, and recent trends

### 3. Search and Filter
- Navigate to `/search` to find specific articles
- Filter by source, category, sentiment, date range, or keywords

### 4. Analyze Articles
- Navigate to `/analysis` to perform detailed analysis
- Summarize articles, extract topics, and analyze sentiment

## API Endpoints

### News Endpoints
- `GET /api/v1/news/` - Get news articles
- `POST /api/v1/news/collect` - Collect news from sources
- `POST /api/v1/news/search` - Search news articles
- `GET /api/v1/news/stats/summary` - Get news statistics

### Analysis Endpoints
- `POST /api/v1/analysis/sentiment` - Analyze sentiment
- `POST /api/v1/analysis/topics` - Extract topics
- `POST /api/v1/analysis/summarize` - Summarize articles
- `POST /api/v1/analysis/keywords` - Extract keywords

### Trends Endpoints
- `GET /api/v1/trends/topics` - Get trending topics
- `GET /api/v1/trends/breaking` - Get breaking news
- `GET /api/v1/trends/analysis` - Get topic trends
- `GET /api/v1/trends/summary` - Get trends summary

## Configuration

### Environment Variables

#### Backend (.env)
```env
# Database
DATABASE_URL=sqlite:///./data/database.db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# News Sources
NEWS_API_KEY=your_news_api_key_here
RSS_FEEDS=https://feeds.bbci.co.uk/news/rss.xml,https://rss.cnn.com/rss/edition.rss

# Analysis Features
SENTIMENT_ANALYSIS_ENABLED=True
TOPIC_MODELING_ENABLED=True
SUMMARIZATION_ENABLED=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=./data/logs/app.log
```

#### Frontend
Create `.env` file in frontend directory:
```env
REACT_APP_API_URL=http://localhost:8000
```

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style
- Backend follows PEP 8 Python style guidelines
- Frontend uses ESLint and Prettier for consistent formatting

### Adding New Features
1. Backend: Add service in `backend/app/services/`
2. API: Add endpoints in `backend/app/api/`
3. Frontend: Add components in `frontend/src/components/`
4. Update API services in `frontend/src/services/`

## Troubleshooting

### Common Issues

1. **Backend won't start**
   - Check Python version (3.8+ required)
   - Ensure all dependencies installed: `pip install -r requirements.txt`
   - Check if port 8000 is available

2. **Frontend won't start**
   - Check Node.js version (14+ required)
   - Ensure dependencies installed: `npm install`
   - Check if port 3000 is available

3. **News collection fails**
   - Verify RSS feed URLs are accessible
   - Check internet connection
   - Ensure NewsAPI key is valid (if using NewsAPI)

4. **Database errors**
   - Ensure data directory exists
   - Check database file permissions
   - Verify DATABASE_URL in .env file

### Getting Help
- Check the logs in `data/logs/app.log`
- Review API documentation at `http://localhost:8000/docs`
- Open an issue on GitHub with detailed error information

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - JavaScript library for building UIs
- [Material-UI](https://mui.com/) - React UI component library
- [Newspaper3k](https://newspaper.readthedocs.io/) - News article extraction
- [TextBlob](https://textblob.readthedocs.io/) - Text processing library

## Roadmap

- [ ] Add user authentication and preferences
- [ ] Implement real-time WebSocket updates
- [ ] Add more visualization options
- [ ] Support for more news sources
- [ ] Mobile app development
- [ ] Advanced ML models for better analysis
- [ ] Multi-language support
