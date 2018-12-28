from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import config_dict

app = Flask(__name__)
Config = config_dict["development"]
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
