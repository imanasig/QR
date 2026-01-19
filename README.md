# Membership QR System

A complete membership management system with QR code generation, logo overlay, and public profile pages.

## Features

✅ **Admin Dashboard**
- Register new members
- View all members
- Auto-generate unique membership IDs

✅ **QR Code Generation**
- Automatic QR code creation
- Logo overlay on QR codes (centered, scannable)
- High error correction for reliable scanning

✅ **Public Profiles**
- Scan QR → Instant profile view
- Displays: Name, Contact, Blood Group
- Mobile-friendly design

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Your Logo

Place your logo image at `static/logo.png` (PNG format recommended, square image works best)

If you don't have a logo yet, the system will work without it - QR codes will be generated without overlay.

### 3. Run the Application

```bash
python app.py
```

The server will start at `http://localhost:5000`

## Usage

### For Admins:

1. **Access Dashboard**: Open `http://localhost:5000`
2. **Register Member**: Click "Register New Member"
3. **Enter Details**: Name, Contact Number, Blood Group
4. **Get QR Code**: System generates unique ID and QR code
5. **Download/Print**: Save the QR code for member cards

### For Members:

1. **Scan QR Code**: Use any smartphone camera
2. **View Profile**: Automatically redirected to profile page
3. **Share Contact**: Contact number is clickable (tel: link)

## Database

- Uses SQLite (file: `members.db`)
- Auto-created on first run
- Stores: Member ID, Name, Contact, Blood Group, Registration Date

## QR Code Details

- **Error Correction**: High (30% of code can be damaged/covered)
- **Logo Size**: 1/5 of QR code (allows logo without breaking scan)
- **Format**: PNG image
- **Scannable**: Works with all standard QR readers

## Customization

### Change Logo Size

Edit `app.py`, line ~60:
```python
logo_size = qr_width // 5  # Change 5 to 4 for bigger logo, 6 for smaller
```

### Change Color Scheme

Edit `templates/base.html`, modify gradient colors:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add More Fields

1. Update database schema in `init_db()` function
2. Add form fields in `register.html`
3. Update `register()` route to save new fields
4. Display in `public_profile.html`

## File Structure

```
QR_Generator/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── members.db                  # SQLite database (auto-created)
├── static/
│   └── logo.png               # Your logo (add this)
└── templates/
    ├── base.html              # Base template with styling
    ├── index.html             # Admin dashboard
    ├── register.html          # Registration form
    ├── member_details.html    # Member details + QR display
    └── public_profile.html    # Public profile (scanned view)
```

## Production Deployment

Before deploying to production:

1. **Change Secret Key** in `app.py`:
   ```python
   app.config['SECRET_KEY'] = 'your-random-secret-key-here'
   ```

2. **Disable Debug Mode** in `app.py`:
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

3. **Use Production Server**: Deploy with Gunicorn, uWSGI, or similar

4. **Add HTTPS**: Use SSL certificate for secure connections

5. **Database Backup**: Regularly backup `members.db`

## Use Cases

- Medical ID cards
- Gym memberships
- NGO volunteer cards
- Blood bank donor registry
- Event attendee badges
- Club memberships
- Employee ID cards

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **QR Generation**: qrcode library with Pillow
- **Frontend**: HTML5, CSS3 (no external frameworks)

## Support

For issues or questions, check that:
- Python 3.7+ is installed
- All dependencies are installed (`pip install -r requirements.txt`)
- Port 5000 is not in use
- You have write permissions in the directory (for database creation)

---

**Built with ❤️ for simple, effective membership management**
