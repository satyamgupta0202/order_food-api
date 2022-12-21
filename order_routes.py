from fastapi import APIRouter , Depends
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from database import engine , Base , Session
from schema import OrderModel , UserModel
from models import User , Order
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException


session = Session(bind = engine)

order_router = APIRouter(
    prefix = '/order',
    tags=["order"]
)


@order_router.get('/' , status_code=201)
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail= "Token is invalid/empty")
    return {"welcome order vro"}

@order_router.post('/order')
async def create_order(order: OrderModel , Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail= "Token is invalid/empty")

    # authorized to pakka hai ab
    currentUser = Authorize.get_jwt_subject()
    user = session.query(Order).filter(User.username == currentUser).first()

    new_order = Order(
        pizza_size= order.pizza_size,
        quantity=order.quantity,
    )

    new_order.user = user
    session.add(new_order)
    session.commit()

    response = {
        "pizza_size" :new_order.pizza_size,
        "quantity" : new_order.quantity,
        "id":new_order.id,    
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)
