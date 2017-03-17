#coding:utf-8

from flask import Flask
app = Flask(__name__)
app.debug = True
app.secret_key = "ggj$&@!#6!5a46dqwc$pinhtfd6h$#~jg:"

UPLOAD_FOLDER = 'E:/sae/www/app/static/images/'#服务端改为/srv/www/app/static/images/
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
VIDEO_FOLDER = 'E:/sae/www/app/static/video'
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
from app import views