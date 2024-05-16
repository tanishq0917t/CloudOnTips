from flask import *
from flask_session import Session
from mongoConnection import MongoCollection
import time

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if not session.get("name"): return redirect("/login")
    return render_template("dashboard.html",name=session.get("name"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/myvps")
def myvps():
    return render_template("myvps.html")

@app.route("/newVps")
def newVps():
    return render_template("newVps.html")

@app.route("/getData",methods=['POST'])
def getData():
    user=session.get('name')
    return user

@app.route("/logout")
def logout():
	session["name"] = None
	return redirect("/")

@app.route("/auth",methods=["POST"])
def auth():
    if request.method=="POST":
        user=request.form['user']
        pwd=request.form['pass']
        mongoCollection=MongoCollection()
        collection=mongoCollection.getCollection("Users")
        data=collection.find_one({"userid":user})
        print(data)
        if data==None:
            return "-1"
        if data['pass']==pwd:
            session["name"] = user
            return "1"
        else: return "-1"



if __name__ == '__main__':
    app.run(debug = True)