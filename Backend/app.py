from Database_Handler.handler import *
#from flask import Flask, request, render_template, redirect
from flask import *

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def home():
    if 'name' in session:
        return render_template('home2.html', username=session['name'])
    else:
        return render_template('hometest.html')

@app.route("/login",methods = ['POST', 'GET'])
def loginpage():
    alert = None
    if request.method == 'POST':
        name = request.form['Name']
        password = request.form['Password']
        result = Login.check(name, password)
        session['name'] = name
        if result != None:
            return redirect('/')
        else:
            alert = "invalid credentials"
    
    return render_template('testlogin.html', alert=alert)

@app.route("/signup",methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['signupname']
        password = request.form['signuppass']
        password2 = request.form['signuprepass']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        pincode = request.form['pincode']
        city = request.form['city']
        phno = request.form['phno']
        email = request.form['email']

        List = [name, password, password2, firstname, lastname, pincode, city, phno, email]

        result1 = SignUp.check_if_unique(name)
        if result1 != None:
            return redirect('/signup')
        
        result2 = SignUp.check_password(password, password2)
        if result2 == None:
            return redirect('/signup')

        for x in List:
            result3 = SignUp.check_not_null(x)
            if result3 == None:
                return redirect('/signup')
        
        SignUp.updatelogindb(name, password)
        SignUp.updateprofiledb(name, firstname, lastname, pincode, city, phno, email)
        return "accepted"

    return render_template('signupb.html')

@app.route("/logout",methods = ['POST', 'GET'])
def logout():
    if 'name' in session:
        session.pop('name', None)
        return redirect('/')
    else:
        return "no one is logged in"

@app.route("/volunteer",methods = ['POST', 'GET'])
def volunteer():
    if 'name' in session:
        if request.method == 'POST':
            start = request.form['sdate']
            end = request.form['edate']
            pref = request.form['pref']
            id = session['name']
            List = [start, end, pref]

            for x in List:
                result1 = Volunteer.check_not_null(x)
                if result1 == None:
                    return redirect('/volunteer')

            result2 = Volunteer.check_dates(start, end)
            if result2 == None:
                return redirect('/volunteer')
            
            Volunteer.check_for_existing(id, start, end, pref)
            return "done"

        return render_template('volunteer.html')
    else:
        return redirect('/login')