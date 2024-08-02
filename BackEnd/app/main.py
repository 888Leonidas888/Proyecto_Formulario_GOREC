from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.oauth.token_manager import *
from app.api.v1.users import router as router_users

app = FastAPI()

app.title = 'API control de expedientes'
app.version = 'v0.0.1'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)


@app.get('/', tags=['home'])
def home():
    return {'end_point': ['http://127.0.0.1:8000/api/v1/users']}


@app.post('/token', tags=['oauth'])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user('users', form_data.username, form_data.password)
    # Check if user is correct
    print(user)
    access_token_expire = timedelta(hours=8)
    access_token_JWT = create_token({"sub": user['user']}, access_token_expire)
    # Data from form
    print(form_data.username, form_data.password)
    return {
        "access_token": access_token_JWT,
        "token_time": "bearer"
    }


# app.include_router(router_users, prefix='/api/v1',
#                    tags=['users'], dependencies=[Depends(get_admin_user)])
app.include_router(router_users, prefix='/api/v1/users', tags=['users'])
