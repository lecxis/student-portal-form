from flask import Flask, render_template, url_for, request, flash, current_app,jsonify, redirect
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import os

app= Flask(__name__)
app.secret_key='sec'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'students'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD']='tommot'
mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

#view for the index page
@app.route('/')
def index():
    return render_template('index.html')

#get state and local govt data and load as json
statesfile = os.path.join('static', "states-localgovts.json")
statesData=json.load(open(statesfile))
#def index():
 #   return render_template('index.html')

#@app.route('/form')
#def student_form():
#    return render_template('form.html',states=data)
#return states data
@app.route('/states' , methods=['GET', 'POST'])
def states():
    if request.method == 'GET':
        return jsonify(statesData)

#view for the students dashboard
@app.route('/dashboard')
def dashboard():
    conn= mysql.get_db()
    cursor=conn.cursor()
    cursor.execute('select id, first, middle, last, gender, jamb, addmission_status from data;' )
    allStudents = cursor.fetchall()
    return render_template('dashboard.html', details=allStudents)

#view for displaying individual student details
@app.route('/person/<id>')
def person(id):
    person_id=id
    print(person_id)
    conn=mysql.get_db()
    cursor= conn.cursor()
    cursor.execute('select id, first, middle, last, email, date, gender, phone, address, state, LGA, next_of_kin, jamb, addmission_status,image_name from data where id=%s', (person_id))
    student= cursor.fetchall()
    return render_template('person.html', details=student)

#view for diplaying stuident form, accepting data and image as well as updating the database
@app.route('/form', methods=['GET','POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html',states=statesData)
    elif request.method == 'POST' and request.get_json():
        req=request.get_json()
        firstName= req['firstName']
        middleName= req['middleName']
        lastName= req['lastName']
        email= req['email']
        dateOfBirth= req['dateOfBirth']
        gender= req['gender']
        phone= req['phoneNumber']
        address= req['address']
        state= req['state']
        lga= req['lga']
        nextOfKin= req['NextOfKin']
        jamb= req['jambScore']
        image=req['firstName']+req['middleName']+req['lastName']+'.png'
        if checkForm(firstName, middleName, lastName, jamb)==True:
            conn=mysql.get_db()
            cur= conn.cursor()
            cur.execute('insert into data(first, middle, last, email, date, gender, phone, address, state, LGA, next_of_kin, jamb,image_name) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (firstName, middleName, lastName, email, dateOfBirth, gender, phone, address, state, lga, nextOfKin, jamb,image))
            conn.commit()
            cur.close()
            print(firstName)
            flash('User  succesfully added', 'flash_success')
            return json.dumps('success')
        else:
            return json.dumps('failure')
            #return jsonify(message='password_update_error'),500
      
    elif request.method == 'POST' and request.files['file']:
        image= request.files['file']
        path = request.form.get("path")
        if image:
            filepath= os.path.join(current_app.root_path, 'static/images/{path}' .format(path=path))
            image.save(filepath)
        return  'dashboard' #redirect (url_for('dashboard')) 
    #return render_template('dashboard.html')

    # validate data to see if user already exist and or jamb score is invalid 
def checkForm(first, middle, last, jamb):
    conn=mysql.get_db()
    cur= conn.cursor()
    cur.execute('select id, first, middle, last, email, date, gender, phone, address, state, LGA, next_of_kin, jamb, addmission_status,image_name from data where first=%s and middle=%s and last=%s', (first,middle,last))
    users= cur.fetchall()
    print(users)
    if not users:
        if int(jamb) > 400:
            flash('Jamb Score is invalid', 'flash_error')
        else:
            return True
    else:
        flash('User already exist', 'flash_error')
        return False

# update admission status
@app.route('/status', methods=['POST'])
def status():
    req=request.get_json()
    id= req['id']
    status= req['status']
    conn=mysql.get_db()
    cursor= conn.cursor()
    cursor.execute('Update data set addmission_status = %s where id=%s',(status, id))
    conn.commit()
    cursor.close()
    return json.dumps('success')

if __name__=="__main__":
     app.run()
 ## venv\Scripts\activate to start virtual environment 
 ## python app.py to start application