from passlib.context import CryptContext
            # hashing algorithm we are using
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated = "auto")

def hash(password: str):
    return pwd_context.hash(password)


# compare two hashes to verify
# 7
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
