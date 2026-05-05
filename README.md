# Pravin Enterprises - Hardware Store E-Commerce Platform

A complete Python Django-based e-commerce platform for an online hardware store.

## Features

### ✨ Core Features
- **User Authentication**: Registration and login with password hashing
- **Product Management**: Browse, search, filter, and view detailed product information
- **Shopping Cart**: Add/remove items, update quantities
- **Checkout Process**: Multi-step checkout with address management
- **Direct Order Placement**: Place orders without an online payment step
- **Order Management**: Real-time order tracking and status updates
- **Invoice Generation**: Automatic PDF invoice generation
- **WhatsApp Notifications**: Real-time order notifications via Twilio WhatsApp API
- **Admin Panel**: Full admin dashboard for inventory and order management

### 🔐 Security Features
- Password hashing and encryption
- CSRF protection
- Immediate invoice generation
- Session management
- Input validation and sanitization

### 📱 Responsive Design
- Mobile-friendly interface
- Optimized for all devices
- Bootstrap 5 framework

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual Environment

### Step 1: Clone or Download the Project

```bash
cd "d:\Pravin\pravin python\pravin_enterprises"
```

### Step 2: Create Virtual Environment

You can use the provided helper script to automate setup and startup on Windows.

```bat
start.bat
```

This script will:
- create `venv` if needed
- install dependencies only when missing
- copy `.env.example` to `.env` if no `.env` exists
- run `python manage.py migrate`
- start the development server

If you prefer to run setup manually, use:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your credentials
# - Twilio credentials
# - Email configuration
# - Database settings
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create:
- Username
- Email
- Password

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

---

## Usage

### Customer Features

1. **Register & Login**
   - Create account with name, email, and phone
   - Secure login with email

2. **Browse Products**
   - Search products by name
   - Filter by category, price range
   - Sort by newest, price, rating

3. **Shopping Cart**
   - Add products to cart
   - Update quantities
   - View price summary

4. **Checkout**
   - Enter shipping address
   - Add billing address
   - Place order

5. **Order Confirmation**
   - Order is placed immediately
   - Invoice is generated automatically
   - Admin receives WhatsApp notification

6. **Order Tracking**
   - View order status
   - Track shipment
   - Download invoice

### Admin Features

1. **Access Admin Panel**
   - Go to `http://127.0.0.1:8000/admin/`
   - Login with superuser credentials

2. **Product Management**
   - Add new products
   - Edit product details
   - Update prices and stock
   - Add product images

3. **Order Management**
   - View all orders
   - Update order status
   - View customer details
   - Track shipments

4. **User Management**
   - View customer profiles
   - Manage user data
   - View addresses

5. **Inventory**
   - Check stock levels
   - Low stock alerts
   - Popular products report

---

## API Endpoints

### Products
- `GET /products/` - List all products
- `GET /product/<slug>/` - Product details
- `GET /category/<slug>/` - Products by category

### Cart
- `POST /cart/add/<product_id>/` - Add to cart
- `GET /cart/` - View cart
- `POST /cart/update/<item_id>/` - Update item
- `POST /cart/remove/<item_id>/` - Remove item

### Orders
- `POST /orders/checkout/` - Create order
- `GET /orders/list/` - Order history
- `GET /orders/<order_id>/` - Order details

### Accounts
- `POST /accounts/register/` - Register
- `POST /accounts/login/` - Login
- `GET /accounts/profile/` - User profile
- `GET /accounts/dashboard/` - Dashboard

### Invoices
- `GET /payments/invoice/<order_id>/download/` - Download invoice PDF

---

## Configuration

### Invoice Template Setup

Admins can edit invoice text from **Admin Panel > Invoices > Invoice templates**.
Only one template should be active; new invoices use the active template.

### WhatsApp Notifications (Twilio)

1. Create account at https://www.twilio.com/
2. Get Account SID and Auth Token
3. Create WhatsApp Sandbox
4. Add to .env file:
   ```
   TWILIO_ACCOUNT_SID=your_sid_here
   TWILIO_AUTH_TOKEN=your_token_here
   OWNER_WHATSAPP_NUMBER=whatsapp:+91XXXXXXXXXX
   ```

### Email Configuration

1. Create Gmail App Password
2. Add to .env file:
   ```
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   ```

---

## Database Models

### Users
- `User` - Django built-in user model
- `UserProfile` - Extended user information
- `Address` - User addresses

### Products
- `Category` - Product categories
- `Product` - Product information
- `ProductReview` - Customer reviews

### Orders & Invoices
- `Cart` - Shopping cart
- `CartItem` - Cart items
- `Order` - Order information
- `OrderItem` - Items in order
- `Invoice` - Generated invoices
- `InvoiceTemplate` - Admin-editable invoice PDF text

---

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Activate virtual environment and install requirements
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

---

## Production Deployment

### Steps for Deployment

1. Set DEBUG = False in settings.py
2. Configure ALLOWED_HOSTS
3. Use PostgreSQL instead of SQLite
4. Set SECURE_SSL_REDIRECT = True
5. Use environment variables for sensitive data
6. Set up Gunicorn WSGI server
7. Configure Nginx as reverse proxy
8. Set up SSL certificate

### Deployment Checklist
- [ ] Update SECRET_KEY
- [ ] Set DEBUG = False
- [ ] Configure database
- [ ] Set ALLOWED_HOSTS
- [ ] Configure email backend
- [ ] Configure WhatsApp
- [ ] Set up SSL/HTTPS
- [ ] Run migrations
- [ ] Collect static files
- [ ] Set up backup strategy

---

## Support & Documentation

For more information, visit:
- Django Documentation: https://docs.djangoproject.com/
- Twilio API: https://www.twilio.com/docs/
- Bootstrap: https://getbootstrap.com/docs/

---

## License

This project is proprietary software for Pravin Enterprises.

---

## Contact

- **Email**: info@pravinenterprises.com
- **Phone**: +91-XXXXXXXXXX
- **Website**: https://www.pravinenterprises.com

---

**Version**: 1.0.0  
**Last Updated**: March 2026
