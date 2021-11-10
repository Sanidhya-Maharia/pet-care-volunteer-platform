import pymongo

client = pymongo.MongoClient("mongodb+srv://Sanidhya:user1@cluster0.9uhlx.mongodb.net/User_info?retryWrites=true&w=majority")
db = client["User_info"]
login = db["Login"]

class Login:
    def check(name, password):
        q = {"name": name, "password": password} 
        x = login.find_one(q, {"_id": 0})
        if x != None:
            return x
        else:
            return "none"