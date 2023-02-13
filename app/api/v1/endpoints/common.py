from app.model.common import *
from app.utilities.common import validate_hashed_password
from logger import *

from fastapi import APIRouter, Request

from app.auth.auth_handler import signJWT
from app.utilities.exceptions.message import dbErrCode, dbErrMsg
from app.utilities.response import returnResponse
from app.utilities import SqlClient
import bcrypt

router = APIRouter()
responseHandler = returnResponse()


@router.post("/login")
async def login(data_obj: LoginSchema):
    db_conn = SqlClient.dbMysql()
    email = data_obj.email
    query = f"SELECT email, password, role from admin WHERE email  = '{data_obj.email}'"
    data = db_conn.SELECT_LOGIN(query)
    db_conn.close()
    #
    if not data['data']:
        # no user found with given email
        logging.warning(f"Login failed - '{data['error']}'")
        return responseHandler.responseBody(status_code=dbErrCode.LOGIN_ATTEMPT_FAILED_EMAIL, msg=dbErrMsg.LOGIN_ATTEMPT_FAILED_EMAIL)
    #
    password = data['data'][0]['password']
    role = data['data'][0]['role']
    jwt_token = None
    return_code = return_msg = None
    if not validate_hashed_password(data_obj.password, password):
        return_code = dbErrCode.LOGIN_ATTEMPT_FAILED_PASSWORD
        return_msg = dbErrMsg.LOGIN_ATTEMPT_FAILED_PASSWORD
        logging.error(f"Login failed - {return_msg}")
    else:
        jwt_token = signJWT([email,role])
    return responseHandler.responseBody(status_code=return_code, msg=return_msg, jwt=jwt_token)

