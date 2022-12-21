from fastapi import FastAPI
from auth_routes import auth_router
from oder_routes import order_router
from fastapi_jwt_auth import AuthJWT
from schema import Settings

app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)
@app.get('/')
async def hello():
    return {"welcome vro"}

@AuthJWT.load_config
def get_config():
    return Settings()