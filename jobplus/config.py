class BaseConfig:
    SECRET_KEY = 'a random secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql://root@127.0.0.1:3306/jobplus'


class ProductConfig(BaseConfig):
    pass


config = {
    'dev': DevConfig(),
    'product': ProductConfig()
}
