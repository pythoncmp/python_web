from info.modules.index import index_bp
from flask import current_app
from manage import redis_store


@index_bp.route("/")
def index():
	print(redis_store.keys())
	current_app.logger.debug("debug信息")
	return "index"
