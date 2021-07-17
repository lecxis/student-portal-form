from flask import Flask, render_template, url_for, request, current_app,jsonify
from flaskext.mysql import MySQL
import pymysql.cursors
import json
import os

app= Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'students'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD']='tommot'

mysql = MySQL(app, cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return render_template('index.html')

#@app.route('/receiver', methods=['POST'])
filen = os.path.join('static', "states-localgovts.json")
data=json.load(open(filen))
def index():
    return render_template('index.html')

@app.route('/form')
def student_form():
    return render_template('form.html',states=data)

@app.route('/states' , methods=['GET', 'POST'])
def states():
    if request.method == 'GET':
        return jsonify(data)

@app.route('/dashboard')
def dashboard():
    conn= mysql.get_db()
    cur=conn.cursor()
    cur.execute('select id, first, middle, last, gender, jamb, addmission_status from data;' )
    rv = cur.fetchall()
    #for item in rv:
     #   print(item)
    return render_template('dashboard.html', details=rv)

@app.route('/person/<id>')
def person(id):
    person_id=id
    print(person_id)
    conn=mysql.get_db()
    cur= conn.cursor()
    cur.execute('select id, first, middle, last, email, date, gender, phone, address, state, LGA, next_of_kin, jamb, addmission_status,image_name from data where id=%s', (person_id))
    rv = cur.fetchall()
    return render_template('person.html', details=rv)

@app.route('/submit', methods=['POST'])
def submitForm():
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
    conn=mysql.get_db()
    cur= conn.cursor()
    cur.execute('insert into data(first, middle, last, email, date, gender, phone, address, state, LGA, next_of_kin, jamb,image_name) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (firstName, middleName, lastName, email, dateOfBirth, gender, phone, address, state, lga, nextOfKin, jamb,image))
    conn.commit()
    cur.close()
    return json.dumps('success')

@app.route('/save_image', methods=['POST'])
def save_image():
    image= request.files['file']
    path = request.form.get("path")
    
    if image:
        filepath= os.path.join(current_app.root_path, 'static/images/{path}' .format(path=path))
        image.save(filepath)
    return 'success'
    # update admission status
@app.route('/status', methods=['POST'])
def status():
    req=request.get_json()
    id= req['id']
    status= req['status']
    conn=mysql.get_db()
    cur= conn.cursor()
    cur.execute('Update data set addmission_status = %s where id=%s',(status, id))
    conn.commit()
    cur.close()
    return json.dumps('success')

if __name__=="__main__":
     app.run()
 ## venv\Scripts\activate to start virtual environment 