import pymongo
import json
import re
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

client = pymongo.MongoClient("mongodb+srv://Sanidhya:user1@cluster0.9uhlx.mongodb.net/User_info?retryWrites=true&w=majority")
db = client["User_info"]
login = db["Login"]
profile = db["Profile"]
volstat = db["Volunteer_status"]

class Login:
    def check(name, password):
        q = {"name": name, "password": password} 
        x = login.find_one(q, {"_id": 0})
        return x

class SignUp:
    def check_email(email):
        if(re.fullmatch(regex, email)):
            return 1
        else:
            return None

    def check_if_unique(name):
        q = {"name": name}
        x = login.find_one(q, {"_id": 0})
        return x

    def check_password(password1, password2):
        if len(password1)<5:
            return None
        elif password1!=password2:
            return None
        else:
            return 1

    def check_not_null(var):
        if var==None or var=="":
            return None
        else:
            return 1

    def updatelogindb(name , password):
        q = {"name": name, "password": password}
        login.insert_one(q)

    def updateprofiledb(name, firstname, lastname, pincode, city, phno, email):
        q = {"_id": name, "firstname": firstname, "lastname": lastname, "pincode": pincode, "city": city, "phno": phno, "email": email}
        profile.insert_one(q)

class Volunteer:
    def check_not_null(var):
        if var==None or var=="":
            return None
        else:
            return 1

    def insertdata(id, start, end, pref):
        cq = profile.find_one({"_id": id})
        x = json.dumps(cq)
        y = json.loads(x)
        city = y["city"]
        q = {"_id": id, "start_date": start, "end_date": end, "preference": pref, "city": city}
        volstat.insert_one(q)

    def updatedata(id, start, end, pref):
        q1 = {"_id": id}
        q2 = {"$set": {"start_date": start, "end_date": end, "preference": pref}}
        volstat.update_one(q1, q2)

    def check_for_existing(id, start, end, pref):
        q = {"_id": id}
        x = volstat.find_one(q)
        if x is None:
            Volunteer.insertdata(id, start, end, pref)
        else:
            Volunteer.updatedata(id, start, end, pref)

    def check_dates(start, end):
        if start>end:
            return None
        else:
            return 1

class Search:
    def check_not_null(var):
        if var==None or var=="":
            return None
        else:
            return 1

    def getdata(id, start, end):
        cq = profile.find_one({"_id": id})
        x = json.dumps(cq)
        y = json.loads(x)
        city = y["city"]
        array=[]
        q = volstat.find({"end_date": {"$gt": start}, "start_date": {"$lt": end}, "city": city})
        for x in q:
            y = json.dumps(x)
            z = json.loads(y)
            array.append(z)
        return array

class Profile:
    def getdata(id):
        q = profile.find_one({"_id": id})
        x = json.dumps(q)
        y = json.loads(x)
        return y

    def edit_data(id, firstname, lastname, pincode, city, phno, email):
        q1 = {"_id": id}
        q2 = {"$set": {"firstname": firstname, "lastname": lastname, "pincode": pincode, "city": city, "phno": phno, "email": email}}
        profile.update_one(q1, q2)