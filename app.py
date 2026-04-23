from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from products import PRODUCTS, CATEGORIES, get_product, related_products
from models import db, User
import os
import json

app = Flask(__name__)
app.secret_key = "meatly-dev-secret-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meatly.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

DELIVERY_FEE = 49
FREE_DELIVERY_OVER = 499
COUPONS = {"FRESH10": 0.10}


def get_cart():
    return session.setdefault("cart", {})


def save_cart():
    if current_user.is_authenticated:
        current_user.cart_data = json.dumps(get_cart())
        db.session.commit()


def cart_summary():
    cart = get_cart()
    items = []
    subtotal = 0
    savings = 0
    for pid, qty in cart.items():
        p = get_product(pid)
        if not p:
            continue
        line = p["price"] * qty
        savings += (p.get("mrp", p["price"]) - p["price"]) * qty
        subtotal += line
        items.append({**p, "qty": qty, "line_total": line})
    coupon = session.get("coupon")
    discount = int(subtotal * COUPONS[coupon]) if coupon in COUPONS else 0
    delivery = 0 if subtotal == 0 or subtotal >= FREE_DELIVERY_OVER else DELIVERY_FEE
    total = max(subtotal - discount, 0) + delivery
    return {
        "items": items,
        "subtotal": subtotal,
        "savings": savings,
        "discount": discount,
        "delivery": delivery,
        "total": total,
        "coupon": coupon,
        "count": sum(cart.values()),
    }


@app.context_processor
def inject_globals():
    return {
        "cart_count": sum(get_cart().values()),
        "categories": CATEGORIES,
        "user": current_user
    }

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "error")
            return redirect(url_for("register"))
        
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            
            # Load cart from DB
            if user.cart_data:
                try:
                    db_cart = json.loads(user.cart_data)
                    # Merge guest cart with DB cart or just replace? 
                    # Let's replace for simplicity as requested, or merge.
                    # User likely wants their saved cart back.
                    session["cart"] = db_cart
                except json.JSONDecodeError:
                    pass
            
            flash(f"Welcome back, {user.name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))
        else:
            flash("Invalid email or password", "error")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("cart", None)
    session.pop("coupon", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/")
def home():
    featured = [p for p in PRODUCTS if p.get("featured")][:6]
    return render_template("index.html", featured=featured)


@app.route("/products")
def products():
    q = request.args.get("q", "").strip().lower()
    cat = request.args.get("cat", "")
    sort = request.args.get("sort", "popular")
    items = list(PRODUCTS)
    if cat:
        items = [p for p in items if p["category"] == cat]
    if q:
        items = [p for p in items if q in p["name"].lower() or q in p["description"].lower()]
    if sort == "price-asc":
        items.sort(key=lambda p: p["price"])
    elif sort == "price-desc":
        items.sort(key=lambda p: -p["price"])
    elif sort == "rating":
        items.sort(key=lambda p: -p["rating"])
    return render_template("products.html", items=items, q=q, cat=cat, sort=sort)


@app.route("/products/<product_id>")
def product_detail(product_id):
    p = get_product(product_id)
    if not p:
        return render_template("404.html"), 404
    return render_template("product_detail.html", p=p, related=related_products(product_id))


@app.route("/cart")
def cart_view():
    return render_template("cart.html", **cart_summary())


@app.route("/cart/add/<product_id>", methods=["POST"])
def cart_add(product_id):
    p = get_product(product_id)
    if not p:
        return jsonify({"ok": False}), 404
    cart = get_cart()
    qty = int(request.form.get("qty", 1))
    cart[product_id] = cart.get(product_id, 0) + qty
    session.modified = True
    save_cart()
    flash(f"Added {p['name']} to cart", "success")
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({"ok": True, "count": sum(cart.values())})
    return redirect(request.referrer or url_for("products"))


@app.route("/cart/update/<product_id>", methods=["POST"])
def cart_update(product_id):
    cart = get_cart()
    qty = int(request.form.get("qty", 0))
    if qty <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = qty
    session.modified = True
    save_cart()
    return redirect(url_for("cart_view"))


@app.route("/cart/remove/<product_id>", methods=["POST"])
def cart_remove(product_id):
    get_cart().pop(product_id, None)
    session.modified = True
    save_cart()
    return redirect(url_for("cart_view"))


@app.route("/cart/coupon", methods=["POST"])
def cart_coupon():
    code = request.form.get("code", "").strip().upper()
    if code in COUPONS:
        session["coupon"] = code
        flash(f"Coupon {code} applied — {int(COUPONS[code]*100)}% off!", "success")
    else:
        session.pop("coupon", None)
        flash("Invalid coupon code", "error")
    return redirect(url_for("cart_view"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks! We'll get back to you within 24 hours.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
