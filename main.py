# from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.interceptors.AuthInterceptor import AuthInterceptor
from app.interceptors.ExcHandler import ExcHandler
from fastapi import FastAPI
from app.routers import ScheduleDecisionRouter, TestRouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Create Exception Handler
exceptionHandler = ExcHandler(app)
exceptionHandler.turn_on()

authInterceptor = AuthInterceptor(app)
authInterceptor.turn_on()

# Include routers
app.include_router(ScheduleDecisionRouter.router)
app.include_router(TestRouter.router)
