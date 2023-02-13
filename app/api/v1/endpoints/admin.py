import datetime
from http.client import HTTPException

from app.api.v1.validator import if_request_valid
from app.auth.auth_bearer import JWTBearer
from app.utilities.common import hash_password, validate_access
from logger import *

from fastapi import APIRouter, Request, Depends, Header

from app.auth.auth_handler import signJWT, decodeJWT
from app.model.admin import *
from app.utilities.exceptions.message import dbErrCode, dbErrMsg
from app.utilities.response import returnResponse
from app.utilities import SqlClient
from typing import Union

router = APIRouter()
responseHandler = returnResponse()


@router.post("/register", dependencies=[Depends(JWTBearer()), Depends(validate_access)])
async def admin_register(data_obj: AdminSchema, authorization: Union[str, None] = Header(default=None)):
    registered_by = decodeJWT(authorization.replace('Bearer ', ''))['email']
    db_conn = SqlClient.dbMysql()
    password = hash_password(data_obj.password).decode('utf-8')
    query = f"INSERT INTO `admin` VALUES (NULL, '{data_obj.email}', '{data_obj.phone}', '{password}', '{datetime.datetime.now()}', '{registered_by}', " \
            f"'{data_obj.accountStatus}', '{data_obj.role}');"
    logging.info(query)
    data = db_conn.INSERT(query)
    db_conn.close()
    return_code = return_msg = None
    if 'failed' in data.keys():
        logging.error(f"Admin register - '{data['error']}'")
        return_code = dbErrCode.ACCOUNT_CREATION
        return_msg = dbErrMsg.ACCOUNT_CREATION
    logging.info(f"Admin register success- '{data_obj.email}'")
    return responseHandler.responseBody(status_code=return_code, msg=return_msg)


@router.post("/user/is-exist")
async def check_if_user_exist(request: Request):
    body = await request.json()
    registration_id = body['reg_id']
    db_conn = SqlClient.dbMysql()
    data = db_conn.if_exist('users', ['regId'], [registration_id])
    db_conn.close()
    return data


