#-*-coding:utf-8
from app import app
from flask import render_template, flash, redirect,g,url_for, abort,request,session,jsonify
from models import *
import functools
import os
import json
from werkzeug import secure_filename
from security import ts,sendmail
from verificationCode import ImageChar,RandomChar


def use(func):
	@functools.wraps(func)
	def wrapper(*args,**kw):
		if 'user' in session:
			return func(*args,**kw)
		else:
			return redirect(url_for('login'))
	return wrapper

def admin(func):
	@functools.wraps(func)
	def wrapper(*args,**kw):
		if 'admin' in session:
			return func(*args,**kw)
		else:
			return redirect(url_for('adminLogin'))
	return wrapper
#主页
@app.route('/')
@app.route('/<int:index>')
def index(index=1):
	p = Page(get_count('videos'),index)
	news = get_videos(p.offset,p.limit)
	return render_template('index.html',page=p,news=news)

@app.route('/adminLogin',methods=["GET","POST"])
def adminLogin():
	if request.method=="POST":
		if checkAdmin(request.form):
			session['admin'] = request.form['name']
			return redirect(url_for('adminManage'))
	return render_template('adminLogin.html')

#管理@admin
@app.route('/admin')
@admin
def adminManage():
	return render_template('admin.html')
#视频播放页
@app.route('/v/<video_id>')
def v(video_id):
	video_address = get_vidoe_address(video_id)
	return render_template('v.html',video_address=video_address)

#注册
@app.route('/register',methods=['GET','POST'])
def register():
	if request.method=="POST":
		createUser(request.form)
		token = ts.dumps(request.form['email'],salt='weiyi-confirm-key')
		confirm_url = url_for('confirm_email',token=token,_external=True)
		html = render_template(
			'activate.html',confirm_url=confirm_url)
		sendmail(html,request.form['email'],u'验证邮件')
		return redirect(url_for('login'))
	return render_template('register.html')

#验证邮箱
@app.route('/confirm/<token>')
def confirm_email(token):
	try:
		email = ts.loads(token,salt="weiyi-confirm-key", max_age=86400)
	except:
		abort(404)
	db_confirm(email)
	return redirect(url_for('index'))


@app.route('/change_paw/<token>',methods=['GET','POST'])
def change_paw(token):
	try:
		email = ts.loads(token,salt="weiyi-confirm-key", max_age=86400)
	except:
		abort(404)
	if request.method=="POST":
		db_change_paw(email,request.form['password'])
		return redirect(url_for('index'))
	return render_template('change_paw2.html')

#修改密码
@app.route('/changepassword',methods=['GET','POST'])
def changepassword():
	if request.method=="POST":
		email = request.form['email']
		token = ts.dumps(email,salt='weiyi-confirm-key')
		confirm_url = url_for('change_paw',token=token,_external=True)
		html = render_template(
			'activate.html',confirm_url=confirm_url)
		sendmail(html,request.form['email'],u'修改密码')
		return redirect(url_for('index'))
	return render_template('change_paw.html')

#登录
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=="POST":
		if checkUser(request.form):
			session['user'] = request.form['email']
			return redirect(url_for('private'))
	return render_template('login.html')

#登出
@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('index'))


#登出
@app.route('/adminLogout')
def adminLogout():
	session.pop('admin', None)
	return redirect(url_for('index'))

#文件上传
ALLOWED_EXTENSIONS = set(['jpg','jpeg','png','gif','bmp','flv','mp4','swf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS 

@app.route("/api/upload",methods=['POST'])
def fileUpload():
    if request.method =="POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return '/static/images/'+filename
    return "0"

@app.route('/addVideo',methods=["GET","POST"])
def addVideo():
	if request.method=="POST":
		return create_video(request.form)
	return render_template('addvideo.html')
#视频文件上传
@app.route('/uploadvideo',methods=['GET','POST'])
def upload_video():
	if request.method=="POST":
		address = ''
		for i in range(len(request.files)):
			file = request.files['file'+str(i)]
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['VIDEO_FOLDER'],filename))
				address +='/static/video/'+filename+'|'
		address = address[:-1].strip()
		try:
			return up_video(address)
		except:
			return u"错误"
	return render_template('videoupload.html')
#直接添加地址
@app.route('/add_address',methods=["GET","POST"])
def add_address():
	if request.method=="POST":
		print '1'
		print request.form['address']
		try:
			return up_video(request.form['address'])
		except:
			return u"错误"
	return render_template('add_address.html')

@app.route('/view/<title>')
def view(title):
	content = get_video(title)
	return render_template('view.html',content=content)

@app.route('/search')
def search():
	keyword=request.args.get('keyword').encode('utf-8')
	index = request.args.get('index') if request.args.get('index') else 1
	count = get_keyword_count(keyword)
	p = Page(count,index)
	content=search_by_keyword(keyword,p.offset,p.limit)
	return render_template('search.html',keyword=keyword,page=p,content=content,count=count)

@app.route('/VerifyCode/<int:time>')
@app.route('/VerifyCode/')
def verify_code(time=0):
	ver_code = RandomChar.ascii()
	ver_img = ImageChar(rand_str=ver_code)
	response = app.make_response(ver_img.ShowStrIO())
	response.headers['Content-Type'] = 'image/png'
	return response