# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy,BaseQuery
#from sqlalchemy import *
from sqlalchemy.orm import query

import MySQLdb
import os
from wtforms import *

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@ip/db_name'
'''
your own mysql information,include username,password,ip,db_name
'''
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class Reader(db.Model):
	__tablename__ = 'readers'
	Reader_id = db.Column(db.String(64),primary_key=True)
	reader_name = db.Column(db.String(64))
	sex = db.Column(db.String(64))
	birthday = db.Column(db.DateTime)
	phone = db.Column(db.Integer)
	mobile = db.Column(db.String(64))
	card_name = db.Column(db.String(64))
	Card_id = db.Column(db.String(64))
	level = db.Column(db.String(64))
	day = db.Column(db.DateTime)

	def __repr__(self):
		return '<Reader_id %r' % self.Reader_id

bootstrap = Bootstrap(app)
moment = Moment(app)
app.secret_key= os.urandom(5)
conn = MySQLdb.connect("ip", "username", "password", "bd_name",charset='utf8')

'''
your own mysql information,include username,password,ip,db_name
'''

cur = conn.cursor()


def insert(username,password):
	sql = "insert into readers (Reader_id,phone) values ('%s','%s')" %(username,password)
	cur.execute(sql)
	conn.commit()
	conn.close()

def isExisted(username,password):
	sql="select * from readers where Reader_id ='%s' and phone ='%s'" %(username,password)
	cur.execute(sql)
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True


class LoginForm(Form):
	username = StringField("username",[validators.DataRequired()])
	password = PasswordField("password",[validators.DataRequired()])

@app.route("/manager")
def manager():
    return render_template('manager.html')

@app.route("/register",methods=['GET','POST'])
def register():
	myForm=LoginForm(request.form)
	if request.method=='POST':
		if(myForm.username.data == 'admin'):
			return "register failed ! because your username is illegal"
		else:
			insert(myForm.username.data,myForm.password.data)
			return "register success"
	return render_template('register.html',form=myForm)

@app.route("/login",methods=['GET','POST'])
def login():
	myForm=LoginForm(request.form)
	session['name'] = myForm.username.data
	if request.method =='POST':
		if (isExisted(myForm.username.data,myForm.password.data) and myForm.username.data !='admin'):
			return redirect(url_for('user'))
		elif (isExisted(myForm.username.data,myForm.password.data) and myForm.username.data =='admin'):
			return redirect(url_for('manager'))
		else:
			return "Login Failed"
	return render_template('user_login1.html',form=myForm)

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/reader/query', methods=['GET', 'POST'])
def reader_query():

	return render_template('user.html')


@app.route('/reader/info', methods=['GET', 'POST'])
def reader_info():
	readerInfo = Reader()
	readerInfo = Reader.query.filter_by(Reader_id =session['name']).first()
	return render_template('user_info.html',reader = readerInfo)

@app.route("/book_manager",methods=['GET','POST'])
def book_manager():
	return render_template('book_manager.html')

@app.route("/user_manager",methods=['GET','POST'])
def user_manager():
	return render_template('user_manager.html')

@app.route("/borrow_manager",methods=['GET','POST'])
def borrow_manager():
	return render_template('borrow_manager.html')


if __name__=="__main__":
	app.run(debug=True)
