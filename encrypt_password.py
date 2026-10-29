import hashlib
def encrypt_password(password):
    salt = '5gz'
    pwd_salt = password + salt
    hash = hashlib.sha256(pwd_salt.encode())
    return hash.hexdigest()