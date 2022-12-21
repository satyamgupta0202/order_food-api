from fastapi import APIRouter,Depends
from models import User
from schema import UserModel , LoginModel
from database import Base ,Session,engine
from fastapi.exceptions import HTTPException
from werkzeug.security import check_password_hash,generate_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.encoders import jsonable_encoder

session = Session(bind = engine)

auth_router = APIRouter(
    prefix = '/auth',
    tags=["auth"]
)


@auth_router.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail="token not provided/invalid")
    return {"welcome  vro"}


@auth_router.post('/signup' , status_code=201)
async def register(user: UserModel):

# username
    username = session.query(User).filter(User.username == user.username).first()
    if  username is not None:
        return HTTPException(status_code=400 , detail="username already exist")

# email
    email = session.query(User).filter(User.email == user.email).first()
    if  email is not None:
        return HTTPException(status_code=400 , detail="email already exist")


    new_user = User(
        username = user.username , 
        email = user.email,
        password = generate_password_hash(user.password),
        is_active = user.is_active,
        is_staff = user.is_staff
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

    

@auth_router.post('/login')
def login(user: LoginModel , Authorize: AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password , user.password):

        access_token = Authorize.create_access_token(subject = db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        return jsonable_encoder(response)

    return HTTPException(status_code=400 , detail="Username or password invalid")