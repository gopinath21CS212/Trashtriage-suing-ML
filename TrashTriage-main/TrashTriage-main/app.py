import base64
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import Flask, Response, jsonify, render_template,request, redirect, session
import cv2
import numpy as np
import pandas as pd
from classification import classification
import tensorflow as tf

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'devahari'
app.config['MYSQL_DB'] = 'TrashTriage'

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

mysql = MySQL(app)


output_folder = 'captured_frames'

import MySQLdb

def log_into_prediction(prediction):
    mat = prediction.split("$")[0].split("#")[1]
    
    # Establish a connection to the database
    cursor = mysql.connection.cursor()

    # Fetch the EmployeeID for the given username
    cursor.execute("SELECT EmployeeID FROM register WHERE username = %s", (session['username'],))
    employee_id = cursor.fetchone()

    if employee_id is not None:
        # Increment the value in the prediction table
        cursor.execute("SELECT * FROM prediction where EmployeeID=%s",(employee_id[0],))
        t = cursor.fetchone()
        if t == None:
            cursor.execute("INSERT INTO prediction(EmployeeID,plastics,glass,paper,metal,gadget) VALUES(%s,%s,%s,%s,%s,%s)",(employee_id[0],0,0,0,0,0))
        else:
            cursor.execute("UPDATE prediction SET {} = {} + 1 WHERE EmployeeID = %s".format(mat, mat), (employee_id[0],))
        mysql.connection.commit()
    else:
        print("User not found")

    cursor.close()


@app.route('/registerToDatabase', methods=['GET', 'POST'])
def registerToDatabase():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname = request.form['fname']
        username = request.form['uname']
        password = request.form['pass']
        em_id = request.form['eid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO register (username, password, fullname, EmployeeID) VALUES (%s, %s, %s, %s)',
                       (username,password,fullname,em_id))
        mysql.connection.commit()

        session['loggedin'] = True
        session['username'] = username
        return redirect('/')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('login.html', msg=msg)

@app.route('/classify',methods=["POST","GET"])
def classify():
    image = request.form.get("image")    
    if image:
        if ',' in image:
            base64_data = image.split(',')[1]
            image_data = base64.b64decode(base64_data)
            nparr = np.frombuffer(image_data, np.uint8)
            pre_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is not None:
        classf = classification('keras_model.h5','labels.txt')
        prediction = classf.classify_image(pre_image)
        log_into_prediction(prediction)
    return jsonify({'prediction': prediction})

@app.route('/login',methods=["GET","POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT username,password FROM register WHERE username = %s', (username,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and user_data['password'] == password:
            session['loggedin'] = True
            session['username'] = username
            msg = 'Logged in successfully !'
            return redirect('/')
        else:
            msg = 'Incorrect username or password !'

    return render_template('login.html', msg=msg)

@app.route("/logout")
def logout():
    session.pop("username")
    session.clear()
    return redirect("/")
    

@app.route('/register',methods=["GET","POST"])
def register():
    msg = ''
    if request.method == 'POST' and 'uname' in request.form and 'pass' in request.form:
        fullname = request.form['fname']
        username = request.form['uname']
        password = request.form['pass']
        em_id = request.form['eid']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO register (username, password, fullname, EmployeeID) VALUES (%s, %s, %s, %s)',
                       (username,password,fullname,em_id))
        mysql.connection.commit()

        session['loggedin'] = True
        session['username'] = username
        return redirect('/')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)
    
@app.route('/')
def home():
    if 'username' in session:
        return render_template("index.html")
    else:
        return render_template('login.html')

@app.route('/segregate')
def segregate():
    return render_template('segregate.html')

@app.route('/report')
def report():
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
