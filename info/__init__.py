from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict
import logging
from logging.handlers import RotatingFileHandler

# 只是声明了db对象而已,并没有做真实的数据库初始化操作
db = SQLAlchemy()
# #type:StrictRedis 提前声明redis_store数据类型
redis_store = None  # type:StrictRedis


def write_log(Config):
	# 设置日志的记录等级
	logging.basicConfig(level=Config.LOG_LEVEL)  # 调试debug级
	# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
	file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
	# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
	formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
	# 为刚创建的日志记录器设置日志记录格式
	file_log_handler.setFormatter(formatter)
	# 为全局的日志工具对象（flask app使用的）添加日志记录器
	logging.getLogger().addHandler(file_log_handler)


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
	
	# 记录日志
	write_log(Config)
	
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
