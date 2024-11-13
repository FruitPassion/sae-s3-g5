import base64
import hashlib

import bcrypt


def encrypt_password(password, salt=13):
    return bcrypt.hashpw(get_b64(password), bcrypt.gensalt(salt))


def compare_passwords(new_passw, old_passwd):
    if isinstance(old_passwd, str):
        old_passwd = bytes(old_passwd, "utf-8")
    return bcrypt.checkpw(get_b64(str(new_passw)), old_passwd)


def get_b64(password):
    return base64.b64encode(hashlib.sha256(password.encode("utf_8")).digest())
