import logging

from fastapi import APIRouter, Request

from app.utilities import SqlClient
from app.utilities.exceptions.message import dbErrCode, dbErrMsg
from app.utilities.response import returnResponse

router = APIRouter()
responseHandler = returnResponse()


# Using Request instance
@router.post("/register-ep")
def register_endpoints(request: Request):
    url_list = ','.join(route.path.replace('/api/v1','') for route in request.app.routes if '/api/' in route.path)
    db_conn = SqlClient.dbMysql()
    qry_value = ''
    for ep in url_list.split(','):
        qry_value+=f"('{ep}',0),"
    query = f"INSERT INTO `ep_control_settings`(`endpoint`,`is_disabled`) VALUES {qry_value[:-1]};"
    logging.info(query)
    data = db_conn.INSERT(query)
    db_conn.close()
    return_code = return_msg = None
    if 'failed' in data.keys():
        logging.error(f"Endpoint register - '{data['error']}'")
        return_code = dbErrCode.ENDPOINT_REGISTRATION
        return_msg = dbErrMsg.ENDPOINT_REGISTRATION
    logging.info(f"Endpoint registry updated'")
    return responseHandler.responseBody(status_code=return_code, msg=return_msg)

@router.get("/db-registered-ep")
def all_registered_endpoints_in_database():
    db_conn = SqlClient.dbMysql()
    query = f"SELECT * FROM `ep_control_settings`"
    logging.info(query)
    data = db_conn.SELECT(query)['data']
    db_conn.close()
    return data

@router.get("/app-registered-ep")
def all_registered_endpoints_on_application(request: Request):
    url_list = [{ "path": route.path.replace('/api/v1', '') }for route in request.app.routes if '/api/' in route.path]
    return url_list
