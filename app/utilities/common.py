import logging

import bcrypt
from fastapi import HTTPException, Header, Request
from typing import Union

from app.api.v1.validator import responseHandler
from app.auth.auth_handler import decodeJWT
from app.utilities import SqlClient
from app.utilities.exceptions.message import dbErrCode, dbErrMsg


def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def validate_hashed_password(password: str, hashed_password: bytes):
    # returns True or False
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def __check_if_access_allowed(data, invoker_id, invoker_role):
    is_disabled = data['is_disabled']
    blocked_users = data['blocked_user_id'].split(',')
    allowed_roles = data['allowed_roles'].split(',')
    if is_disabled:
        logging.error('endpoint disabled')
        raise HTTPException(status_code=404, detail="endpoint disabled")
    if invoker_id in blocked_users:
        logging.error('Forbidden - user blocked')
        raise HTTPException(status_code=403, detail="Forbidden - user blocked")
    if invoker_role not in allowed_roles:
        logging.error('Forbidden - not enough privileges')
        raise HTTPException(status_code=400, detail="Forbidden - not enough privileges")
    return True


def validate_access(request: Request, authorization: Union[str, None] = Header(default=None)):
    db_conn = SqlClient.dbMysql()
    invoked_ep = str(request.url).split('v1')[1]
    query = f"SELECT * from ep_control_settings WHERE endpoint  = '{invoked_ep}'"
    data = db_conn.SELECT(query)
    db_conn.close()
    if not data['data']:
        logging.warning(f"Invalid endpoint")
        return responseHandler.responseBody(status_code=dbErrCode.INVALID_EP, msg=dbErrMsg.INVALID_EP)
    token_items = decodeJWT(authorization.replace('Bearer ', ''))
    invoker_id = token_items['email']
    invoker_role = token_items['role']
    #
    if __check_if_access_allowed(data['data'][0], invoker_id, invoker_role):
        return True
    #


