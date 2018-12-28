from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict


def create_app(model):
	"""
	将app相关联的配置封装到"工厂方法"中
	
	:param model:
	:return:
	"""
	app = Flask(__name__)
	Config = config_dict[model]
	app.config.from_object(Config)
	db = SQLAlchemy(app)
	# 创建redis数据库对象
	redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
	csrf = CSRFProtect(app)
	
	# 借助Session将flask的session进行存储
	# if config['SESSION_TYPE'] == 'redis':
	# 	session_interface = RedisSessionInterface(
	# 		config['SESSION_REDIS'], config['SESSION_KEY_PREFIX'],
	# 		config['SESSION_USE_SIGNER'], config['SESSION_PERMANENT'])
	Session(app)
	return app
