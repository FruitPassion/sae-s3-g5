import hashlib
import re


# Encrypt password with SHA512 and return it
def encrypt_password(password, pseudo):
    return hashlib.sha512((''.join(str(ord(c)) for c in pseudo)).encode('utf-8') + password.encode('utf-8')).hexdigest()


# Check if password is strong enough
# Returns a dict indicating the wrong criteria
# A password is considered strong if:
#     8 characters length or more
#     1 digit or more
#     1 symbol or more
#     1 uppercase letter or more
#     1 lowercase letter or more
# Found on :
# https://stackoverflow.com/questions/16709638/checking-the-strength-of-a-password-how-to-check-conditions#32542964
def password_strenght(password):
    length_error = len(password) < 12
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

    return {
        'password_ok': password_ok,
        'length_error': length_error,
        'digit_error': digit_error,
        'uppercase_error': uppercase_error,
        'lowercase_error': lowercase_error,
        'symbol_error': symbol_error,
    }
