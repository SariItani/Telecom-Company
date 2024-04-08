from flask import render_template
from telecom_app import app, mysql, cursor

@app.route('/')
def index():
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    return render_template('index.html', customers=customers)
