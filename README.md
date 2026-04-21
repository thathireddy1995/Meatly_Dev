# Meatly — Flask Edition

Premium meat delivery website (Licious-style), built with **Python + Flask + Tailwind (via CDN)**.

## Features
- 6 pages: Home, Products, Product Detail, Cart, About, Contact
- Search, category filter, sorting
- Server-side cart in Flask session (add / update / remove)
- Coupon `FRESH10` (10% off)
- Free delivery over ₹499 (else ₹49)
- Responsive design, premium UI

## Run locally

```bash
# 1. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
python app.py
```

Visit **http://localhost:5000** in your browser.

## Project structure
```
meatly-flask/
├── app.py              # Flask routes & cart logic
├── products.py         # Product catalogue (12 items)
├── requirements.txt
├── templates/          # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── about.html
│   ├── contact.html
│   └── 404.html
└── static/
    ├── css/styles.css
    └── images/         # Product & hero images
```

## Try it
- Add items to cart from any product card
- Go to **Cart** → apply coupon `FRESH10`
- Add ₹499+ to unlock free delivery
