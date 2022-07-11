class DevConfig(object):
    SECRET_KEY = 'your_secret_key'
    CONFIG_TYPE = 'Development'
    WEBSITE_TITLE = 'BSBT-Interface'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='sqlite:///../comparative_judgements.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(object):
    SECRET_KEY = 'toady57isproduction62'
    CONFIG_TYPE = 'Production'
    SQLALCHEMY_DATABASE_URI='sqlite:///../comparative_judgements.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
