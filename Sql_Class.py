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
from wtforms import *
import os

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:10IDCcom@123.206.23.69:3306/only_for_test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.secret_key= os.urandom(5)


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
	password = db.Column(db.String(64))

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

	def __repr__(self):
		return '<Reader_id %r' % self.Reader_id

class loss_reporting(db.Model):
	__tablename__ = 'loss_reporting'
	Reader_id = db.Column(db.String(64), primary_key=True)
	Loss_date = db.Column(db.DateTime)

	def __repr__(self):
		return '<Reader_id %r' % self.Reader_id



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

class register_Form(Form):
	Reader_id = StringField('读者编号',[validators.DataRequired()])
	reader_name = StringField('读者姓名',[validators.DataRequired()])
	sex = StringField('性别',[validators.DataRequired()])
	birthday = DateTimeField('生日',[validators.DataRequired()])
	phone =  IntegerField('电话',[validators.DataRequired()])
	mobile = StringField('手机',[validators.DataRequired()])
	card_name = StringField('证件名',[validators.DataRequired()])
	Card_id = StringField('证件号码',[validators.DataRequired()])
	level = StringField('读者等级',[validators.DataRequired()])
	day = DateTimeField('办理时间', [validators.DataRequired()])
	#password = StringField('密码',[validators.DataRequired()])

class readerchange_Form(Form):
	Reader_id = StringField('读者编号', [validators.DataRequired()])
	mobile = StringField('手机',[validators.DataRequired()])
	level = StringField('读者等级',[validators.DataRequired()])

class rcpwd_Form(Form):
	pwd = StringField('手机', [validators.DataRequired()])
	pwdagain = StringField('读者等级', [validators.DataRequired()])

class loss_Form(Form):
	Reader_id = StringField('读者编号', [validators.DataRequired()])
	Loss_date = DateTimeField('挂失时间', [validators.DataRequired()])


@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/borrow_manager",methods=['GET','POST'])
def borrow_manager():
	error = None
	form = Borrow_Form(request.form)
	if session['name'] == 'admin':
		if request.method == 'POST':
			if request.form['Operation'] == 'borrow':
				B_reader = Reader.query.filter_by(reader_name=form.borrow_name.data).first()
				r_loss = loss_reporting.query.filter_by(Reader_id=B_reader.Reader_id)
				if not r_loss:
					B_book = book.query.filter_by(book_name=form.borrow_book.data).first()
					if B_book.Quanity_in - B_book.Quanity_out > 0:
						newborrow = borrow(Reader_id=B_reader.Reader_id,
										   Book_id=B_book.Book_id,
										   Date_borrow=form.Date_borrow.data,
										   loss='否')
						db.session.add(newborrow)
						B_book.Quanity_out += 1
						B_book.Quanity_in -= 1
						db.session.add(B_book)
						error = 'Operation succeeded'
				else:
					error = 'reader card is loss'
			elif request.form['Operation'] == 'return':
				B_book = book.query.filter_by(book_name=form.borrow_book.data).first()
				B_reader = Reader.query.filter_by(reader_name=form.borrow_name.data).first()
				B_borrow = borrow.query.filter_by(Book_id=B_book.Book_id, Reader_id=B_reader.Reader_id).first()
				if B_borrow:
					B_borrow.Date_return = form.Date_borrow.data
					db.session.add(B_borrow)
					B_book.Quanity_out -= 1
					B_book.Quanity_in += 1
					db.session.add(B_book)
					error = 'Operation succeeded'
				else:
					error = 'Operation failed'
			else:
				B_reader = Reader.query.filter_by(reader_name=form.borrow_name.data).first()
				B_book = book.query.filter_by(book_name=form.borrow_book.data).first()
				B_borrow = borrow.query.filter_by(Book_id=B_book.Book_id, Reader_id=B_reader.Reader_id).first()
				if B_borrow:
					B_borrow.loss = '是'
					db.session.add(B_borrow)
					B_book.Quanity_loss += 1
					db.session.add(B_book)
					error = 'Operation succeeded'
				else:
					error = 'Operation failed'
	else:
		return redirect(url_for('no_permision'))
	return render_template('borrow_manager.html',form = form,error = error)


@app.route("/manager")
def manager():
	return render_template('manager.html')

@app.route("/register",methods=['GET','POST'])
def register():
	if session['name'] == 'admin':
		error = None
		form = register_Form(request.form)
		if request.method=='POST':
			NewReader = Reader(Reader_id = form.Reader_id.data,
						   reader_name = form.reader_name.data,
						   sex = form.sex.data,
						   birthday = form.birthday.data,
						   phone = form.phone.data,
						   mobile = form.mobile.data,
						   card_name = form.card_name.data,
						   Card_id = form.Card_id.data,
						   level = form.level.data,
						   day = form.day.data,
						   password = form.Reader_id.data)
			db.session.add(NewReader)
			error = 'Operation succeeded'
	else:
		return redirect(url_for('no_permision'))
	return render_template('register.html',form=form,error = error)


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


@app.route("/login",methods=['GET','POST'])
def login():
	error = None
	myForm=LoginForm(request.form)
	session['name'] = myForm.username.data
	if request.method =='POST':
		check_reader = Reader.query.filter_by(Reader_id =myForm.username.data ).first()
		if (check_reader.password  == myForm.password.data and myForm.username.data !='admin'):
			return redirect(url_for('user'))
		elif (check_reader.password  == myForm.password.data and myForm.username.data =='admin'):
			return redirect(url_for('manager'))
		else:
			error = 'failed'
	return render_template('user_login1.html',form=myForm,error = error)

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

@app.route('/reader/reader_change_pwd', methods=['GET', 'POST'])
def reader_ch_pwd():
	error = None
	form = rcpwd_Form(request.form)
	if request.method == 'POST':
		reader_change_pws = Reader.query.filter_by(Reader_id = session['name']).first()
		if form.pwd.data == form.pwdagain.data:
			reader_change_pws.password = form.pwd.data
			error = 'Operation succeeded'
		else:
			error = 'twice diffirence'
	return render_template('reader_change_pwd.html',form = form,error = error)

@app.route('/loss', methods=['GET', 'POST'])
def loss():
	error = None
	form = loss_Form(request.form)
	if session['name'] == 'admin':
		if request.method == 'POST':
			reader_loss = Reader.query.filter_by(Reader_id=form.Reader_id.data).first()
			if reader_loss:
				newloss = loss_reporting(Reader_id=form.Reader_id.data,
										 Loss_date=form.Loss_date.data)
				db.session.add(newloss)
				error = 'Operation succeeded'
			else:
				error = 'Operation failed'
	else:
		return redirect(url_for('no_permision'))
	return render_template('loss.html',form = form,error = error)

@app.route("/book_manager",methods=['GET','POST'])
def book_manager():
	if session['name'] == 'admin':
		bookm = book.query.all()
	else:
		return redirect(url_for('no_permision'))
	return render_template('book_manager.html',bookm = bookm)


@app.route("/book_change/<bookid>",methods=['GET','POST'])
def book_change(bookid):
	pass
	return render_template('no_permission.html')


@app.route("/reader_change",methods=['GET','POST'])
def reader_change():
	if session['name'] == 'admin':
		error = None
		form = readerchange_Form(request.form)
		change_Reader = Reader.query.filter_by(Reader_id = form.Reader_id.data).first()
		if request.method=='POST':
			change_Reader.mobile = form.mobile.data
			change_Reader.level = form.level.data
			db.session.add(change_Reader)
			error = 'Operation succeeded'
	else:
		return redirect(url_for('no_permision'))
	return render_template('reader_change.html',form = form,error = error)

@app.route("/user_manager",methods=['GET','POST'])
def user_manager():
	return render_template('user_manager.html')


@app.route("/no_permision",methods=['GET','POST'])
def no_permision():
	return render_template('no_permission.html')


if __name__=="__main__":
	app.run()
