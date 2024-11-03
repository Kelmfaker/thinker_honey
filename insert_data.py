import sqlite3

def insert_data():
    conn = sqlite3.connect('shopping_cart.db')
    cursor = conn.cursor()

    products = [
        ("عسل الدغموس", 50.0, "عسل الدغموس يُعتبر من العسل الطبيعي الذي يُستخرج من زهور الدغموس، وهو يتميز بلونه الأحمر الغني بالمواد العضوية والمغذية.", "img/prd-img/A.jpg"),
        ("عسل السدر", 70.0, "عسل السدر يُستخرج من زهور شجرة السدر، وهو معروف بفوائده الصحية العديدة.", "img/prd-img/B.jpg"),
        ("عسل الزعتر", 60.0, "عسل الزعتر يُستخرج من زهور الزعتر، ويتميز بنكهته الفريدة وفوائده الصحية.", "img/prd-img/C.jpg")
    ]

    cursor.executemany('INSERT INTO products (name, price, description, image) VALUES (?, ?, ?, ?)', products)
    conn.commit()
    conn.close()

insert_data()
