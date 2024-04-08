from flask import Flask
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'sari'
app.config['MYSQL_PASSWORD'] = 'Sari@Itani101'
app.config['MYSQL_DATABASE'] = 'TELECOM'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DATABASE']
)

cursor = mysql.cursor()

from telecom_app import views
