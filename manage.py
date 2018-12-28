from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, redis_store

app = create_app("development")
# 6将app交给管理对象管理
manager = Manager(app)
# 87数据库迁移初始化
Migrate(app, db)
# 8添加迁移命令
manager.add_command("db", MigrateCommand)


@app.route("/")
def index():
	redis_store.set("name", "laowang")
	return "hello"


if __name__ == '__main__':
	# 9使用manager对象启动项目代替app.run
	manager.run()
