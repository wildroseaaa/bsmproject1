from passlib.context import CryptContext

number_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def crypt(number: str):
        return number_cxt.hash(number)