from flask import render_template, request, redirect, url_for, session, jsonify
from app import app
from models import get_categories, get_services_by_category, add_to_cart, remove_from_cart, extract_price

@app.route('/')
def index():
    categories = get_categories()
    return render_template('index.html', categories=categories)

@app.route('/category/<category_name>')
def category(category_name):
    services = get_services_by_category(category_name)
    return render_template('category.html', services=services, category_name=category_name)

@app.route('/add_to_cart/<int:service_id>', methods=['POST'])
def add_to_cart_route(service_id):
    add_to_cart(service_id)
    return jsonify({"message": "Услуга добавлена в корзину!"})

@app.route('/remove_from_cart/<int:unique_id>', methods=['POST'])
def remove_from_cart_route(unique_id):
    remove_from_cart(unique_id)
    cart_items = session.get('cart', [])
    total_price = sum(extract_price(item['price']) for item in cart_items)
    return jsonify({"message": "Услуга удалена из корзины!", "total_price": total_price, "cart_items": cart_items})

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total_price = sum(extract_price(item['price']) for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))
