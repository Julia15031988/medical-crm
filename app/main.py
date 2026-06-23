#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from app.routers import auth_register_login

app = FastAPI()
app.include_router(auth_register_login.router)
