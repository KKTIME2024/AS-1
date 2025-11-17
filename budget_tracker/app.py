from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/incomes')
def incomes():
    return render_template('incomes.html')

@app.route('/expenditures')
def expenditures():
    return render_template('expenditures.html')

@app.route('/goal')
def goal():
    return render_template('goal.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

if __name__ == '__main__':
    app.run(debug=True)