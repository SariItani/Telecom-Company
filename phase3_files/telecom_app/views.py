import csv
from datetime import datetime, timedelta
import random
import string
from flask import render_template, request, redirect, url_for, session, flash
from telecom_app import app, mysql, cursor
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# make a constant loop that runs continuously in the backend that always checks for overdue payments and deactivates the accounts and dismantles the SIM Card from that account.

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

def insert_sim_card(IMSI, phone_number, ICCID, PUK, PIN):
        sql = "INSERT INTO SIM_Cards (IMSI, phone_number, sim_status, ICCID, PUK, PIN) VALUES (%s, %s, %s, %s, %s, %s)"
        sim_card_data = (IMSI, phone_number, 'Inactive', ICCID, PUK, PIN)

        cursor.execute(sql, sim_card_data)
        mysql.commit()
        print(f"SIM card inserted successfully:\n{IMSI}\n{phone_number}\n{ICCID}\n{PUK}\nP{PIN}")

def generate_unique_value(existing_values, length=10):
    while True:
        value = ''.join(random.choices(string.digits, k=length))
        if value not in existing_values:
            existing_values.add(value)
            return value

def generate_sim_card_data(existing_values):
    # Generate unique IMSI
    imsi = generate_unique_value(existing_values)

    # Generate random phone number (for example)
    phone_number = ''.join(random.choices(string.digits, k=10))

    # Generate unique ICCID, PUK, and PIN
    iccid = generate_unique_value(existing_values)
    puk = generate_unique_value(existing_values)
    pin = generate_unique_value(existing_values)

    return imsi, phone_number, iccid, puk, pin

def insert_sim_cards(num_sim_cards):
    existing_values = set()
    for _ in range(num_sim_cards):
        imsi, phone_number, iccid, puk, pin = generate_sim_card_data(existing_values)
        insert_sim_card(imsi, phone_number, iccid, puk, pin)

# Insert 20 SIM cards each time the website reloads
insert_sim_cards(20)

def populate_services_table():
    bundles = [
        {"service_name": "Recharge Card $7", "description": "Recharge card bundle - $7", "price": 7.00},
        {"service_name": "Recharge Card $15", "description": "Recharge card bundle - $15", "price": 15.00},
        {"service_name": "Recharge Card $30", "description": "Recharge card bundle - $30", "price": 30.00},
        {"service_name": "Recharge Card $50", "description": "Recharge card bundle - $50", "price": 50.00},
        {"service_name": "Recharge Card $75", "description": "Recharge card bundle - $75", "price": 75.00},
        {"service_name": "Recharge Card $100", "description": "Recharge card bundle - $100", "price": 100.00},
        {"service_name": "Recharge Card $150", "description": "Recharge card bundle - $150", "price": 150.00},
        {"service_name": "Standard Bundle", "description": "Monthly service charge", "price": 5.00},
        {"service_name": "Basic Data Package", "description": "500MB Internet Access", "price": 10.00},
        {"service_name": "Standard Data Package", "description": "1500MB Internet Access", "price": 20.00},
        {"service_name": "Premium Data Package", "description": "5000MB Internet Access", "price": 30.00},
        {"service_name": "Basic Voice Package", "description": "90Mins Voice", "price": 10.00},
        {"service_name": "Standard Voice Package", "description": "270Mins Voice", "price": 20.00},
        {"service_name": "Unlimited Voice Package", "description": "Unlimited Voice", "price": 40.00},
        {"service_name": "Data + Voice Combo", "description": "750MB Internet and 75 Mins Voice", "price": 25.00},
        {"service_name": "Data + SMS Combo", "description": "750MB Internet and 1000SMS Messages", "price": 25.00},
        {"service_name": "Voice + SMS Combo", "description": "75Mins Voice and 1000SMS Messages", "price": 25.00},
        {"service_name": "International Calling Package", "description": "Enable International calling for a month", "price": 20.00},
        {"service_name": "International Roaming Package", "description": "Enable International roaming for a month", "price": 15.00},
        {"service_name": "International Messaging Package", "description": "Enable International messaging for a month", "price": 10.00},
        {"service_name": "Streaming Package", "description": "1080P Streaming - 4000MB Dedicated Internet", "price": 12.00},
        {"service_name": "Gaming Package", "description": "<100Ping Gaming - 4000MB Dedicated Internet", "price": 8.00},
        {"service_name": "Content Bundle", "description": "4K Content - 4000MB Dedicated Internet", "price": 15.00},
    ]

    cursor.execute("SELECT * FROM Services")
    existing_services = cursor.fetchall()
    if existing_services:
        print("Services table already populated.")
        return

    for bundle in bundles:
        sql = "INSERT INTO Services (service_name, description, price) VALUES (%s, %s, %s)"
        values = (bundle["service_name"], bundle["description"], bundle["price"])
        cursor.execute(sql, values)

    mysql.commit()
    print("Services table populated successfully.")

populate_services_table()

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
            if account_data[-1] == 'Individual':
                balance = 7.00
            elif account_data[-1] == 'Business':
                balance = 30.00
            
            cursor.execute("INSERT INTO Accounts (cid, balance, account_type, account_status) VALUES (%s, %s, %s, %s)",
                        (account_data[0], balance, account_data[-1], "Active"))
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
                
                cursor.execute("SELECT pid FROM Services WHERE service_name = 'Standard Bundle'")
                service_id = cursor.fetchone()[0]
                
                today = datetime.now()
                ending_date = today + timedelta(days=30)

                cursor.execute("INSERT INTO Subscriptions (pid, IMSI, starting_date, ending_date, renewal) VALUES (%s, %s, %s, %s, 'Auto')",
                            (service_id, random_inactive_sim, today, ending_date))
                
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
                SELECT
                    c.customer_name AS CustomerName,
                    c.contact_info AS ContactInfo,
                    c.customer_address AS Address,
                    a.account_type AS AccountType,
                    a.account_status AS AccountStatus,
                    s.IMSI AS SIMCardIMSI,
                    s.phone_number AS SIMCardPhoneNumber,
                    a.balance AS AccountBalance,
                MAX(sub.ending_date) AS NextDueDate  -- Get latest subscription's ending date
                FROM Customers c
                LEFT JOIN Accounts a ON c.cid = a.cid
                LEFT JOIN SIM_Cards s ON a.aid = s.aid
                LEFT JOIN Subscriptions sub ON s.IMSI = sub.IMSI  -- Join with Subscriptions table
                WHERE sub.ending_date >= CURDATE()  -- Filter for future ending dates
                GROUP BY c.cid, a.aid, s.IMSI, s.phone_number
                ORDER BY c.customer_name;
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
    if 'username' not in session:
        return redirect(url_for('login'))
    cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (session['username'],))
    customer = cursor.fetchone()
    if not customer:
        session.pop('username', None)
        return redirect(url_for('login'))
    if request.method == 'POST':
        print(request.form)
        cursor.execute("SELECT * FROM Accounts WHERE cid = %s", (customer[0],))
        existing_account = cursor.fetchone()
        if existing_account:
            flash("You already have an existing account.")
            return redirect(url_for('customer_portal'))
        with open('telecom_app/account_requests.csv', "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow((customer[0], customer[1], customer[2], customer[3], request.form.get('paymentMethod'), request.form.get('accountType')))
        flash("Wait for the application process now.")
        return redirect(url_for('customer_portal'))
    return render_template('account.html')

@app.route('/customers/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    cursor.execute("SELECT * FROM Customers WHERE customer_name = %s", (username,))
    customer = cursor.fetchone()

    cursor.execute("""
        SELECT a.*, c.customer_name
        FROM Accounts a
        INNER JOIN Customers c ON a.cid = c.cid
        WHERE c.customer_name = %s
    """, (username,))
    account = cursor.fetchone()

    cursor.execute("""
        SELECT p.*, e.employee_name, s.service_name
        FROM Payments p
        LEFT JOIN Employees e ON p.eid = e.eid
        LEFT JOIN Subscriptions sub ON p.sub_id = sub.sub_id
        LEFT JOIN Services s ON sub.pid = s.pid
        INNER JOIN Accounts a ON p.aid = a.aid
        INNER JOIN Customers c ON a.cid = c.cid
        WHERE c.customer_name = %s
        AND (p.payment_date IS NOT NULL AND (p.sub_id IS NOT NULL OR p.eid IS NOT NULL))
        ORDER BY p.payment_date DESC;
    """, (username,))
    payments = cursor.fetchall()

    cursor.execute("""
        SELECT p.*, s.service_name
        FROM Payments p
        LEFT JOIN Subscriptions sub ON p.sub_id = sub.sub_id
        LEFT JOIN Services s ON sub.pid = s.pid
        INNER JOIN Accounts a ON p.aid = a.aid
        INNER JOIN Customers c ON a.cid = c.cid
        WHERE c.customer_name = %s
        AND (p.payment_date IS NULL AND p.sub_id IS NOT NULL)
        ORDER BY p.due_date DESC;
    """, (username,))
    due_payments_with_subscription = cursor.fetchall()

    cursor.execute("""
        SELECT p.*, e.employee_name
        FROM Payments p
        LEFT JOIN Employees e ON p.eid = e.eid
        LEFT JOIN Subscriptions sub ON p.sub_id = sub.sub_id
        INNER JOIN Accounts a ON p.aid = a.aid
        INNER JOIN Customers c ON a.cid = c.cid
        WHERE c.customer_name = %s
        AND (p.payment_date IS NULL AND p.eid IS NOT NULL)
        ORDER BY p.due_date DESC;
    """, (username,))
    due_payments_with_employee = cursor.fetchall()

    due_payments = due_payments_with_subscription + due_payments_with_employee
    due_payments.sort(key=lambda x: x[4], reverse=True)

    cursor.execute("""
        SELECT sub.*, s.service_name
        FROM Subscriptions sub
        INNER JOIN Services s ON sub.pid = s.pid
        INNER JOIN SIM_Cards sc ON sub.IMSI = sc.IMSI
        INNER JOIN Accounts a ON sc.aid = a.aid
        INNER JOIN Customers c ON a.cid = c.cid
        WHERE c.customer_name = %s
        AND sub.ending_date >= CURDATE();
    """, (username,))
    subscriptions = cursor.fetchall()

    cursor.execute("""
        SELECT sc.*, a.account_type
        FROM SIM_Cards sc
        INNER JOIN Accounts a ON sc.aid = a.aid
        INNER JOIN Customers c ON a.cid = c.cid
        WHERE c.customer_name = %s;
    """, (username,))
    sim_card = cursor.fetchone()
    
    print("customer:", customer)
    print("account:", account)
    print("payments:", payments)
    print("due_payments:", due_payments)
    print("subscriptions:", subscriptions)
    print("sim_card:", sim_card)
    
    profile_data = {
        'Customer Details': {
            'Name': customer[1],
            'Contact Info': customer[2],
            'Address': customer[3]
        },
        'Account Details': {
            'Account ID': account[0],
            'Balance': account[2],
            'Type': account[3],
            'Status': account[4]
        },
        'Subscription Details': [{
            'Service Name': sub[6],
            'Starting Date': sub[3],
            'Ending Date': sub[4],
            'Renewal': sub[5]
        } for sub in subscriptions],
        'SIM Card Details': {
            'IMSI': sim_card[0],
            'Phone Number': sim_card[2],
            'Status': sim_card[3],
            'ICCID': sim_card[4],
            'PUK': sim_card[5],
            'PIN': sim_card[6]
        },
        'Payment History': [{
            'Amount': payment[5],
            'Due Date': payment[4],
            'Payment Date': payment[7],
            'Employee Name': payment[8] if payment[8] else '-',
            'Subscription ID': payment[3] if payment[3] else '-',
            'Service Name': payment[-1] if payment[-1] else '-'
        } for payment in payments],
        'Due Payments': [{
            'Amount': due_payment[5],
            'Due Date': due_payment[4],
            'Employee Name': due_payment[8] if due_payment[8] else '-',
            'Subscription ID': due_payment[3] if due_payment[3] else '-',
            'Service Name': due_payment[-1] if due_payment[-1] else '-'
        } for due_payment in due_payments]
    }
    
    print(profile_data)
    
    return render_template('profile.html', profile_data=profile_data)

@app.route('/customers/shop', methods=['GET', 'POST'])
def shop():
    if 'username' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM Services")
    services = cursor.fetchall()

    if request.method == 'POST':
        pid = request.form.get('buy')
        cursor.execute(f"SELECT * FROM Services WHERE pid={pid}")
        service = cursor.fetchone()
        try:
            cursor.execute("SELECT aid FROM Accounts WHERE cid = (SELECT cid FROM Customers WHERE customer_name = %s)", (session['username'],))
            account_id = cursor.fetchone()[0]
        except:
            return redirect(url_for('customer_portal'))
        price = service[-1]
        today = datetime.now().date()
        end_date = today + timedelta(days=30)
        cursor.execute("SELECT IMSI FROM SIM_Cards WHERE aid = %s", (account_id,))
        imsi = cursor.fetchone()[0]
        
        recharge = False
        if service[1] in ["Recharge Card $7", "Recharge Card $15", "Recharge Card $30", "Recharge Card $50", "Recharge Card $75", "Recharge Card $100", "Recharge Card $150"]:
            recharge = True
        if service[1] in ["Recharge Card $7", "Recharge Card $15", "Recharge Card $30", "Recharge Card $50", "Recharge Card $75", "Recharge Card $100", "Recharge Card $150", "International Calling Package", "International Roaming Package", "International Messaging Package"]:
            renewal = 'Manual'
        else:
            renewal = 'Auto'
        if renewal == 'Auto':
            cursor.execute("INSERT INTO Subscriptions (pid, IMSI, starting_date, ending_date, renewal) VALUES (%s, %s, %s, %s, %s)", (pid, imsi, today, end_date, renewal))
        else:
            cursor.execute("INSERT INTO Subscriptions (pid, IMSI, starting_date, ending_date, renewal) VALUES (%s, %s, %s, %s, %s)", (pid, imsi, today, today, renewal))
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        sub_id = cursor.fetchone()[0]
        
        if renewal == 'Auto':
            cursor.execute("INSERT INTO Payments (aid, sub_id, due_date, amount, payment_method) VALUES (%s, %s, %s, %s, %s)", (account_id, sub_id, end_date, price, 'Credit Card'))
        
        cursor.execute("INSERT INTO Payments (aid, sub_id, due_date, amount, payment_method, payment_date) VALUES (%s, %s, %s, %s, %s, %s)", (account_id, sub_id, today, price, 'Credit Card', today))
        
        if recharge:
            cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE aid = %s", (price, account_id))
            cursor.execute("UPDATE Subscriptions SET ending_date = %s WHERE pid = 8 AND IMSI = %s", (end_date, imsi))
            # cursor.execute("DELETE FROM Subscriptions WHERE sub_id = %s", (sub_id,))
        else:
            cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE aid = %s", (price, account_id))
        mysql.commit()

        return redirect(url_for('shop'))

    return render_template('shop.html', services=services)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))