#-*-coding:utf-8 -*-
import MySQLdb

def get_conn():
	db = MySQLdb.connect(host="127.0.0.1",\
		user="root",passwd="new_pass",\
		db="leimu",charset='utf8')
	return db

def run():
	sql1 = "create table users (name varchar(255),email varchar(255),password varchar(255))"
	sql2 = "insert into users (name,email,password) values('weiyi','393129389@qq.com','123');"
	sql3 = "create table admins(name varchar(30),password varchar(50));"
	sql4 = "insert into admins (name,password) values('weiyi','19940428');"
	sql5 = "create table videoaddress(id int not null primary key auto_increment,address varchar(255) not null);"
	sql6 = "create table videos(title varchar(255) PRIMARY KEY,image varchar(255),content varchar(4096),time datetime)"
	try:
		conn = get_conn()
		print "connect......"
		cur = conn.cursor()
		cur.execute(sql1)
		print "sql1"
		cur.execute(sql2)
		print "sql2"
		cur.execute(sql3)
		print "sql3"
		cur.execute(sql4)
		print "sql4"
		cur.execute(sql5)
		print "sql5"
		cur.execute(sql6)
		print "sql6"
		conn.commit()
	finally:
		cur.close()
		conn.close()

run()