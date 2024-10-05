from fastapi import FastAPI

from app.interceptors.AuthInterceptor import AuthInterceptor
from app.interceptors.ExcHandler import ExcHandler
from app.routers import ScheduleDecision

app = FastAPI()

# Create Exception Handler
exceptionHandler = ExcHandler(app)
exceptionHandler.turn_on()

authInterceptor = AuthInterceptor(app)
authInterceptor.turn_on()

# Include routers
app.include_router(ScheduleDecision.router)