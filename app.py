from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import qrcode
from PIL import Image
import io
import os
import secrets
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
DATABASE = os.environ.get('DATABASE_PATH', 'members.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the members table."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            blood_group TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def generate_member_id():
    """Generate a unique 8-character alphanumeric member ID."""
    while True:
        member_id = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        conn = get_db_connection()
        existing = conn.execute('SELECT id FROM members WHERE member_id = ?', (member_id,)).fetchone()
        conn.close()
        if not existing:
            return member_id

def create_qr_with_logo(data, logo_path='static/logo.png'):
    """Create a QR code with a centered logo overlay."""
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo overlay
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # Add logo if it exists
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        
        # Calculate logo size (should be about 1/5 of QR code size)
        qr_width, qr_height = qr_img.size
        logo_size = qr_width // 5
        
        # Resize logo
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Calculate position to center the logo
        logo_pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        # Paste logo onto QR code
        qr_img.paste(logo, logo_pos, logo if logo.mode == 'RGBA' else None)
    
    return qr_img

@app.route('/')
def index():
    """Admin dashboard - list all members."""
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM members ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', members=members)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new member."""
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        blood_group = request.form['blood_group']
        
        # Generate unique member ID
        member_id = generate_member_id()
        
        # Save to database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO members (member_id, name, contact, blood_group) VALUES (?, ?, ?, ?)',
            (member_id, name, contact, blood_group)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for('member_details', member_id=member_id))
    
    return render_template('register.html')

@app.route('/member/<member_id>')
def member_details(member_id):
    """Admin view - show member details with QR code."""
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM members WHERE member_id = ?', (member_id,)).fetchone()
    conn.close()
    
    if member is None:
        return "Member not found", 404
    
    return render_template('member_details.html', member=member)

@app.route('/qr/<member_id>')
def generate_qr(member_id):
    """Generate and return QR code image for a member."""
    # Create the URL that the QR will point to
    profile_url = url_for('public_profile', member_id=member_id, _external=True)
    
    # Generate QR code with logo
    qr_img = create_qr_with_logo(profile_url)
    
    # Save to bytes
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/profile/<member_id>')
def public_profile(member_id):
    """Public profile page - what users see when they scan the QR code."""
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM members WHERE member_id = ?', (member_id,)).fetchone()
    conn.close()
    
    if member is None:
        return "Member not found", 404
    
    return render_template('public_profile.html', member=member)

if __name__ == '__main__':
    init_db()
    # Create static directory if it doesn't exist
    
    # Get port from environment variable (for deployment) or use 5001 for local development
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port
    app.run(debug=True, host='0.0.0.0', port=5001)
