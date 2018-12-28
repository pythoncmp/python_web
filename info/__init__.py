from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict

# 只是声明了db对象而已,并没有做真实的数据库初始化操作
db = SQLAlchemy()
# #type:StrictRedis 提前声明redis_store数据类型
redis_store = None  # type:StrictRedis


# 将app封装起来,给外界提供一个接口方法create_app

def create_app(model):
	"""
	将app相关联的配置封装到"工厂方法"中
	
	:param model:
	:return:
	"""
	app = Flask(__name__)
	Config = config_dict[model]
	app.config.from_object(Config)
	# 创建mysql数据库对象
	db.init_app(app)
	
	# 创建redis数据库对象(懒加载思想)
	global redis_store
	redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
	
	CSRFProtect(app)
	
	# 借助Session将flask的session进行存储
	# if config['SESSION_TYPE'] == 'redis':
	# 	session_interface = RedisSessionInterface(
	# 		config['SESSION_REDIS'], config['SESSION_KEY_PREFIX'],
	# 		config['SESSION_USE_SIGNER'], config['SESSION_PERMANENT'])
	Session(app)
	return app
