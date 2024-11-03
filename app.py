import sqlite3

def init_db():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT, image TEXT, quantity INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart
                      (id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER)''')
    conn.commit()
    conn.close()

def clear_data():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products')
    cursor.execute('DELETE FROM cart')
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()

    products = [
        ("عسل الدغموس", 50.0, "عسل الدغموس يُعتبر من العسل الطبيعي الذي يُستخرج من زهور الدغموس، وهو يتميز بلونه الأحمر الغني بالمواد العضوية والمغذية.", "img/prd-img/A.jpg", 10),
        ("عسل السدر", 70.0, "عسل السدر يُستخرج من زهور شجرة السدر، وهو معروف بفوائده الصحية العديدة.", "img/prd-img/B.jpg", 15),
        ("عسل الزعتر", 60.0, "عسل الزعتر يُستخرج من زهور الزعتر، ويتميز بنكهته الفريدة وفوائده الصحية.", "img/prd-img/C.jpg", 20)
    ]

    cursor.executemany('INSERT INTO products (name, price, description, image, quantity) VALUES (?, ?, ?, ?, ?)', products)
    conn.commit()
    conn.close()

# إنشاء قاعدة البيانات والجداول
init_db()

# مسح البيانات القديمة
clear_data()

# إدخال البيانات الجديدة
insert_data()
