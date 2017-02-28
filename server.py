from flask import Flask, render_template,request, Response,jsonify
app = Flask(__name__)
import urllib
import urllib2
import os,re,ast
import json
from prosperworks import api
from prosperworks.models import Company, Lead
api.configure('5d1d796c3977a1ac772edb25ad32fe95', 'saitejak2017@gmail.com')


def get_db(dbname):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[dbname]
    return db




def IsValidMail(email):
	if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
		return "Enter valid Email ID "
	return ""

def createLead(info,db):
	lead = Lead.create(name=info['name'],company_name=info['company'],email={"email": info['email'],"category": "Work"},phone_numbers=[{'number':info['phone'],'category':'mobile'}])
	db.leads.insert(info)
	return lead.id



@app.route('/')
def hello_world():
     return render_template("form.html")

@app.route('/leads', methods=['GET'])
def getAll():
	print "++++++++++++++"
	db = get_db('leads')
	info = db.leads.find({}, {'_id': False})
	info =list(info)
	info =json.dumps(info)
	resp = Response(info, status=200, mimetype='application/json')
	return resp


@app.route('/submit', methods=['POST'])
def submit():
	data = dict(request.form).keys()[0]
	data =ast.literal_eval(data)
	print data
	name = str(data['name'])
	phone = str(data['phone'])
	email = str(data['email'])
	company= str(data['company'])
	print name,company,email,phone
	error=""
	error+= ( IsValidMail(email))
	print error
	if len(error)==0:
		db = get_db('leads')
		info = {"name" : name,'company':company , 'email':email ,'phone':phone}
		resp = createLead(info,db)
		print resp
		print "########Success###############"
		info =json.dumps(dict(info),default=lambda x: None )
		resp = Response(info, status=200, mimetype='application/json')
		return resp
	else:
		resp = Response(error, status=449, mimetype='application/json')
		return resp



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1',port=8080)

    