<<<<<<< HEAD
# Food Quality Detection System

A web application for analyzing food quality through image upload with user authentication and history tracking.

## Features

- User login system (default: username=root, password=root)
- Image upload with drag-and-drop support
- Food quality analysis with mock AI predictions
- Temperature and humidity simulation
- Analysis history tracking
- Responsive web design

## Setup Instructions

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and go to: http://localhost:5000

4. Login with:
   - Username: root
   - Password: root

## Database

The application uses SQLite database (food_quality.db) which is automatically created on first run.

## File Structure

```
finalfood/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── food_quality.db       # SQLite database (auto-created)
├── templates/
│   ├── login.html        # Login page
│   ├── dashboard.html    # Main dashboard
│   └── history.html      # Analysis history
└── static/
    ├── css/
    │   └── style.css     # Stylesheet
    ├── js/
    │   └── script.js     # JavaScript functionality
    └── uploads/          # Uploaded images storage
```

## Usage

1. Login with the provided credentials
2. Upload a food image by clicking or dragging to the upload area
3. Click "Analyze Image" to get quality predictions
4. View analysis history in the History section
5. Results include quality score, temperature, humidity, and freshness rating
=======
# DATAScience
>>>>>>> ec376c9f4377c59512229fe40bd2edba4c31fbfb
