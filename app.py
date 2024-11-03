from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password, is_admin):
        self.id = id
        self.username = username
        self.password = password
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('shopping_cart.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            user_obj = User(user[0], user[1], user[2], user[3])
            login_user(user_obj)
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin.html')

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']
    image = request.form['image']
    quantity = request.form['quantity']
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, description, image, quantity) VALUES (?, ?, ?, ?, ?)', (name, price, description, image, quantity))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

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

@app.route('/')
def index():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

def init_db():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS products')
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT, image TEXT, quantity INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY, username TEXT, password TEXT, is_admin BOOLEAN)''')
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()
    products = [
        ("عسل الدغموس", 50.0, "عسل الدغموس يُعتبر من العسل الطبيعي الذي يُستخرج من زهور الدغموس، وهو يتميز بلونه الأحمر الغني بالمواد العضوية والمغذية.", "../static/img/prd-img/A.jpg", 10),
        ("عسل السدر", 70.0, "عسل السدر يُستخرج من زهور شجرة السدر، وهو معروف بفوائده الصحية العديدة.", "../static/img/prd-img/B.jpg", 15),
        ("عسل الزعتر", 60.0, "عسل الزعتر يُستخرج من زهور الزعتر، ويتميز بنكهته الفريدة وفوائده الصحية.", "../static/img/prd-img/C.jpg", 20)
    ]

    cursor.executemany('INSERT INTO products (name, price, description, image, quantity) VALUES (?, ?, ?, ?, ?)', products)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    insert_data()
    app.run(debug=True, port=5000)
