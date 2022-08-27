from werkzeug.exceptions import HTTPException


class UnKnownError(HTTPException):
    name = 'UnKnownError'
    code = 200
    error_code = 4000
    description = 'Something went wrong, Please try after sometime.'

