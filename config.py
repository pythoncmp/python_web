from redis import StrictRedis


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
	# 具体将session中的数据储存到哪个redis数据库对象
	SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=1)
	# session储存的数据后产生的session_id需要加密
	SESSION_USE_SIGNER = True
	# 设置非永久储存
	SESSION_PERMANENT = False
	# 设置session过期时长,默认过期时长:31天
	PERMANENT_SESSION_LIFETIME = 86400


class DevelopmentConfig(Config):
	DEBUG = True


class ProductionConfig(Config):
	DEBUG = False


# 给外界提供一个接口
config_dict = {
	"development": DevelopmentConfig,
	"production": ProductionConfig
}
