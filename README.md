# AI Chicken Farming Application

A comprehensive AI-powered application for managing chicken farms with predictive analytics for health monitoring, production forecasting, and feed optimization.

## Features

- **Chicken Management**: Add, edit, and track individual chickens with details like breed, age, and health status
- **Egg Production Tracking**: Monitor and analyze egg production patterns
- **Health Monitoring**: Track health records and identify potential issues
- **Feed Scheduling**: Optimize feeding schedules for better productivity
- **AI-Powered Insights**: 
  - Health risk prediction using machine learning
  - Production forecasting based on chicken characteristics
  - Feed optimization recommendations
- **Dashboard**: Visualize key metrics and AI insights
- **Responsive UI**: Modern, user-friendly interface with friendly colors

## Deployment on Vercel

### Prerequisites

- A Vercel account (sign up at [vercel.com](https://vercel.com))

### Deployment Steps

1. Fork or clone this repository to your GitHub account
2. Sign in to your Vercel account
3. Click "New Project" and import your forked repository
4. Vercel will automatically detect this is a Python/Flask application
5. Make sure the following settings are configured:
   - Framework Preset: None (or Python)
   - Root Directory: Select the root of your project
6. Deploy the project

### Configuration

The project includes:
- `vercel.json` - Vercel configuration file
- `requirements.txt` - Python dependencies
- `api/index.py` - Main Flask application
- `models/` - Database and AI model implementations
- `templates/index.html` - Frontend interface

### Environment Notes

> **Note**: This application uses SQLite as its database, which is file-based. For production use, consider switching to a more robust database solution. The application will create the database file automatically on first run.

## Local Development

To run this application locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the development server: `python main.py`
4. Visit `http://localhost:5000` in your browser

## Architecture

- **Backend**: Flask API with SQLite database
- **AI Models**: Scikit-learn based models for health prediction, production forecasting, and feed optimization
- **Frontend**: HTML/CSS/JavaScript with Bootstrap and Chart.js
- **Database**: SQLite for storing chicken data, health records, and production metrics

## Technologies Used

- Python
- Flask
- Scikit-learn
- SQLite
- HTML/CSS/JavaScript
- Bootstrap
- Chart.js
- Pandas
- NumPy