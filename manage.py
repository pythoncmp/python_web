from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class Config(object):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/information"
	# 开启数据库跟踪模式
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	
	# redis配置信息
	REDIS_HOST = "192.168.188.140"
	REDIS_PORT = 6379
	
	# 使用session记得添加加密字符串对session_id加密
	SECRET_KEY = "ABCDEFG"
	
	# 将flask中的session存储到redis数据库的储存信息
	# 储存到哪种数据库
	SESSION_TYPE = "redis"
	# 具体将session中的数据粗处女到哪个redis数据库对象
	SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)
	# session储存的数据后产生的session_id需要加密
	SESSION_USE_SIGNER = True
	# 设置非永久储存
	SESSION_PERMANENT = False
	# 设置session过期时长,默认过期时长:31天
	PERMANENT_SESSION_LIFETIME = 86400


app = Flask(__name__)
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

# 6将app交给管理对象管理
manager = Manager(app)
# 87数据库迁移初始化
Migrate(app, db)
# 8添加迁移命令
manager.add_command("db", MigrateCommand)


@app.route("/")
def index():
	return "hello"


if __name__ == '__main__':
	# 9使用manager对象启动项目代替app.run
	manager.run()
