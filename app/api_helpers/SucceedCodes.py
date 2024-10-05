from http import HTTPStatus


class BodyCode:
    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.httpStatus = HTTPStatus.OK


class SucceedCodes:
    AUTHENTICATION = BodyCode(21001, "Authenticate successfully")
    CAL_BODY_FAT = BodyCode(31001, "Calculate Body Fat successfully")
