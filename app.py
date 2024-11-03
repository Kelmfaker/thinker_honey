from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_folder='static')

if __name__ == '__main__':
    init_db()
    insert_data()
    app.run(debug=True, host='0.0.0.0', port=5000)

def init_db():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS cart')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT, image TEXT, quantity INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS cart
                      (id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER)''')
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()

    products = [
        ("عسل الدغموس", 50.0, "عسل الدغموس يُعتبر من العسل الطبيعي الذي يُستخرج من زهور الدغموس، وهو يتميز بلونه الأحمر الغني بالمواد العضوية والمغذية.", "../static/img/prd-img/A.jpg", 10),
        ("عسل السدر", 70.0, "عسل السدر يُستخرج من زهور شجرة السدر، وهو معروف بفوائده الصحية العديدة.", "../static/img/prd-img/b.jpg", 15),
        ("عسل الزعتر", 60.0, "عسل الزعتر يُستخرج من زهور الزعتر، ويتميز بنكهته الفريدة وفوائده الصحية.", "../static/img/prd-img/c.jpg", 20)
    ]

    cursor.executemany('INSERT INTO products (name, price, description, image, quantity) VALUES (?, ?, ?, ?, ?)', products)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cart (product_id, quantity) VALUES (?, ?)', (product_id, quantity))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    insert_data()
    app.run(debug=True, port=5000)
