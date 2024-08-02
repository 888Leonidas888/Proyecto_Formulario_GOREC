from fastapi import APIRouter, HTTPException
from app.db.storage import Database
from typing import Optional, Union
from app.schemas.user import User, UserCreate, UsersList, UserUpdate
from app.schemas.message import Message

router = APIRouter()
table_users = 'users'


@router.get('/', response_model=Union[UsersList, User, list[None]])
def read_users(id_user: Optional[int] = None):
    try:
        db = Database()
        db.connect()

        if id_user:
            user = db.read(table_users, id=id_user)
            if len(user) == 0:
                raise HTTPException(status_code=404,
                                    detail=f'User with id {id_user} not fount.')
            return user[0]
        else:
            users = db.read_all(table_users)
            return {'users': users}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Internal server error {str(e)}')
    finally:
        db.disconnect()


@router.post('/', response_model=Message)
def create_users(user: UserCreate):
    new_user = user.model_dump()

    try:
        db = Database()
        db.connect()
        db.create(table_users, **new_user)
        db.connection.commit()
        return {'message': f'User {user.user} created'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f'Internal server error {str(e)}')
    finally:
        db.disconnect()


@router.delete('/', response_model=Message)
def delete_users(id_user: int):
    try:
        with Database() as db:
            db.delete(table_users, id=id_user)
        return {'message': f'User with id {id_user} was deleted.'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{str(e)}')


@router.put('/')
def update_users(id_user: int, user: UserUpdate):
    update_user = user.model_dump(exclude_unset=True)

    params_user = {
        'id': id_user
    }

    try:
        with Database() as db:
            user = db.read(table_users, id=id_user)
            if len(user) == 0:
                raise HTTPException(status_code=404,
                                    detail=f'User with id {id_user} not fount.')
            db.update(table_users, params_user, **update_user)
        return {'message': f'User with {id_user} was updated.'}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'{str(e)}')
