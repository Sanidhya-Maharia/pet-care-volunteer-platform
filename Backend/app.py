import re
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
        return render_template('home1.html')

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
    alert = None
    if request.method == 'POST':
        name = request.form['signupname']
        password = request.form['signuppass']
        password2 = request.form['signuprepass']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        pincode = request.form['pincode']
        #city = request.form['city']
        city = request.form.get('city')
        phno = request.form['phno']
        email = request.form['email']

        List = [name, password, password2, firstname, lastname, pincode, city, phno, email]

        result1 = SignUp.check_if_unique(name)
        if result1 != None:
            alert = "username already exists"
        
        result2 = SignUp.check_password(password, password2)
        if result2 == None:
            alert = "passwords don't match"

        for x in List:
            result3 = SignUp.check_not_null(x)
            if result3 == None:
                alert = "some fields were left empty"
        
        if alert == None:
            SignUp.updatelogindb(name, password)
            SignUp.updateprofiledb(name, firstname, lastname, pincode, city, phno, email)
            session['name'] = name
            return redirect('/')

    return render_template('signuptest.html', alert=alert)

@app.route("/logout",methods = ['POST', 'GET'])
def logout():
    if 'name' in session:
        session.pop('name', None)
        return redirect('/')
    else:
        return "no one is logged in"

@app.route("/volunteer",methods = ['POST', 'GET'])
def volunteer():
    username = session['name']
    if 'name' in session:
        if request.method == 'POST':
            start = request.form['sdate']
            end = request.form['edate']
            pref = request.form.get('pref')
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
            return redirect("/")

        return render_template('testvol.html', username=username)
    else:
        return redirect('/login')

@app.route("/search",methods = ['POST', 'GET'])
def search():
    display = None
    if 'name' in session:
        if request.method == 'POST':
            start = request.form['sdate']
            end = request.form['edate']
            id = session['name']
            List = [start, end]

            for x in List:
                result1 = Search.check_not_null(x)
                if result1 == None:
                    return redirect('/search')
            
            results = Search.getdata(id, start, end)
            display = results
        
        return render_template('newsearch.html', display=display)
    else:
        return redirect('/login')

@app.route("/profile",methods = ['GET'])
def yourprofile():
    display = None
    if 'name' in session:
        id = session['name']
        display = Profile.getdata(id)
        return render_template('profile.html', display=display)
    else:
        return redirect('/login')

@app.route("/profile/<user>",methods = ['GET'])
def otherprofile(user):
    if 'name' in session:
        display = Profile.getdata(user)
        return render_template('profile2.html', display=display)
    else:
        return redirect('/login')

@app.route("/editprofile",methods = ['POST', 'GET'])
def editprofile():
    if 'name' in session:
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            pincode = request.form['pincode']
            city = request.form.get('city')
            phno = request.form['phno']
            email = request.form['email']
            id = session['name']

            Profile.edit_data(id, firstname, lastname, pincode, city, phno, email)
            return redirect('/profile')
        
        return render_template('edit.html')
    else:
        return redirect('/login')

@app.route("/services",methods = ['GET'])
def services():
    return render_template('services.html')

@app.route("/aboutus",methods = ['GET'])
def aboutus():
    return render_template('about.html')

@app.route("/contact",methods = ['GET'])
def contact():
    return render_template('contact.html')