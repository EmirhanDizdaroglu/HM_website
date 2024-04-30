from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# MySQL yapılandırma ayarları
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '1234')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'hm_project')

mysql = MySQL(app)

@app.route('/')
def home():
    try:
        with mysql.connection.cursor() as cursor:
            # Kategorileri al
            cursor.execute(
                "SELECT DISTINCT category.name FROM products "
                "JOIN category ON products.category_id = category.id"
            )
            category = [row[0] for row in cursor.fetchall()]

            # Yeni ve eski ürünleri al, önce yeni ürünler sonra eski ürünler
            cursor.execute(
                "SELECT name, image, price, is_new FROM products "
                "WHERE category_id = 1 "  # Varsayılan olarak 'Kadın' kategorisi
                "ORDER BY is_new DESC "  # Yeni ürünler öncelikli
                "LIMIT 16"
            )
            products = cursor.fetchall()

        return render_template('index.html', category=category, products=products)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/new-products', methods=['GET'])
def get_new_products():
    category_id = request.args.get('category', '')

    query = (
        "SELECT name, image, price, is_new FROM products "
        "WHERE category_id = %s "  # Parametrized query for safety
        "ORDER BY is_new DESC "
        "LIMIT 16"
    )

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(query, (category_id,))
            products = cursor.fetchall()

        return jsonify([{
            'name': product[0],
            'image': product[1],
            'price': product[2],
            'is_new': product[3],
        } for product in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['GET', 'POST'])
def search_results():
    # Arama parametrelerini alın
    sort_order = request.args.get('sort', 'asc')  # Sıralama parametresi
    query = request.args.get('query', '')  # Arama sorgusu
    category_name = request.args.get('category', '')  # Kategori adı

    # Sıralama düzenini ayarlayın
    sort_clause = 'ASC' if sort_order == 'asc' else 'DESC'

    # SQL sorgusunun başlangıcı
    base_query = "SELECT name, image, price FROM products WHERE 1=1"  # Başlangıç koşulu
    
    # Ürün adında belirli bir kelime arayın
    if query:
        base_query += " AND name LIKE %s"
        params = [f"%{query}%"]
    else:
        params = []

    # Kategori kontrolü
    if category_name:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id FROM category WHERE name = %s", (category_name,))
            category = cursor.fetchone()

        if category:
            category_id = category[0]
            base_query += " AND category_id = %s"
            params.append(category_id)

    # Sıralama ve sorgu son hali
    base_query += f" ORDER BY price {sort_clause}"

    # SQL sorgusunu çalıştırın ve sonuçları alın
    with mysql.connection.cursor() as cursor:
        cursor.execute(base_query, tuple(params))
        results = cursor.fetchall()

    # Şablonu render edin
    return render_template("search_results.html", results=results, query=query, category=category_name)


@app.route('/all-products', methods=['GET'])
def all_products():
    sort_order = request.args.get('sort', 'asc')  # Sıralama
    page = int(request.args.get('page', 1))  # Hangi sayfa
    per_page = 112  # Sayfa başına ürün sayısı
    
    # Sıralama yönü
    sort_clause = 'ASC' if sort_order == 'asc' else 'DESC'

    # SQL sorgusu
    query = f"SELECT name, image, price FROM products ORDER BY price {sort_clause} LIMIT {per_page} OFFSET {(page - 1) * per_page}"

    with mysql.connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    # Toplam ürün sayısını bul
    with mysql.connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]

    total_pages = (total_products + per_page - 1) // per_page  # Toplam sayfa sayısı

    return render_template(
        "search_results.html",
        results=results,
        current_page=page,
        total_pages=total_pages,
        query="All Products"
    )
# Flask endpoint'i
@app.route('/products', methods=['GET'])
def get_products():
    with mysql.connection.cursor() as cursor:
        # Ürünleri ve bedenlerini çekmek için INNER JOIN kullanın
        cursor.execute("""
            SELECT p.name, s.name AS size
            FROM products p
            JOIN product_sizes ps ON p.id = ps.product_id
            JOIN sizes s ON ps.size_id = s.id
        """)
        results = cursor.fetchall()
    
    # Verileri JSON olarak döndürün veya şablonu render edin
    return jsonify(results)

#@app.route('/all-products', methods=['GET'])
#def all_products():
#    sort_order = request.args.get('sort', 'asc')  # Sıralama
#    size_filter = request.args.get('size', '')  # Beden #filtresi
#    page = int(request.args.get('page', 1))  # Hangi sayfa
#    per_page = 20  # Sayfa başına ürün sayısı
#    
#    # Sıralama yönü
#    sort_clause = 'ASC' if sort_order == 'asc' else 'DESC'
#
#    # SQL sorgusu
#    query = "SELECT name, image, price FROM products"
#    query_conditions = []
#
#    if size_filter:
#        query += " WHERE size = %s"
#        query_conditions.append(size_filter)
#
#    query += f" ORDER BY price {sort_clause}"
#    query += f" LIMIT {per_page} OFFSET {(page - 1) * per_page}#"  # Sayfalama için limit ve offset
#
#    with mysql.connection.cursor() as cursor:
#        cursor.execute(query, tuple(query_conditions))
#        results = cursor.fetchall()
#
#    # Sayfa bilgileri
#    total_products_query = "SELECT COUNT(*) FROM products"
#    if size_filter:
#        total_products_query += " WHERE size = %s"
#
#    with mysql.connection.cursor() as cursor:
#        if size_filter:
#            cursor.execute(total_products_query, #(size_filter,))
#        else:
#            cursor.execute(total_products_query)
#        
#        total_products = cursor.fetchone()[0]  # Toplam ürün #sayısı
#
#    total_pages = (total_products + per_page - 1) // per_page  ## Toplam sayfa sayısı
#
#    return render_template(
#        "search_results.html",
#        results=results,
#        current_page=page,
#        total_pages=total_pages,
#        query=request.args.get('query', 'All Products'),
#    )


