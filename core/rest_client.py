import json

import requests

from utils.log_util import logger
from utils.read import base_data

api_base_url = base_data.read_ini()['host']['api_site_url'] # 接口基地址

class RestClient:
    def __init__(self):
        self.api_base_url = api_base_url
        self.seesion = requests.Session()

    def do_request(self, url, method, **kwargs):
        response = self.request(url,method,**kwargs).json()
        logger.info("接口返回内容>>>\n{}".format(json.dumps(response, ensure_ascii=False, indent=2)))
        return response

    def request(self, url, method, **kwargs):
        self.request_log(url, method, **kwargs)
        if method == "GET":
            return self.seesion.get(self.api_base_url + url,**kwargs)
        if method == "POST":
            return self.seesion.post(self.api_base_url + url,**kwargs)
        if method == "PUT":
            return self.seesion.put(self.api_base_url + url,**kwargs)
        if method == "DELETE":
            return self.seesion.delete(self.api_base_url + url,**kwargs)
    def request_log(self, url, method, **kwargs):
        data = dict(**kwargs).get('data')
        json_data = dict(**kwargs).get('json')
        params = dict(**kwargs).get('params')
        headers = dict(**kwargs).get('headers')

        logger.info("接口请求的地址>>>{}".format(self.api_base_url + url))
        logger.info("接口请求的方法>>>{}".format(method))
        if data is not None:
            logger.info("接口请求的data参数>>>{}".format(json.dumps(data,ensure_ascii=False,indent=2)))
        if json_data is not None:
            logger.info("接口请求的json参数>>>{}".format(json.dumps(json_data,ensure_ascii=False,indent=2)))
        if params is not None:
            logger.info("接口请求的params参数>>>{}".format(json.dumps(params,ensure_ascii=False,indent=2)))
        if headers is not None:
            logger.info("接口请求的headers参数>>>{}".format(json.dumps(headers,ensure_ascii=False,indent=2)))

api_util = RestClient()