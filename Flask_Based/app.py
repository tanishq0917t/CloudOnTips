from flask import *
from flask_session import Session
from mongoConnection import MongoCollection
from createEC2 import CreateEC2
from ConfigureEC2 import EC2Configurations
from sendMail import SendMail
import random
import uuid
import importlib
import os
import sys

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

urls={}

def loadURL():
    connection=MongoCollection()
    collection=connection.getCollection("ServerlessServices")
    a=collection.find()
    for i in a:
        url=i['url']
        if i.get('tp'):
            data={
                'user':i['user'],
                'serviceName':i['serviceName'],
                'functionName':i['functionName'],
                'file':i['handlingFileName'],
                'req':i['req'],
                'tp':i['tp']
            }
        else:
            data={
                'user':i['user'],
                'serviceName':i['serviceName'],
                'functionName':i['functionName'],
                'file':i['handlingFileName'],
                'req':i['req']
            }
        urls[url]=data


loadURL()
print(urls)
def createURLMapping():
    url = str(uuid.uuid4()).split('-')[-1]
    return f"/service/{url}"

def dynamic_function_executor(module_name, function_name,inp, reqType):
    try:
        module_path = os.path.dirname(module_name)
        sys.path.append(module_path)
        module_file = os.path.basename(module_name)
        module_name_no_ext = os.path.splitext(module_file)[0]
        module = importlib.import_module(module_name_no_ext)
        func = getattr(module, function_name)
        result=func(inp,reqType)
        return result
    except ImportError:
        return f"Module '{module_name}' not found."
    except AttributeError:
        return f"Function '{function_name}' not found in module '{module_name}'."
    except Exception as e:
        return f"An error occurred: {str(e)}"


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

@app.route("/pems")
def pems():
    if not session.get("name"): return redirect("/login")
    return render_template("mypems.html")

@app.route("/serverless")
def serverless():
    if not session.get("name"): return redirect("/login")
    return render_template("serverless.html")



@app.route("/getData",methods=['POST'])
def getData():
    user=session.get('name')
    return user

@app.route("/authDone",methods=['POST'])
def authDone():
    if request.method=="POST":
        user=request.form['user']
        session["name"] = user
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
        accName = request_data.get('accName')
        obj=CreateEC2()
        data={
            'serverName':name,
            'serverStorage':storage,
            'serverOS':os,
            'serverType':inst,
            'serverSoftwares':soft_list,
            'user':accName
        }
        instanceId,publicIP=obj.createNewEC2(data)
        connection=MongoCollection()
        collection=connection.getCollection('VPSDetails')
        collection.insert_one({
            'user':accName,
            'vpsName':name,
            'instanceId':instanceId,
            'os':os,
            'status':'Running',
            'publicIP':publicIP
        })
        return instanceId

@app.route("/getVPSData",methods=["POST"])
def getVPSData():
    if request.method=="POST":
        user=request.form['user']
        connection=MongoCollection()
        collection=connection.getCollection("VPSDetails")
        pems=collection.find({'user':user})
        lst=[]
        for i in pems:
            d=dict()
            d['name']=i['vpsName']
            if i['os']=="ami-05e00961530ae1b55":
                d['os']="Ubuntu 22.04"
            elif i['os']=="ami-0f58b397bc5c1f2e8":
                d['os']="Ubuntu 24.04"
            d['status']=i['status']
            d['publicIP']=i['publicIP']
            lst.append(d)
        print("sending data")
        collection=connection.getCollection("ServerlessServices")
        services=collection.find({'user':user})
        lst1=[]
        for i in services:
            d=dict()
            d['serviceName']=i['serviceName']
            d['functionName']=i['functionName']
            d['url']=i['url']
            d['req']=i['req']
            lst1.append(d)
        return {'pems':lst,'services':lst1}


@app.route("/stopInstance",methods=["POST"])
def stopInstance():
    if request.method=="POST":
        user=request.form['user']
        vpsName=request.form['vpsName']
        ec2=EC2Configurations()
        response=ec2.stopInstance(user,vpsName)
        return response
        

@app.route("/startInstance",methods=["POST"])
def startInstance():
    if request.method=="POST":
        user=request.form['user']
        vpsName=request.form['vpsName']
        ec2=EC2Configurations()
        response=ec2.startInstance(user,vpsName)
        return response
        

@app.route("/deleteInstance",methods=["POST"])
def deleteInstance():
    if request.method=="POST":
        user=request.form['user']
        vpsName=request.form['vpsName']
        ec2=EC2Configurations()
        response=ec2.deleteInstance(user,vpsName)
        return response

@app.route("/downloadPEM",methods=["POST"])        
def downloadPEM():
    if request.method=="POST":
        user=request.form['user']
        file=request.form['file']
        sendEmail=SendMail()
        subject="PEM File"
        body=f"Hi {user},<br>Please find below attached PEM file as per your request<br><br>Thanks & Regards<br>Cloud On Tips"
        sendEmail.mail(user,subject,body,file)
        return "Done"
    
@app.route("/sendOtp",methods=["POST"])
def sendOtp():
    if request.method=="POST":
        user=request.form['user']
        otp=str(random.random())[2:8]
        print(otp)
        sendEmail=SendMail()
        subject="OTP Verification"
        body=f"Hi {user},<br>Please find below OTP: {otp} for your login request.<br><br>Thanks & Regards<br>Cloud On Tips"
        sendEmail.mail(user,subject,body)
        return otp

@app.route("/createServerlessService",methods=["POST"])
def createServerlessService():
    if request.method=="POST":
        print(request.form)
        print(request.files['file'])
        user=request.form['user'].split('@')[0]
        serviceName=request.form['serviceName']
        functionName=request.form['functionName']
        fName=request.files['file'].filename
        request.files['file'].save(f"services/{user}/{fName}")
        reqType=request.form['req']
        url=createURLMapping()
        connection=MongoCollection()
        collection=connection.getCollection("ServerlessServices")
        if reqType=="POST":
            tp=request.form['tp']
            data={
                'user':request.form['user'],
                'serviceName':serviceName,
                'functionName':functionName,
                'handlingFileName':fName,
                'url':url,
                'req':reqType,
                'tp':tp
            }
        else:
            data={
                'user':request.form['user'],
                'serviceName':serviceName,
                'functionName':functionName,
                'handlingFileName':fName,
                'url':url,
                'req':reqType
            }
        urls[url]=data
        collection.insert_one(data)
        return ""

@app.route("/service/<random_value>",methods=["GET","POST"])
def service(random_value):
    data=urls["/service/"+random_value]
    moduleName=data['file']
    functionName=data['functionName']
    user=data['user'].split('@')[0]
    reqType=data['req']
    if request.method=="POST" and reqType=="POST":    
        tp=data['tp']
        if tp=="JSON":
            return dynamic_function_executor(f"services/{user}/"+moduleName,functionName,request.json,reqType)
        elif tp=="FORMDATA":
            return dynamic_function_executor(f"services/{user}/"+moduleName,functionName,request.form,reqType)
    elif request.method=="GET" and reqType=="GET":
        return dynamic_function_executor(f"services/{user}/"+moduleName,functionName,request.args,reqType)
    else: return {"message":"Invalid request Type"}
    





if __name__ == '__main__':
    app.run(debug = True)
