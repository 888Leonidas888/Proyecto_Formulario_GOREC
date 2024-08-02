
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.DB_Manager import Database
from datetime import datetime, timedelta
from jose import jwt, JWTError
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')

oauth_schema = OAuth2PasswordBearer('/token')

def get_user(table, username):
    params = {'user': username}
    if username:
        database = Database()
        database.connect()
        result = database.read(table, **params)
        keys_to_remove = ['updated_at', 'created_at']
        structured_data = map(lambda x: {key: value for key, value in x.items() if key not in keys_to_remove}, result)
        structured_data = list(structured_data)
        database.disconnect()
        return (structured_data[0])
    else:
        raise Exception(f"Username {username} not found on DB")
    
def verify_password(form_pass, db_pass):
    if form_pass == db_pass:
        return True
    else:
        return False

def auth_user(table, username, password):
    user = get_user(table, username)
    if not user:
        raise HTTPException(status_code=401,
                            detail=f'Couldnt authenticate', headers={'WWW-Authenticate': "Bearer"})
    if not verify_password(password, user['password']):
        raise HTTPException(status_code=401,
                            detail=f'Couldnt authenticate', headers={'WWW-Authenticate': "Bearer"})
    return user
    
def create_token(data, time_expire):
    data_copy = data.copy()
    if time_expire is None:
        expire = datetime.utcnow() + timedelta(minutes=15)
    else:
        expire = datetime.utcnow() + time_expire
    data_copy.update({"exp": expire})
    token_JWT = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_JWT

async def get_current_user(token = Depends(oauth_schema)):
    try:
        token_decode = jwt.decode(token, key= SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode['sub']
        if username == None:
            raise HTTPException(status_code=401,
                            detail=f'Couldnt authenticate', headers={'WWW-Authenticate': "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401,
                            detail=f'Couldnt authenticate', headers={'WWW-Authenticate': "Bearer"})
    # Change the table of needed
    user = get_user('users', username)
    if not user:
        raise HTTPException(status_code=401,
                            detail=f'Couldnt authenticate', headers={'WWW-Authenticate': "Bearer"})
    return user

async def get_admin_user(current_user = Depends(get_current_user)):
    if current_user.get('permission') != 'administrador':
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user