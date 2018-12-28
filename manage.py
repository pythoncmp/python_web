from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, redis_store
import logging
from flask import current_app

app = create_app("development")
# 6将app交给管理对象管理
manager = Manager(app)
# 87数据库迁移初始化
Migrate(app, db)
# 8添加迁移命令
manager.add_command("db", MigrateCommand)


@app.route("/")
def index():
	print("////////////" + redis_store.keys())
	logging.debug("debug信息")
	logging.info("info信息")
	logging.warning("warning信息")
	logging.error("error信息")
	logging.critical("critical信息")
	
	current_app.logger.debug("flask记录debug信息")
	return "hello"


if __name__ == '__main__':
	# 9使用manager对象启动项目代替app.run
	manager.run()
