import pytest

from utils.ExtractUtil import ExtractUtil


@pytest.fixture(scope="session")
def login_token():
    """获取登录认证 token，用于需要 ADMIN 权限的接口
    注意: 后端 JwtAuthenticationFilter 解析 Authorization: Bearer <token>
    登录接口需先执行，将 token 提取到 extract.yaml 中
    """
    token = ExtractUtil().get_extract_value("token")
    headers = {
        "Authorization": "Bearer " + token
    }
    return headers
