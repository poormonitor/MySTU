import os

database = os.path.join(os.path.dirname(__file__), "data.sqlite")


class Config(object):
    JWT_SECRET_KEY = "hard_to_guess_string"
    SEND_FILE_MAX_AGE_DEFAULT = 2592000
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEIXIN_APPID = "wx1234567890abcdef"
    WEIXIN_APPSECRET = "weixinsecret"
