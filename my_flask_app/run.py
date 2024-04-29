# run.py
from app import app  # Flask uygulamasını içe aktarın

if __name__ == "__main__":
    app.run(debug=True)  # Geliştirici modu için 'debug=True'
