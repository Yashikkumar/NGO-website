from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# Initialize Flask, pointing it to your 'public' folder
app = Flask(__name__, static_folder='public', static_url_path='')

# --- GOOGLE SHEETS CONNECTION ---
def get_sheet():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # This will securely read from credentials.json
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        return client.open('EktaMission_Contacts').sheet1
    except Exception as e:
        print(f"Error connecting to Sheets: {e}")
        return None

# --- ROUTES ---
@app.route('/')
def home():
    # Show your exact index.html design
    return app.send_static_file('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    sheet = get_sheet()
    
    if sheet and name and email and message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            sheet.append_row([timestamp, name, email, message])
            success = True
        except:
            success = False
    else:
        success = False

    # A clean success screen that matches your website's colors
    if success:
        return f"""
            <div style="text-align: center; font-family: 'Poppins', sans-serif; margin-top: 100px;">
                <h1 style="color: green;">Thank you, {name}!</h1>
                <p>Your message has been safely delivered to Ekta Mission.</p>
                <br>
                <a href="/" style="padding: 10px 20px; background: orange; color: black; text-decoration: none; border-radius: 5px; font-weight: bold;">Return to Home Page</a>
            </div>
        """
    else:
        return f"""
            <div style="text-align: center; font-family: 'Poppins', sans-serif; margin-top: 100px;">
                <h1 style="color: red;">Oops! Something went wrong.</h1>
                <p>We couldn't send your message. Please try again later.</p>
                <br>
                <a href="/" style="padding: 10px 20px; background: black; color: white; text-decoration: none; border-radius: 5px;">Go Back</a>
            </div>
        """

# This is required for Render to run the app
if __name__ == '__main__':
    app.run(port=3000, debug=True)