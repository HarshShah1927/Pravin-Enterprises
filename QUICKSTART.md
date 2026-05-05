# PRAVIN ENTERPRISES - QUICK START GUIDE

## 🚀 Complete Setup Instructions

### Step 1: Initial Setup (First Time Only)

```bash
# Navigate to project directory
cd "d:\Pravin\pravin python\pravin_enterprises"
```

Then run the helper script on Windows:

```bat
start.bat
```

This will create the virtual environment, install dependencies if needed, copy `.env.example` to `.env` when missing, apply migrations, and start the development server.

If you want to run the setup steps manually instead, continue with:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

```bash
# Copy example env file
copy .env.example .env

# Edit .env file and add:
# - Twilio credentials (from https://www.twilio.com/console)
# - Email configuration (for order notifications)
```

### Step 3: Initialize Database

```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Follow prompts to create username, email, and password

# (Optional) Load sample products
python manage.py load_sample_products
```

### Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

---

## 📱 Default URLs

### Customer Pages
- **Home**: http://127.0.0.1:8000/
- **Products**: http://127.0.0.1:8000/products/
- **Cart**: http://127.0.0.1:8000/cart/
- **Register**: http://127.0.0.1:8000/accounts/register/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Dashboard**: http://127.0.0.1:8000/accounts/dashboard/

### Admin Panel
- **Admin**: http://127.0.0.1:8000/admin/
- **Login with superuser credentials**

---

## Invoice Setup

Admins can change invoice PDF text from **Admin Panel > Invoices > Invoice templates**.
New orders generate an invoice immediately using the active template.

---

## 💬 WhatsApp Notifications Setup

### Twilio Configuration

1. Go to https://www.twilio.com/
2. Create account
3. Get Account SID and Auth Token
4. Set up WhatsApp Sandbox
5. Add to .env:
   ```
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   OWNER_WHATSAPP_NUMBER=whatsapp:+91XXXXXXXXXX
   ```

---

## 📧 Email Configuration

### Gmail Setup

1. Enable 2-Factor Authentication on Gmail
2. Create App Password: https://myaccount.google.com/apppasswords
3. Add to .env:
   ```
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

---

## 📊 Admin Panel Features

### Access Admin
```
http://127.0.0.1:8000/admin/
```

### Available Sections
1. **Products**
   - Add/Edit/Delete products
   - Manage categories
   - View reviews
   - Update inventory

2. **Orders**
   - View all orders
   - Update order status
   - View customer details
   - Track shipments

3. **Users**
   - Manage user accounts
   - View profiles
   - Verify users

4. **Invoices**
   - Download invoices
   - Edit invoice templates

---

## 🧪 Testing the Application

### 1. Create Test Account
```
- Email: test@example.com
- Password: TestPass123
- Phone: +91 9999999999
```

### 2. Browse Products
- Search by name
- Filter by category
- Sort by price/rating

### 3. Add to Cart
- Add multiple items
- Update quantities
- Remove items

### 4. Checkout
- Enter shipping address
- Place the order
- Download the generated invoice from the order page

### 5. Track Order
- View order status
- Download invoice
- Check order history

---

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError
```bash
# Solution: Install missing packages
pip install -r requirements.txt
```

### Issue: Migration errors
```bash
# Solution: Run migrations again
python manage.py migrate --no-input
```

### Issue: Static files not loading
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

### Issue: Port 8000 already in use
```bash
# Solution: Use different port
python manage.py runserver 8001
```

### Issue: Database locked
```bash
# Solution: Remove db.sqlite3 and migrate again
rm db.sqlite3
python manage.py migrate
```

---

## 📝 Useful Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_products

# Collect static files
python manage.py collectstatic

# Start development server
python manage.py runserver

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Create backup
python manage.py dumpdata > backup.json

# Restore backup
python manage.py loaddata backup.json
```

---

## 🔒 Security Checklist

Before going to production:

- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS/SSL certificate
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure secure session cookies
- [ ] Set up CSRF protection
- [ ] Enable security headers
- [ ] Set up regular backups
- [ ] Configure logging
- [ ] Test invoice generation

---

## 📱 Project Structure

```
pravin_enterprises/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── .env.example            # Environment variables template
│
├── pravin_enterprises/      # Main project folder
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
│
├── accounts/               # User authentication app
│   ├── models.py           # User models
│   ├── views.py            # Authentication views
│   ├── forms.py            # Authentication forms
│   └── urls.py             # URL routes
│
├── products/              # Products app
│   ├── models.py          # Product models
│   ├── views.py           # Product views
│   ├── forms.py           # Product forms
│   └── urls.py            # URL routes
│
├── cart/                  # Shopping cart app
│   ├── models.py          # Cart models
│   ├── views.py           # Cart views
│   └── urls.py            # URL routes
│
├── orders/               # Orders app
│   ├── models.py         # Order models
│   ├── views.py          # Order views
│   └── urls.py           # URL routes
│
├── payments/            # Invoices app
│   ├── models.py        # Invoice models
│   ├── views.py         # Invoice views
│   └── urls.py          # URL routes
│
├── notifications/       # Notifications app
│   ├── whatsapp.py      # WhatsApp integration
│   └── views.py         # Notification views
│
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── accounts/        # Auth templates
│   ├── products/        # Product templates
│   ├── cart/            # Cart templates
│   ├── orders/          # Order templates
│
├── static/              # Static files
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Images
│
└── media/              # User uploaded files
    ├── products/       # Product images
    └── invoices/       # Invoice PDFs
```

---

## 🎯 Key Features Implemented

✅ User Authentication & Registration
✅ Product Browsing & Search
✅ Shopping Cart Management
✅ Checkout Process
✅ Immediate Invoice Generation
✅ PDF Invoice Generation
✅ WhatsApp Order Notifications
✅ Admin Dashboard
✅ Order Tracking
✅ Responsive Design
✅ Security Features

---

## 📞 Support

For issues, questions, or contributions:
- Email: info@pravinenterprises.com
- Phone: +91-XXXXXXXXXX

---

## 📄 License

Copyright © 2026 Pravin Enterprises. All rights reserved.

---

**Version**: 1.0.0  
**Last Updated**: March 2026  
**Status**: ✅ Production Ready
