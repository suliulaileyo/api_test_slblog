# -*- coding:utf-8 -*-
"""
describe：SL Blog 登录接口自动化测试
author：AI 生成

测试覆盖场景：
  1. 正常登录     → code=200, message=登录成功, 提取 token
  2. 密码错误     → code=500, message=用户名或密码错误
  3. 用户名不存在 → code=500, message=用户名或密码错误
  4. 密码为空     → code=500, message=用户名或密码错误
  5. 用户名为空   → code=500, message=用户名或密码错误
  6. 均为空       → code=500, message=用户名或密码错误
"""
import allure
import pytest

from core.ApiService import ApiService
from utils.YamlUtil import YamlUtil


@allure.feature("用户模块")
@allure.story("登录功能")
class TestLogin:

    @pytest.mark.run(order=1)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("login.yaml", "blog_login")
    )
    def test_login(self, data):
        """SL Blog 登录接口测试 - 数据驱动"""
        ApiService().handle_case(data)
