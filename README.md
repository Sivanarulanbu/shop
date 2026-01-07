# Swiftbuy E-commerce Platform 🛍️

A modern, full-featured e-commerce solution built with Django, offering a premium shopping experience with automated logistics and professional communication.

---

## 🚀 Live System Status
The platform is **Fully Operational** and feature-complete.

- **Primary URL:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Gateway:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## ✨ Premium Features

### 🛒 Shopping Experience
- **Advanced Product Catalog:** Search and filter by category, brand, price, and featured status.
- **Dynamic Cart System:** Real-time updates with quantity management and persistent sessions.
- **Seamless Checkout:** Streamlined order placement with multi-address support.
- **Live Order Tracking:** Real-time visual progress from confirmation to delivery.

### 📧 Intelligent Communications
- **Professional Email Lifecycle:** Branded HTML notifications for registration, order confirmation, and shipment.
- **Automated Invoices:** High-quality PDF invoices generated using `xhtml2pdf` and automatically attached to delivery emails.
- **Smart Alerts:** Real-time low-stock notifications and failed payment warnings.

### 🛠️ Robust Management
- **Integrated Admin Dashboard:** A custom, high-visibility dashboard for tracking sales, inventory alerts, and best-selling products.
- **Order Logistics:** Dedicated views for managing tracking numbers, delivery partners, and shipment statuses.
- **User Management:** Full RBAC (Role-Based Access Control) for customers and staff.

---

## 🛠️ Technical Stack

- **Backend:** Python 3.x / Django 5.x
- **Database:** PostgreSQL (Production-ready)
- **Frontend:** HTML5, CSS3, Vanilla Javascript, Bootstrap 5
- **PDF Engine:** xhtml2pdf / ReportLab
- **Communication:** SMTP / Gmail Integration
- **Styling:** Premium Custom CSS with Swiftbuy branding

---

## 🔐 Administration

**Admin Access:**
- **URL:** `/admin/`
- **Username:** `admin`
- **Password:** `admin123`
- **Permissions:** Full system superuser access.

---

## 📂 Project Structure

- `shop/`: Main e-commerce logic (Products, Orders, Tracking, Signals)
- `accounts/`: User authentication and profile management
- `ecommerce/`: Project configuration and settings
- `static/` & `media/`: Asset management for professional branding

---

## 🎯 Getting Started

1. **Environment Setup:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Database Initialization:**
   ```bash
   python manage.py migrate
   ```
3. **Launch Server:**
   ```bash
   python manage.py runserver
   ```

---

&copy; 2026 Swiftbuy. *Engineered for Excellence.*
