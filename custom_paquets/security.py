import base64
import hashlib
import bcrypt
from configparser_crypt import ConfigParserCrypt


def encrypt_password(password):
    return bcrypt.hashpw(get_b64(password), bcrypt.gensalt(13))


def compare_passwords(new_passw, old_passwd):
    old_passwd = bytes(old_passwd, 'utf-8')
    return bcrypt.checkpw(get_b64(str(new_passw)), old_passwd)


def get_b64(password):
    return base64.b64encode(hashlib.sha256(password.encode('utf_8')).digest())


def generate_key():
    conf_file = ConfigParserCrypt()
    conf_file.generate_key()
    aes_key = conf_file.aes_key
    out_file = open("key.encrypt", "wb")
    out_file.write(aes_key)
    out_file.close()
    
    
def encrypt_file(db_password):   
    conf_file = ConfigParserCrypt()
    in_file = open("key.encrypt", "rb") 
    key = in_file.read() 
    in_file.close()
    conf_file.aes_key = key
    
    conf_file.add_section('DBS')
    conf_file['DBS']['db_password'] = db_password
    
    with open('dbs.encrypted', 'wb') as file_handle:
        conf_file.write_encrypted(file_handle)
        