import pymongo

client = pymongo.MongoClient("mongodb+srv://Sanidhya:user1@cluster0.9uhlx.mongodb.net/User_info?retryWrites=true&w=majority")
db = client["User_info"]
login = db["Login"]
profile = db["Profile"]

class Login:
    def check(name, password):
        q = {"name": name, "password": password} 
        x = login.find_one(q, {"_id": 0})
        return x

class SignUp:
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
        if var==None:
            return None
        else:
            return 1

    def updatelogindb(name , password):
        q = {"name": name, "password": password}
        login.insert_one(q)

    def updateprofiledb(name, firstname, lastname, pincode, city, phno, email):
        q = {"_id": name, "firstname": firstname, "lastname": lastname, "pincode": pincode, "city": city, "phno": phno, "email": email}
        profile.insert_one(q)