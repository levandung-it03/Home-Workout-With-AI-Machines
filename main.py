# from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from app.app_sql import initialize_data
from app.app_sql.setup_database import Base, engine
from app.interceptors.AuthInterceptor import AuthInterceptor
from app.interceptors.ExcHandler import ExcHandler
from fastapi import FastAPI
from app.routers import ScheduleDecisionRouter, TestRouter
from app.services.business import ScheduleDecisionService


# Initialize data
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize models
    Base.metadata.create_all(bind=engine)
    ScheduleDecisionService.schedule_decision_model_preparation_on_startup()
    #Initialize data
    await initialize_data.run()
    yield

app = FastAPI(lifespan=lifespan)
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