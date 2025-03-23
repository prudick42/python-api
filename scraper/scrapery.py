import requests
from bs4 import BeautifulSoup
import sqlite3

DATABASE = "data/services.db"

def create_database():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                service_name TEXT,
                price TEXT,
                UNIQUE(category, service_name)
            )
        """)
        conn.commit()

def save_services(services):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        for category, service_name, price in services:
            cursor.execute("""
                INSERT INTO services (category, service_name, price)
                VALUES (?, ?, ?)
                ON CONFLICT(category, service_name) 
                DO UPDATE SET price=excluded.price
            """, (category, service_name, price))

        conn.commit()

def scrape_services():
    url = "https://стомпрактика.рф/prices/"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    services = []

    for prices_block in soup.find_all("div", class_="prices-block"):
        category_tag = prices_block.select_one(".prices-block__header__title a, .prices-block__header__title")
        if category_tag:
            category = category_tag.text.strip()
        else:
            category = "Неизвестная категория"

        for row in prices_block.select(".prices-list__row"):
            service_name_tag = row.select_one(".prices-list__column .name")
            price_tag = row.select_one(".prices-list__column_price .prices__values")

            if service_name_tag and price_tag:
                service_name = service_name_tag.text.strip()
                price = price_tag.text.strip().replace("\n", "").replace("₽", "").strip()
                services.append((category, service_name, price))

    return services

if __name__ == "__main__":
    create_database()
    services = scrape_services()
    save_services(services)
