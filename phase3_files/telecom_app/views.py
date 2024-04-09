import csv
from datetime import datetime
import random
import string
from flask import render_template, request, redirect, url_for, session, flash
from telecom_app import app, mysql, cursor
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# def initialize_root_user():
#     cursor.execute("SELECT * FROM Employees WHERE employee_name = 'root'")
#     root_user = cursor.fetchone()
#     if not root_user:
#         hashed_password = bcrypt.generate_password_hash('root').decode('utf-8')
#         cursor.execute("INSERT INTO Employees (employee_name, contact_info, employee_address, department, job_title, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
#                        ('root', '+96181192894', 'Aramoun, Mount Lebanon, Lebanon', 'Site', 'Manager', hashed_password))
#         mysql.commit()
#         print("Root user added successfully.")
#     else:
#         print("Root user already exists.")

# initialize_root_user()

# def insert_sim_card(IMSI, phone_number, ICCID, PUK, PIN):
#         sql = "INSERT INTO SIM_Cards (IMSI, phone_number, sim_status, ICCID, PUK, PIN) VALUES (%s, %s, %s, %s, %s, %s)"
#         sim_card_data = (IMSI, phone_number, 'Inactive', ICCID, PUK, PIN)

#         cursor.execute(sql, sim_card_data)
#         mysql.commit()
#         print(f"SIM card inserted successfully:\n{IMSI}\n{phone_number}\n{ICCID}\n{PUK}\nP{PIN}")

# def generate_unique_value(existing_values, length=10):
#     while True:
#         value = ''.join(random.choices(string.digits, k=length))
#         if value not in existing_values:
#             existing_values.add(value)
#             return value

# def generate_sim_card_data(existing_values):
#     # Generate unique IMSI
#     imsi = generate_unique_value(existing_values)

#     # Generate random phone number (for example)
#     phone_number = ''.join(random.choices(string.digits, k=10))

#     # Generate unique ICCID, PUK, and PIN
#     iccid = generate_unique_value(existing_values)
#     puk = generate_unique_value(existing_values)
#     pin = generate_unique_value(existing_values)

#     return imsi, phone_number, iccid, puk, pin

# def insert_sim_cards(num_sim_cards):
#     existing_values = set()
#     for _ in range(num_sim_cards):
#         imsi, phone_number, iccid, puk, pin = generate_sim_card_data(existing_values)
#         insert_sim_card(imsi, phone_number, iccid, puk, pin)

# # Insert 1000 SIM cards
# insert_sim_cards(1000)

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
            with open('telecom_app/requests.csv', "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow((username, contact_info, address, hashed_password))
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
    
@app.route('/employees/requests', methods=['GET', 'POST'])
def requests():
    if 'username' in session:
        cursor.execute("SELECT * FROM Employees WHERE employee_name = %s", (session['username'],))
        employee = cursor.fetchone()
        if employee[-2] != 'Manager':
            flash("You are not a Manager! Get a manager to do it instead.", 'error')
            session.clear()
            return redirect(url_for('login'))
        if employee:
            with open('telecom_app/requests.csv', 'r', newline="") as file:
                csv_reader = csv.reader(file)
                requests = list(csv_reader)
                print(requests)
            with open('telecom_app/account_requests.csv', 'r', newline="") as file:
                csv_reader = csv.reader(file)
                accounts = list(csv_reader)
                print(accounts)
            return render_template('requests.html', employeeRequests=requests, accounts=accounts)
        else:
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/handle-request', methods=['POST'])
def handle_request():
    if request.method == 'POST':
        print(request.form)
        if request.form.get('accept'):
            request_index = request.form.get('request_index')
            job_title = request.form.get('job')
            department = request.form.get('department')
            
            username = request_index
            with open('telecom_app/requests.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == request_index:
                        employee = row
                        break
            contact_info = employee[1]
            address = employee[2]
            hashed_password = employee[3]
            
            cursor.execute("INSERT INTO Employees (employee_name, contact_info, employee_address, department, job_title, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                        (username, contact_info, address, department, job_title, hashed_password))
            mysql.commit()
            
            flash('Employee created successfully', 'success')
            with open('telecom_app/requests.csv', 'r') as file:
                lines = file.readlines()
            with open('telecom_app/requests.csv', 'w') as file:
                for line in lines:
                    if request_index not in line:
                        file.write(line)

            return redirect(url_for('requests'))
        
        elif request.form.get('reject'):
            request_index = request.form.get('request_index')
            flash('Employee Rejected and will never bother us again', 'error')
            with open('telecom_app/requests.csv', 'r') as file:
                lines = file.readlines()
            with open('telecom_app/requests.csv', 'w') as file:
                for line in lines:
                    if request_index not in line:
                        file.write(line)
            return redirect(url_for('requests'))
        
        elif request.form.get('accept-account'):
            request_index = request.form.get('account_index')
            with open('telecom_app/account_requests.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == request_index:
                        account_data = row
                        break
            cursor.execute("INSERT INTO Accounts (cid, account_type, account_status) VALUES (%s, %s, %s)",
                           (account_data[0], account_data[-1], "Active"))
            cursor.execute("SELECT LAST_INSERT_ID()")
            aid = cursor.fetchone()[0]
            mysql.commit()
            
            with open('telecom_app/account_requests.csv', 'r') as file:
                lines = file.readlines()
            with open('telecom_app/account_requests.csv', 'w') as file:
                for line in lines:
                    if request_index not in line:
                        file.write(line)
                        
            cursor.execute("SELECT eid FROM Employees WHERE employee_name = %s", (session['username'],))
            eid = cursor.fetchone()[0]

            cursor.execute("SELECT IMSI FROM SIM_Cards WHERE sim_status = 'Inactive'")
            inactive_sim_cards = cursor.fetchall()
            if inactive_sim_cards:
                random_inactive_sim = random.choice(inactive_sim_cards)[0]
                cursor.execute("UPDATE SIM_Cards SET aid = %s, sim_status = 'Active' WHERE IMSI = %s",
                            (aid, random_inactive_sim))
                if account_data[-1] == 'Individual':
                    amount = 5.67
                elif account_data[-1] == 'Business':
                    amount = 21.67
                cursor.execute("INSERT INTO Payments (aid, eid, amount, payment_method, due_date, payment_date) VALUES (%s, %s, %s, %s, %s, %s)",
                       (aid, eid, amount, account_data[4], datetime.now(), datetime.now()))
                mysql.commit()
            flash('Account created successfully', 'success')
            return redirect(url_for('requests', request_type='customer_accounts'))
        
        elif request.form.get('reject-account'):
            request_index = request.form.get('account_index')
            flash('Account creation request rejected', 'error')
            with open('telecom_app/account_requests.csv', 'r') as file:
                lines = file.readlines()
            with open('telecom_app/account_requests.csv', 'w') as file:
                for line in lines:
                    if request_index not in line:
                        file.write(line)
            return redirect(url_for('requests', request_type='customer_accounts'))
        
    else:
        flash('Invalid request method', 'error')
        return redirect(url_for('requests'))

@app.route('/employees/customers', methods=['GET', 'POST'])
def customers_query():
    if 'username' in session:
        cursor.execute("SELECT * FROM Employees WHERE employee_name = %s", (session['username'],))
        employee = cursor.fetchone()
        if employee:
            sql = """
                SELECT c.cid AS CustomerID, c.customer_name AS CustomerName, c.contact_info AS ContactInfo, c.customer_address AS Address,
                        a.aid AS AccountID, a.account_type AS AccountType, a.account_status AS AccountStatus,
                        s.IMSI AS SIMCardIMSI, s.phone_number AS SIMCardPhoneNumber
                    FROM Customers c
                    LEFT JOIN Accounts a ON c.cid = a.cid
                    LEFT JOIN SIM_Cards s ON a.aid = s.aid
                    ORDER BY c.cid;
                """
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data)
            return render_template('customers-query.html', data=data)
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
    
@app.route('/customers/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        print(request.form)
        cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (session['username'],))
        customer = cursor.fetchone()
        print(customer)
        with open('telecom_app/account_requests.csv', "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((customer[0], customer[1], customer[2], customer[3], request.form.get('paymentMethod'), request.form.get('accountType')))
        flash("Wait for the application process now.")
        return redirect(url_for('customer_portal'))
    if 'username' in session:
        cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (session['username'],))
        customer = cursor.fetchone()
        if customer:
            return render_template('account.html')
        else:
            session.pop('username', None)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))