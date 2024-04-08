from flask import render_template, request, redirect, url_for, session, flash
import pandas as pd
from telecom_app import app, mysql, cursor
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

def initialize_root_user():
    cursor.execute("SELECT * FROM Employees WHERE employee_name = 'root'")
    root_user = cursor.fetchone()
    if not root_user:
        hashed_password = bcrypt.generate_password_hash('root').decode('utf-8')
        cursor.execute("INSERT INTO Employees (employee_name, contact_info, employee_address, department, job_title, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                       ('root', '+96181192894', 'Aramoun, Mount Lebanon, Lebanon', 'Site', 'Manager', hashed_password))
        mysql.commit()
        print("Root user added successfully.")
    else:
        print("Root user already exists.")

initialize_root_user()

# CREATE TABLE IF NOT EXISTS Employees (
#     we will take care of those by creating an HR manager hardcoded into the database
#     department ENUM('POS', 'Site', 'Warehouse'),
#     job_title VARCHAR(50) NOT NULL,
#     PRIMARY KEY (eid)
# ); 

@app.route('/')
def index():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('type')

        if user_type == 'Customer':
            cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (username,))
        elif user_type == 'Employee':
            cursor.execute("SELECT * FROM Employees WHERE employee_name = %s", (username,))

        user = cursor.fetchone()
        
        if user:
            hashed_password = user[-1]
            if bcrypt.check_password_hash(hashed_password, password):
                session['username'] = username
                if user_type == 'Employee':
                    return redirect(url_for('employee_portal'))
                elif user_type == 'Customer':
                    return redirect(url_for('customer_portal'))
            else:
                flash('Incorrect password. Please try again.', 'error')
                return redirect(url_for('login'))
        else:
            flash('User not found. Please sign up.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get Data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone = request.form['phone']
        user_type = request.form['subject']

        # Check Password
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for('signup'))

        # Format stuff for the database
        username = f"{first_name} {last_name}"
        
        if email and phone:
            contact_info = f"Email:{email}, Phone Nb:{phone}"
        elif email:
            contact_info = f"Email:{email}"
        else:
            contact_info = f"Phone Nb:{phone}"
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Check if existing user
        if user_type == 'Customer':
            cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (username,))
        elif user_type == 'Employee':
            cursor.execute("SELECT * FROM Employees WHERE employee_name = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('User already exists. Please choose a different username.', 'error')
            return redirect(url_for('signup'))

        # Create user for customer or send request for employee
        if user_type == 'Customer':
            cursor.execute("INSERT INTO Customers (customer_name, contact_info, customer_address, password_hash) VALUES (%s, %s, %s, %s)",
                           (username, contact_info, address, hashed_password))
        elif user_type == 'Employee':
            df = pd.read_csv("./requests.csv")
            df.add((username, contact_info, address, hashed_password))
            flash("Wait for the application process now.")

        mysql.commit()

        if user_type == 'Employee':
            print(f"I want to become an employee...\nMy name is: {username}\nMy contact info is: {contact_info}\nMy address is: {address}\nMy Password is:{password}\nMy hashed_password is:{hashed_password}")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/employees', methods=['GET', 'POST'])
def employee_portal():
    if 'username' in session:
        cursor.execute("SELECT * FROM Employees WHERE employee_name = %s", (session['username'],))
        employee = cursor.fetchone()
        if employee:
            return render_template('index-employees.html', employee=employee, username=employee[1])
        else:
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/customers', methods=['GET', 'POST'])
def customer_portal():
    if 'username' in session:
        cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (session['username'],))
        customer = cursor.fetchone()
        if customer:
            return render_template('index-customers.html', customer=customer, username=customer[1])
        else:
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))