from fastapi import FastAPI, Request

from app.api_helpers.ApiResponse import ApiResponse
from app.api_helpers.CustomeExc import ApplicationException
from app.api_helpers.ErrorCodes import ErrorCodes


class ExcHandler:
    def __init__(self, app: FastAPI):
        self.app = app

    def turn_on(self):
        self.application_exception_filter()
        self.unaware_exception_filter()

    def application_exception_filter(self):
        @self.app.exception_handler(ApplicationException)
        async def application_exception_handler(request: Request, exc: ApplicationException):
            response = ApiResponse(exc.errorCodes, None)
            return response

    def unaware_exception_filter(self):
        @self.app.exception_handler(Exception)
        async def unaware_exception_handler(request: Request, exc: Exception):
            response = ApiResponse(ErrorCodes.UNAWARE_ERR, None)
            return response