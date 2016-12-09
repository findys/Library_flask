# -*- coding: utf-8 -*-
from flask import Flask,flash
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy,BaseQuery
from flask_wtf import Form
from wtforms import *
from sqlalchemy.orm import query

import MySQLdb
import os

#ol标签排序

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:10IDCcom@123.206.23.69:3306/Sql_Class'
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


class book(db.Model):
	__tablename__ = 'books'
	Book_id = db.Column(db.String(64),primary_key=True)
	book_name = db.Column(db.String(64))
	author = db.Column(db.String(64))
	publishing = db.Column(db.String(64))
	Category_id = db.Column(db.String(64))
	price = db.Column(db.Float)
	Date_in = db.Column(db.DateTime)
	Quanity_in = db.Column(db.Integer)
	Quanity_out = db.Column(db.Integer)
	Quanity_loss = db.Column(db.Integer)

	def __repr__(self):
		return '<Book_id %r' % self.Book_id

class borrow(db.Model):
	__tablename__ = 'borrow'
	Reader_id = db.Column(db.String(64),primary_key=True)
	Book_id = db.Column(db.String(64),primary_key=True)
	Date_borrow = db.Column(db.DateTime)
	Date_return = db.Column(db.DateTime)
	loss = db.Column(db.String(64))


bootstrap = Bootstrap(app)
moment = Moment(app)
app.secret_key= os.urandom(5)
conn = MySQLdb.connect("123.206.23.69", "root", "10IDCcom", "Sql_Class",charset='utf8')

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

class Newbookin_Form(Form):
	book_id = StringField('图书编号',[validators.DataRequired()])
	book_name = StringField('书名',[validators.DataRequired()])
	author = StringField('作者',[validators.DataRequired()])
	publishing = StringField('出版商',[validators.DataRequired()])
	Category_id = StringField('类别编号',[validators.DataRequired()])
	price = IntegerField('价格',[validators.DataRequired()])
	Date_in = DateTimeField('入库时间',[validators.DataRequired()])
	Quanity_in = IntegerField('入库数',[validators.DataRequired()])

class Borrow_Form(Form):
	borrow_name = StringField('借/还书人',[validators.DataRequired()])
	borrow_book = StringField('书名',[validators.DataRequired()])
	Date_borrow = DateTimeField('借书时间', [validators.DataRequired()])

@app.route("/borrow_manager",methods=['GET','POST'])
def borrow_manager():
	error = None
	form = Borrow_Form(request.form)
	if request.method == 'POST':
		B_reader = Reader.query.filter_by(reader_name = form.borrow_name.data).first()
		B_book = book.query.filter_by(book_name = form.borrow_book.data).first()
		if B_book.Quanity_in - B_book.Quanity_out > 0 :
			newborrow = borrow(Reader_id = B_reader.Reader_id,
							   Book_id = B_book.Book_id,
							   Date_borrow = form.Date_borrow.data,
							   loss='否')
			db.session.add(newborrow)
			B_book.Quanity_out = B_book.Quanity_out + 1
			B_book.Quanity_in = B_book.Quanity_in - 1
			db.session.add(B_book)
			error = 'Operation succeeded'
		else:
			error = 'Operation failed'
	return render_template('borrow_manager.html',form = form,error = error)


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
	bookInfo = None
	error = None
	if request.method == 'POST':
		if request.form['item'] == 'name':
			if not request.form['query']:
				error = 'You have to input the book name'
			else:
				bookInfo = book.query.filter_by(book_name = request.form['query']).first()
				if not bookInfo:
					error = 'invalid book name'
	return render_template('query_book.html',books = bookInfo,error = error)


@app.route('/reader/info', methods=['GET', 'POST'])
def reader_info():
	readerInfo = Reader()
	readerInfo = Reader.query.filter_by(Reader_id =session['name'])
	return render_template('user_info.html',readers = readerInfo)


@app.route("/book_manager",methods=['GET','POST'])
def book_manager():
	if session['name'] == 'admin':
		bookm = book()
		bookm = book.query.all()
	else:
		return redirect(url_for('no_permision'))
	return render_template('book_manager.html',bookm = bookm)


@app.route("/new_book_in",methods=['GET','POST'])
def new_book_in():
	if session['name'] == 'admin':
		error = None
		book_form = Newbookin_Form(request.form)
		if request.method == 'POST':
			newbook = book(Book_id = book_form.book_id.data,
					   book_name = book_form.book_name.data,
					   author = book_form.author.data,
					   publishing = book_form.publishing.data,
					   Category_id = book_form.Category_id.data,
					   price = book_form.price.data,
					   Date_in = book_form.Date_in.data,
					   Quanity_in = book_form.Quanity_in.data,
					   Quanity_out = 0,
					   Quanity_loss = 0)
			db.session.add(newbook)
			error = 'Operation succeeded'
	else:
		return redirect(url_for('no_permision'))
	return render_template('new_book_in.html',form = book_form ,error = error)

@app.route("/book_change/<bookid>",methods=['GET','POST'])
def book_change(bookid):
	pass
	return render_template('no_permission.html')


@app.route("/user_manager",methods=['GET','POST'])
def user_manager():
	return render_template('user_manager.html')


@app.route("/no_permision",methods=['GET','POST'])
def no_permision():
	return render_template('no_permission.html')


if __name__=="__main__":
	app.run(debug=True)
