from Database_Handler.handler import Login
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('test.html')

@app.route("/login",methods = ['POST', 'GET'])
def display():
    name = request.form['Name']
    password = request.form['Password']
    return Login.check(name, password)