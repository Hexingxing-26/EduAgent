import traceback
from database.connect import SessionLocal
from schemas.base import UserCreate
from api.user import register

print('python works')
try:
    import bcrypt
    print('bcrypt loaded', bcrypt.__version__)
except Exception as e:
    print('bcrypt import failed', type(e).__name__, e)

from auth.pwd_util import hash_password, verify_password
print('hash_password loaded')
try:
    h = hash_password('Test1234')
    print('hash success, len', len(h))
    print('verify', verify_password('Test1234', h))
except Exception as e:
    print('hash failed', type(e).__name__, e)

user = UserCreate(username='autotest_verify3', password='Test1234', nickname='auto', major='测试')
db = SessionLocal()
try:
    res = register(user, db=db)
    print('register success', res)
except Exception as e:
    print('register exception', type(e).__name__, e)
    traceback.print_exc()
finally:
    db.close()
