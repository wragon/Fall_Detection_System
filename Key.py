import hmac, hashlib, base64
import time


class Key:
    __sid = ""  # write your key
    __uri = None
    __url = None
    __sec_key = ""  # write your key
    __acc_key_id = ""  # write your key
    __acc_sec_key = b''  # write your key
    __stime = None
    __hash_str = None
    __digest = None
    __d_hash = None

    def __init__(self):
        self.__uri = "/sms/v2/services/{}/messages".format(self.__sid)
        self.__url = "https://sens.apigw.ntruss.com{}".format(self.__uri)
        self.__stime = int(float(time.time()) * 1000)
        self.__hash_str = "POST {}\n{}\n{}".format(self.__uri, self.__stime, self.__acc_key_id)
        self.__digest = hmac.new(self.__acc_sec_key, msg=self.__hash_str.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        self.__d_hash = base64.b64encode(self.__digest).decode()

    def get_key(self):
        return [self.__url, self.__stime, self.__acc_key_id, self.__d_hash]
