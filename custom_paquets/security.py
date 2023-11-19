import hashlib
import re


# Encrypt password with SHA512 and return it
def encrypt_password(password, pseudo):
    return hashlib.sha512((''.join(str(ord(c)) for c in pseudo)).encode('utf-8') + password.encode('utf-8')).hexdigest()

