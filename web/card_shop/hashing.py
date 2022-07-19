from argon2 import PasswordHasher

def hash_password(password:str) -> str:
    ph = PasswordHasher()
    return ph.hash(password)

def check_hash(hash:str, password:str) -> bool:
    ph = PasswordHasher()
    try:
        ph.verify(hash, password)
        return True
    except:
        return False

if __name__ == '__main__':
    hash = hash_password('test')
    print(len(hash))
    print(hash)
    print(check_hash(hash, 'test1'))
    print(check_hash(hash, 'test'))