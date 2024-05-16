from flask import *
from flask_session import Session
from mongoConnection import MongoCollection
from createEC2 import CreateEC2

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
    if not session.get("name"): return redirect("/login")
    return render_template("myvps.html")

@app.route("/newVps")
def newVps():
    if not session.get("name"): return redirect("/login")
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


@app.route("/configureNewVPS",methods=["POST"])
def configureNewVPS():
    if request.method=="POST":
        request_data = request.json  # Parse JSON data
        name = request_data.get('name')
        storage = request_data.get('storage')
        os = request_data.get('os')
        inst = request_data.get('inst')
        soft_list = request_data.get('list')
        obj=CreateEC2()
        data={
            'serverName':name,
            'serverStorage':storage,
            'serverOS':os,
            'serverType':inst,
            'serverSoftwares':soft_list
        }
        instanceId=obj.createNewEC2(data)
        return instanceId


if __name__ == '__main__':
    app.run(debug = True)