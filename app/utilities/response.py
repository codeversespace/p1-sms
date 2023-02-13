class returnResponse:

    def responseBody(self, status_code: int, msg: str = None, data: dict = {}, jwt: str = None):
        body = {}
        body["status"] = 'success'
        if status_code is None:
            status_code = 200
        body['code'] = status_code

        if status_code > 1000:
            body["reason"] = msg
            body["status"] = 'failed'

        if jwt is not None:
            body["authentication_token"] = jwt

        if bool(data):
            body["data"] = data
        return body
