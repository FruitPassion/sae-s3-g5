class DevConfig:
    SECRET_KEY = "3@$=)+Nj{HlH8E&u-43}K.~)C3JTSCL5L9a63_iH#UN6V4nd9d"
    ENVIRONMENT = "development"
    FLASK_APP = "Fiches"
    DEBUG = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECURITY_PASSWORD_SALT = "'xm=h}a-Lvf{R[]Hob8WRzC8bl@)m0RM4tfoRRuKAXMs(]uIuB"
    SQLALCHEMY_DATABASE_URI = 'mariadb://local_user:password@localhost:3306/db_fiches_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
