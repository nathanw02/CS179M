from flask import Flask, render_template, request
from algorithms.load import load
from algorithms.balance import balance

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

@app.route('/load', methods = ['GET', 'POST'])
def loadRequest():
    if request.method == 'GET':
        return render_template('steps.html')

    load_items = request.form.get('load')
    unload_items = request.form.get('unload')
    manifest = request.form.get('manifest')

    steps = load(load_items, unload_items, manifest)

    return steps

@app.route('/balance', methods = ['GET', 'POST'])
def balanceRequest():
    if request.method == 'GET':
        return render_template('steps.html')
    
    manifest = request.form.get('manifest')

    steps = balance(manifest)

    return steps

@app.route('/manifest', methods = ['POST'])
def manifest():
    pass

@app.route('/complete', methods = ['POST'])
def complete():
    pass

if __name__ == "__main__": 
    app.run()
