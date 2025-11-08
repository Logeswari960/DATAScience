from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename
from PIL import Image
import random
from datetime import datetime
from iot_sensors import connect_to_device

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize IoT sensors
iot_sensors = connect_to_device()

# Database setup
def init_db():
    conn = sqlite3.connect('food_quality.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    # Analysis history table
    c.execute('''CREATE TABLE IF NOT EXISTS analysis_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  filename TEXT NOT NULL,
                  quality_score REAL,
                  temperature REAL,
                  humidity REAL,
                  freshness TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Insert default user
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('root', 'root'))
    conn.commit()
    conn.close()

# Food image analysis with IoT sensor data
def analyze_food_image(image_path):
    # Get real-time IoT sensor data
    sensor_data = iot_sensors.get_sensor_data()
    
    # Simulate food quality analysis
    quality_score = round(random.uniform(60, 95), 2)
    
    # Use IoT sensor readings
    temperature = sensor_data['temperature']
    humidity = sensor_data['humidity']
    
    # Adjust quality based on environmental conditions
    if temperature > 25 or humidity > 70:
        quality_score -= random.uniform(5, 15)
    elif temperature < 18 or humidity < 40:
        quality_score -= random.uniform(3, 10)
    
    quality_score = max(30, min(95, round(quality_score, 2)))
    
    if quality_score >= 85:
        freshness = "Fresh"
    elif quality_score >= 70:
        freshness = "Good"
    else:
        freshness = "Poor"
    
    return {
        'quality_score': quality_score,
        'temperature': temperature,
        'humidity': humidity,
        'freshness': freshness,
        'sensor_timestamp': sensor_data['timestamp']
    }

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('food_quality.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the image
        analysis = analyze_food_image(filepath)
        
        # Save to database
        conn = sqlite3.connect('food_quality.db')
        c = conn.cursor()
        c.execute("""INSERT INTO analysis_history 
                     (user_id, filename, quality_score, temperature, humidity, freshness)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (session['user_id'], filename, analysis['quality_score'],
                   analysis['temperature'], analysis['humidity'], analysis['freshness']))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'analysis': analysis
        })
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('food_quality.db')
    c = conn.cursor()
    c.execute("""SELECT filename, quality_score, temperature, humidity, freshness, timestamp
                 FROM analysis_history WHERE user_id = ? ORDER BY timestamp DESC""",
              (session['user_id'],))
    history_data = c.fetchall()
    conn.close()
    
    return render_template('history.html', history=history_data)

@app.route('/sensors')
def sensors():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('sensors.html')

@app.route('/api/sensors')
def api_sensors():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'})
    
    sensor_data = iot_sensors.get_sensor_data()
    return jsonify(sensor_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)