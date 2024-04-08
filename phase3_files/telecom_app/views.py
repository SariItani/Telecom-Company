from flask import render_template
from telecom_app import app, mysql, cursor

@app.route('/')
def index():
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    return render_template('index.html', customers=customers)

@app.route('/employees')
def EPortal():
    # require login
    # query employee entry from Employees table and then
    # username = employee.username
    # send usermame to frontend by adding username=username to the render_template()
    return render_template('index-employees.html')
