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
def create_order(order: OrderModel , Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail= "Token is invalid/empty")

    # authorized to pakka hai ab
    currentUser = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == currentUser).first()

    new_order = Order(
        pizza_size= order.pizza_size,
        quantity=order.quantity,
    )

    print(new_order)
    new_order.user = user
    session.add(new_order)
    session.commit()

    response = {
        "pizza_size":new_order.pizza_size,
        "quantity" : new_order.quantity,
        "id":new_order.id,    
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)

# get all order of specific user
@order_router.get('/getAll')
def getAllOrders(Authorize: AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail="id is Invalid/empty")
    
    # authorized tho hai
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff :
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=401 , detail="User must be super user to see all the orders")



# get particular order of specific user
@order_router.get('/getorder/{id}')
async def get_order_by_id(id:int , Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail="jwt is invalid/missing")

    # authorize tho ho gya
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    orders = session.query(Order).filter(Order.id == id).first()
    print(orders)
    return await jsonable_encoder(orders)

    # raise HTTPException(status_code=401 , detail="Invalid token/missing token")


# Get all orders of a specific user
@order_router.get('/user/orders')
def get_order_user(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    user=Authorize.get_jwt_subject()


    current_user=session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)

@order_router.get('/user/order/{id}')
async def get_order_user_with_id(id: int , Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail="jwt token is Invalid/Required")
    
    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    orders = user.orders

    for o in orders:
        if o.id == id:
            return o

    raise HTTPException(status_code=404 , detail="no such order found")


@order_router.put('/order/update/{id}')
async def update_order_with_id(id:int ,order:OrderModel, Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401 , detail="token is either empty or invalid")
    
    current_user = Authorize.get_jwt_subject()
    # user = session.query(User).filter(User.id == current_user).first()
    order_to_update= session.query(Order).filter(Order.id == id).first()
    
    order_to_update.quantity = order.quantity
    order_to_update.pizza_size=order.pizza_size
    
    session.commit()

    return jsonable_encoder(order_to_update)