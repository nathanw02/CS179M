from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    pass

@app.route('/comment', methods = ['POST'])
def comment():
    pass

@app.route('/load', methods = ['POST'])
def load():
    pass

@app.route('/manifest', methods = ['POST'])
def manifest():
    pass

@app.route('/complete', methods = ['POST'])
def complete():
    pass

if __name__ == "__main__": 
    app.run() 