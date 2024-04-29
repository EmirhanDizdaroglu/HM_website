from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL yapılandırma ayarları
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'hm_project'

mysql = MySQL(app)

@app.route('/')
def home():
    try:
        cursor = mysql.connection.cursor()  # İmleç oluştur

        # Kategorileri al
        cursor.execute(
            "SELECT DISTINCT category.name FROM products JOIN category ON products.category_id = category.id WHERE products.is_new = TRUE"
        )
        categories = [row[0] for row in cursor.fetchall()]  # Kategorileri çek

        # Yeni ürünleri al
        cursor.execute("SELECT name, image, price FROM products WHERE is_new = TRUE")
        new_products = cursor.fetchall()  # Yeni ürünleri çek

        cursor.close()  # İmleci kapat

        # Şablonu döndür
        return render_template('index.html', categories=categories, new_products=new_products)
    except Exception as e:
        # Hata durumunda hata mesajını döndür
        return f"Error: {str(e)}", 500



@app.route('/new-products', methods=['GET'])
def get_new_products():
    cursor = mysql.connection.cursor()

    # Yeni ürünleri al
    cursor.execute("SELECT name, image, price FROM products WHERE is_new = TRUE")
    new_products = cursor.fetchall()

    cursor.close()  # İmleci kapatın

    # Yeni ürünleri JSON formatında döndür
    return jsonify([{
        'name': product[0],
        'image': product[1],
        'price': product[2]
    } for product in new_products])