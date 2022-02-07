#wsgi.py, in the same directory as app.py
from app import app

if __name__ == "__main__":
    app.run()