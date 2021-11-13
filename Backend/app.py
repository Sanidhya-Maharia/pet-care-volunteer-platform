from Database_Handler.handler import *
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return redirect('/login')

@app.route("/login",methods = ['POST', 'GET'])
def loginpage():
    if request.method == 'POST':
        name = request.form['Name']
        password = request.form['Password']
        result = Login.check(name, password)
        if result != None:
            return result
        else:
            return redirect('/login')
    
    return render_template('login.html')

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

    return render_template('signup.html')