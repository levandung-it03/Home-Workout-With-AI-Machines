from http import HTTPStatus


class BodyCode:
    def __init__(self, code, message, httpStatus):
        self.code = code
        self.message = message
        self.httpStatus = httpStatus


class ErrorCodes:
    # --Generals(10)
    UNAWARE_ERR = BodyCode(10000, "Unaware exception's thrown from resource server", HTTPStatus.BAD_REQUEST)
    VALIDATOR_ERR_RESPONSE = BodyCode(10001, "Invalid variable type or format of field \"${field}\"",
                                      HTTPStatus.BAD_REQUEST)
    PARSE_JSON_ERR = BodyCode(10002, "Invalid variable type or format of field '${field}'", HTTPStatus.BAD_REQUEST)
    # --Auth(11)
    INVALID_CREDENTIALS = BodyCode(11001, "Username or Password is invalid", HTTPStatus.UNAUTHORIZED)
    INVALID_TOKEN = BodyCode(11002, "Token or its claims are invalid", HTTPStatus.UNAUTHORIZED)
    EXPIRED_TOKEN = BodyCode(11003, "Token is expired", HTTPStatus.FORBIDDEN)
    FORBIDDEN_USER = BodyCode(11004, "User not found or access denied", HTTPStatus.BAD_REQUEST)
    LOGIN_SESSION_EXPIRED = BodyCode(11005, "Login session is expired, please login again", HTTPStatus.BAD_REQUEST)
