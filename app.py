from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

import yaml

app = Flask(__name__)
#congiure db
db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql= MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        userDetails=request.form
        ID=userDetails['ID']
        Fname=userDetails['Fname']
        Lname=userDetails['Lname']
        gender=userDetails['gender']
        age=userDetails['age']
        session=userDetails['session']
        date=userDetails['date']
        phone=userDetails['phone']
        email=userDetails['email']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO members (ID,Fname,Lname,gender,age,session,date,phone,email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(ID,Fname,Lname,gender,age,session,date,phone,email))
        mysql.connection.commit()
        cur.close()
        return redirect('/done')
    return render_template('index.html')

    
@app.route('/done')
def done():
    return render_template ('done.html')



@app.route('/users')
def users():
    cur=mysql.connection.cursor()
    resultv=cur.execute("select * from members")
    if resultv>-1:
        userDetails=cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__=="__main__":
    app.run(debug=True)
