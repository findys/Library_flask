from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import MySQLdb
from wtforms import *

app=Flask(__name__)

conn = MySQLdb.connect("123.206.23.69", "root", "10IDCcom", "Sql_Class")

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


@app.route("/register",methods=['GET','POST'])
def register():
	myForm=LoginForm(request.form)
	if request.method=='POST':
		insert(myForm.username.data,myForm.password.data)
		return redirect("http://www.findys.me")
	return render_template('user_login.html',form=myForm)

@app.route("/login",methods=['GET','POST'])
def login():
	myForm=LoginForm(request.form)
	if request.method =='POST':
		if (isExisted(myForm.username.data,myForm.password.data)):
			return redirect("http://www.findys.me")
		else:
			return "Login Failed"
	return render_template('user_login.html',form=myForm)

if __name__=="__main__":
	app.run(debug= True)