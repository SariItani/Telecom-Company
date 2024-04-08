from flask import render_template, request, redirect, url_for, session, flash
from telecom_app import app, mysql, cursor
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    return render_template('index.html', customers=customers)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        type = request.form['type']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if type == 'Customer':
            cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (username,))
        elif type == 'Employee':
            cursor.execute("SELECT * FROM Employees WHERE employee_name = %s", (username,))

        existing_user = cursor.fetchone()

        if existing_user:
            flash('User already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        if type == 'Customer':
            cursor.execute("INSERT INTO Customers (customer_name, contact_info, customer_address) VALUES (%s, %s, %s)",
                        (username, email, ''))
        elif type == 'Employee':
            cursor.execute("INSERT INTO Employees (employee_name, contact_info, employee_address, department, job_title) VALUES (%s, %s, %s, %s, %s)",
                        (username, '', '', 'POS', 'Customer Service Representative'))
        mysql.commit()
        return redirect(url_for('login'))
    return render_template('sign-up.html')

@app.route('/employees', methods=['GET', 'POST'])
def employee_portal():
    # Check if user is logged in
    if 'username' in session:
        # Fetch employee-specific data from the database
        cursor.execute("SELECT * FROM Employees WHERE username = %s", (session['username'],))
        employee = cursor.fetchone()
        if employee:
            # Render the employee portal base template and pass employee data
            return render_template('index-employees.html', employee=employee)
        else:
            # If the employee is not found, log them out
            session.pop('username', None)
            return redirect(url_for('login'))  # Redirect to login page
    else:
        # If user is not logged in, redirect to login page
        return redirect(url_for('login'))  # Redirect to login page