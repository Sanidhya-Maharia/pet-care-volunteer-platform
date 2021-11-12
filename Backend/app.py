from Database_Handler.handler import *
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/loggedin",methods = ['POST', 'GET'])
def display():
    name = request.form['Name']
    password = request.form['Password']
    result = Login.check(name, password)
    if result!= None:
        return result
    else:
        return redirect('/')

@app.route("/signup",methods = ['POST', 'GET'])
def signup():
    return render_template('signup.html')

@app.route("/signup/profile",methods = ['POST', 'GET'])
def profile():
    name = request.form['signupname']
    result = SignUp.check(name)
    return result