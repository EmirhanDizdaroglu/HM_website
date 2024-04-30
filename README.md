# H&M Website - Flask App

This project is a web application developed using Python and Flask. The application includes Bootstrap, Flexbox, and Grid technologies along with HTML, CSS, and JavaScript. It interacts with the MySQL database and provides a dynamic list of products.

## Installation and Running of the Project

To run the project, follow these steps:

## google drive

https://drive.google.com/file/d/1iOKeBBNKZfPtYz-qwKaRMZH-0hiyFNYN/view?usp=sharing

## 1. Clone Repository
```bash
git clone https://github.com/EmirhanDizdaroglu/hm_project.git
go to the directory with cd project

```

## 2. Activate the Virtual Environment
A virtual environment is used to manage dependencies in Python projects. To activate the virtual environment:
```bash
venv\Scripts\activate # For Windows

source venv/bin/activate # For Linux/MacOS
```
## 3. Install Dependencies
Use pip install -r requirements.txt to install the dependencies used in the project. Some important packages used in the project are:
```bash
install Flask
install mysql-connector
install mysql-connector-python
install mysql-connector-python-rf
install pymysql
```
## 4. Install MySQL Database

Install and run MySQL.
Use appropriate SQL files to create the database and tables.
Update the database configuration in the config.py file with the correct information.
There are products and category tables in the MySQL database and there are foreign key connections between these tables.

## 5. Run the App

To start the Flask application:
```bash
python run.py
```
Then open the following URL in your web browser: http://127.0.0.1:5000/
This URL represents the address where the Flask application runs locally.
## Project File Structure

The project consists of the following files and folders:

- `app/`: The folder containing the main application files.
 - `app/__pycache__/`: Intermediate code files compiled by Python.
 - `app/static/`: Folder containing static files (CSS, JavaScript, images).
 - `app/static/css/`: CSS files.
 - `base.css`: Base CSS styles.
 - `buttons.css`: Custom styles for buttons.
 - `slider.css`: Custom styles for slider.
 - `style.css`: Main style file.
 - `styles.css`: Additional style file.
 - `app/static/images/`: Images used in the project.
 - `app/static/js/`: JavaScript files.
 - `script.js`: Main JavaScript file.
 - `app/templates/`: HTML template files.
 - `index.html`: Home page template.
 - `app/__init__.py`: The file from which the Flask application is started.
- `migrations/`: Folder containing database migration files.
- `venv/`: Virtual media folder. Where Python and Flask dependencies are installed.
- `config.py`: Python file used for application configuration.
- `requirements.txt`: List of Python packages used in the project.
- `run.py`: File used to start the Flask application.


## Project Features:
This project is designed to display at least 16 products in groups of 4 on the home page. Other features include:

Dynamic Categories: Categories are displayed at the top of the slider.
Responsive Design: Hamburger menu and flexible layouts on mobile devices.
Search Results: The left panel contains categories, and the right panel contains search results.
Price Sorting and Size Filtering: Price sorting and size filtering features.

This README file explains the purpose of the project, installation and working steps, project structure, and features.

### project info

Veri tabanında kıyafet bedenleri için bir tablo oluşturuldu ve bu tablo S, M, L, XL bilgilerini saklıyor. Bir ürünün birden fazla bedeni olduğu için ara tablo yapılmalıdır.

her bir ürün için S,M,L,XL özellikleri python kodu ile rastgele dağıtıldı. Bu sayede her bir ürünün bazı bedenleri mevcut bazıları ise olmayacak.
Terminal çıktısı:
```bash
INSERT INTO product_sizes (product_id, size_id) VALUES (156, 2);
INSERT INTO product_sizes (product_id, size_id) VALUES (156, 3);
INSERT INTO product_sizes (product_id, size_id) VALUES (157, 2);
```

veri tabanını kontrol ettiğimizde görünmüyorsa bunu yapabiliriz.
```bash
pip install mysql-connector-python
```
