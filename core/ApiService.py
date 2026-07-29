import logging

import allure

from core.rest_client import RestClient
from utils.AssertUtil import AssertUtil
from utils.ExtractUtil import ExtractUtil


class ApiService:
    def __init__(self):
        self.session = RestClient() # 引入封装好的客户端请求方法
        self.extract = ExtractUtil() # 引入Extract工具类

    def handle_case(self, test_data, login_token=None):
        # 获取url
        url = self.extract.extract_url(test_data['request_info']['url'])
        # 获取method
        method = test_data['request_info']['method']
        # 获取headers
        headers = test_data['request_info']['headers']
        if login_token:
            headers.update(login_token) # 更新 headers（如添加 Authorization）
        # 获取用例标题，并动态设置到 Allure 报告
        base_title = test_data['request_info']['case_title']
        # 获取case_info
        case_info = test_data['case_info']
        # 先处理整个 case_info 中的动态变量（包括 validate）
        processed_case_info = self.extract.extract_case(case_info)
        # 取出 case_desc（如果存在），拼到标题里区分不同场景
        case_desc = processed_case_info.pop("case_desc", None)
        allure_title = f"{base_title} - {case_desc}" if case_desc else base_title
        allure.dynamic.title(allure_title) # 动态设置测试用例的标题，在 Allure 报告中显示
        # 获取validate和extract
        validate = processed_case_info.pop("validate", None)
        extract = processed_case_info.pop("extract", None)
        # 使用处理后的 case_info
        case_info = processed_case_info
        res = self.session.do_request(url=url, method=method, headers=headers, **case_info)
        # 将extract写入到yaml
        self.extract.extract_data(res, extract)
        # 断言逻辑
        AssertUtil().validate_response(res, validate)
        return res
