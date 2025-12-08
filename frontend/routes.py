from flask import Flask, render_template
from backend.app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chickens')
def chickens_page():
    return render_template('index.html')

@app.route('/eggs')
def eggs_page():
    return render_template('index.html')

@app.route('/health')
def health_page():
    return render_template('index.html')

@app.route('/feed')
def feed_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)