import sqlite3
import re
from flask import session

DATABASE = 'data/services.db'

def get_categories():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM services")
        categories = cursor.fetchall()
    return [cat[0] for cat in categories]

def get_services_by_category(category):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE category = ?", (category,))
        services = cursor.fetchall()
    return services

def add_to_cart(service_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE id = ?", (service_id,))
        service = cursor.fetchone()
    if service:
        cart = session.get('cart', [])
        cart.append({'id': service[0], 'name': service[2], 'price': service[3], 'unique_id': len(cart)})
        session['cart'] = cart

def remove_from_cart(unique_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['unique_id'] != unique_id]
    session['cart'] = cart

def extract_price(price_str):
    price_str = re.sub(r'[^0-9 ]', '', price_str)
    return float(price_str.replace(' ', ''))
