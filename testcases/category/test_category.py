# -*- coding:utf-8 -*-
"""
describe：SL Blog 分类模块 - 后台接口自动化测试
author：AI 生成

测试覆盖场景：
  1. 分类列表查询（默认分页/关键词搜索/自定义分页）  → code=200, 提取分类ID
  2. 分类详情查询（存在/不存在）                    → code=200 / code=500
  3. 新增分类（正常/重名/空名称）                   → code=200 / code=500
  4. 编辑分类（正常/重名）                          → code=200 / code=500
  5. 批量删除分类（正常清理/含默认分类拦截）         → code=200 / status=400
  6. 单个删除分类（不存在/下有文章）                → code=500

注意：
  - 分类列表接口公开（无需认证），其余 5 个接口需要 ADMIN 角色 JWT token
  - token 通过 login_token fixture 注入（Bearer 格式）
  - 执行顺序：登录(order=1) → 列表(11) → 详情(12) → 新增(13) → 编辑(14) → 批量删(15) → 单删(16)
  - 接口间数据传递：列表提取 category_id/category_name，新增提取 new_category_id
"""
import allure
import pytest

from core.ApiService import ApiService
from utils.YamlUtil import YamlUtil


@allure.feature("分类模块")
@allure.story("分类列表")
class TestCategoryList:

    @pytest.mark.run(order=11)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("category.yaml", "category_list")
    )
    def test_category_list(self, data, login_token):
        """分类列表查询 - 数据驱动（公开接口，无需认证）"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("分类模块")
@allure.story("分类详情")
class TestCategoryDetail:

    @pytest.mark.run(order=12)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("category.yaml", "category_detail")
    )
    def test_category_detail(self, data, login_token):
        """分类详情查询 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("分类模块")
@allure.story("分类新增")
class TestCategoryAdd:

    @pytest.mark.run(order=13)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("category.yaml", "category_add")
    )
    def test_category_add(self, data, login_token):
        """新增分类 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("分类模块")
@allure.story("分类编辑")
class TestCategoryEdit:

    @pytest.mark.run(order=14)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("category.yaml", "category_edit")
    )
    def test_category_edit(self, data, login_token):
        """编辑分类 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("分类模块")
@allure.story("分类批量删除")
class TestCategoryDeleteBatch:

    @pytest.mark.run(order=15)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("category.yaml", "category_delete_batch")
    )
    def test_category_delete_batch(self, data, login_token):
        """批量删除分类 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("分类模块")
@allure.story("分类单个删除")
class TestCategoryDelete:

    @pytest.mark.run(order=16)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("category.yaml", "category_delete")
    )
    def test_category_delete(self, data, login_token):
        """单个删除分类 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)
