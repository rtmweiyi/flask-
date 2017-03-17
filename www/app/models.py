#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb

from MySQLdb import IntegrityError

class MyDatabase(object):
	def __enter__(self):
		self.db = MySQLdb.connect(host="127.0.0.1",\
		user="root",passwd="new_pass",\
		db="leimu",charset='utf8')
		self.cur = self.db.cursor()
		return self.cur
	def __exit__(self,*args):
		self.db.commit()
		self.cur.close()
		self.db.close()

class MyDatabaseNocommit(object):
	def __enter__(self):
		self.db = MySQLdb.connect(host="127.0.0.1",\
		user="root",passwd="new_pass",\
		db="leimu",charset='utf8')
		self.cur = self.db.cursor()
		return self.cur
	def __exit__(self,*args):
		self.cur.close()
		self.db.close()


def createUser(form):
	value = (form['username'],form['email'],form['password'])
	sql = "insert into users (name,email,password) values(%s,%s,%s);"
	with MyDatabase() as cur:
		cur.execute(sql,value)


def createAdmin(form):
	value = (form['username'],form['password'])
	sql = "insert into admins(name,password) values(%s,%s);"
	with MyDatabase() as cur:
		cur.execute(sql,value)

def checkAdmin(form):
	name = form['name']
	paw = form["password"]
	sql = "select password from admins where name=%s"
	with MyDatabase() as cur:
		cur.execute(sql,(name,))
		result = cur.fetchone()
		password = result[0]
		if paw==password:
			return True
		else:
			return False

def checkUser(form):
	idx = form['email']
	paw = form["password"]
	sql = "select password from users where email=%s"
	with MyDatabase() as cur:
		cur.execute(sql,(idx,))
		result = cur.fetchone()
		password = result[0]
		if paw==password:
			return True
		else:
			return False

def getallpaper(user):
	sql = "select class from users where id=%s"
	with MyDatabase() as cur:
		cur.execute(sql,(user,))
		result = cur.fetchone()
		sql2 = "select paper from bj%s"%result[0]
		cur.execute(sql2)
		result2 = cur.fetchall()
		return result2


def create_video(data):
	sql = "insert into videos(title,image,content,time)values(%s,%s,%s,NOW());"
	with MyDatabase() as cur:
		try:
			cur.execute(sql,(data['title'],data['image'],data['content']))
		except IntegrityError,e:
			return "文章标题已存在"
		except Exception, e:
			return "出错！"
		return u"ok"

def get_count(table):
	sql = "select count(1) from %s"%table
	with MyDatabase() as cur:
		cur.execute(sql)
		result = cur.fetchone()
	return int(result[0])

#存储公告分页信息的类
class Page(object):
	def __init__(self,item_count,page_index=1,page_size=10):
		self.item_count = item_count
		self.page_size = page_size
		self.page_count = item_count//page_size+(1 if item_count%page_size>0 else 0)
		if (item_count==0)or(page_index>self.page_count):
			self.offset = 0
			self.limit = 0
			self.page_index = 1
		else:
			self.page_index = page_index
			self.offset = self.page_size*(page_index-1)
			self.limit = self.page_size
		self.has_next = self.page_index<self.page_count
		self.has_previous = self.page_index>1

def get_videos(offset,limit):
	sql = "select title,image,DATE_FORMAT(time,'%%Y-%%c-%%d %%h:%%i:%%s') from videos order by time DESC LIMIT %s OFFSET %s;"
	with MyDatabase() as cur:
		cur.execute(sql,(limit,offset))
		result = cur.fetchall()
	return result
def get_video(title):
	sql = "select content from videos where title=%s;"
	with MyDatabaseNocommit() as cur:
		cur.execute(sql,(title,))
		result = cur.fetchone()
	return result

def up_video(address):
	sql = "insert into videoaddress (address)values(%s);"
	sql2 = "select id from videoaddress where address=%s;"
	with MyDatabase() as cur:
		cur.execute(sql,(address,))
		cur.execute(sql2,(address,))
		result = cur.fetchone()[0]
	return str(result)

def get_vidoe_address(video_id):
	sql = "select address from videoaddress where id=%s;"
	with MyDatabase() as cur:
		cur.execute(sql,(video_id,))
		result = cur.fetchone()[0]
	return str(result)

def search_by_keyword(keyword,offset,limit):
	keyword = keyword = "%"+keyword+"%"
	sql = "select title,image from videos where content like %s or title like %s order by time DESC LIMIT %s OFFSET %s;"
	with MyDatabase() as cur:
		cur.execute(sql,(keyword,keyword,limit,offset))
		result = cur.fetchall()
	return result

def get_keyword_count(keyword):
	keyword = "%"+keyword+"%"
	sql = u"select count(1) from videos where content like %s or title like %s;"
	with MyDatabase() as cur:
		cur.execute(sql,(keyword,keyword))
		result = cur.fetchone()[0]
	return result

