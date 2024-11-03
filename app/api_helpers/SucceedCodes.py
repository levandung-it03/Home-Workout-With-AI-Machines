from http import HTTPStatus


class BodyCode:
    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.httpStatus = HTTPStatus.OK


class SucceedCodes:
    AUTHENTICATION = BodyCode(21001, "Authenticate successfully")
    CAL_BODY_FAT = BodyCode(31001, "Calculate Body Fat successfully")
    SCHEDULE_DECISION = BodyCode(31002, "Decide Recommend Schedule successfully")
    ADD_SCHEDULE_DATALINE = BodyCode(31003, "Add new Schedule dataline successfully")
    EXPORT_SCHEDULE_CSV = BodyCode(31004, "Export schedule dataset from DB to CSV successfully")
    GET_SCHEDULE_DATASET_PAGES = BodyCode(31005, "Get schedule dataset pages from DB successfully")
    DELETE_SCHEDULE_DATALINE = BodyCode(31006, "Delete dataline successfully")
