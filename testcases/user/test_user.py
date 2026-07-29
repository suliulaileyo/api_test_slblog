import allure
import pytest

from core.ApiService import ApiService
from utils.YamlUtil import YamlUtil


@allure.feature("用户模块")
class TestUser:
    @pytest.mark.parametrize("data",YamlUtil().extract_case("user.yaml","user_login"))
    def test_user(self, data):
        print("测试demo")