from flask import Flask, render_template

app = Flask(__name__)


# 1. POČETNA STRANICA
@app.route('/')
def pocetna():
  
    return render_template('index.html')


if __name__ == '__main__':
    
    app.run(debug=True)