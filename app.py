from flask import *
from flask_session import Session

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

@app.route("/logout")
def logout():
	session["name"] = None
	return redirect("/")

@app.route("/auth",methods=["POST"])
def auth():
    if request.method=="POST":
        user=request.form['user']
        pwd=request.form['pass']
        if user=="user" and pwd=="pass":
            session["name"] = user
            return "1"
        else: return "-1"



if __name__ == '__main__':
    app.run(debug = True)