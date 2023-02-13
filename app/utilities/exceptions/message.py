class ErrorCode:
    class db:
        ACCOUNT_CREATION = 1001
        LOGIN_ATTEMPT_FAILED_PASSWORD = 1002
        LOGIN_ATTEMPT_FAILED_EMAIL = 1003
        INVALID_EP = 1004
        ENDPOINT_REGISTRATION = 1005


class ErrorMsg:
    class db:
        ACCOUNT_CREATION = 'Unable to add account'
        LOGIN_ATTEMPT_FAILED_PASSWORD = 'Wrong password'
        LOGIN_ATTEMPT_FAILED_EMAIL = 'Invalid email'
        INVALID_EP = 'Invalid endpoint or endpoint no updated please contact with your admin'
        ENDPOINT_REGISTRATION = 'Unable to update endpoints in endpoint table'


dbErrCode = ErrorCode.db
dbErrMsg = ErrorMsg.db
