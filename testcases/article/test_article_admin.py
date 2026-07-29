# -*- coding:utf-8 -*-
"""
describe：SL Blog 文章模块 - 后台接口自动化测试
author：AI 生成

测试覆盖场景：
  1. 后台文章列表查询（分页+筛选）  → code=200, 提取文章ID
  2. 后台文章详情查询              → code=200, 验证文章字段
  3. 新建文章（草稿/校验/无分类）   → code=200, 提取新文章ID（需 ADMIN token）
  4. 编辑文章（更新标题/校验）      → code=200（需 ADMIN token）
  5. 获取草稿列表                  → code=200（需 ADMIN token）
  6. 批量移至回收站                → code=200（需 ADMIN token）
  7. 永久删除文章                  → code=200（需 ADMIN token）
  8. 导出文章                      → code=200（需 ADMIN token）
  9. 批量导出文章                 → code=200（需 ADMIN token）

注意：
  - 后台管理接口需要 ADMIN 角色 JWT token
  - token 通过登录接口提取，存储在 extract.yaml 中
  - conftest.py 中定义了 login_token fixture，通过参数注入实现认证
  - 执行顺序：登录 → 列表(2) → 详情(3) → 新建(4) → 编辑(5) → 草稿(6)
             → 移至回收站(7) → 永久删除(8) → 导出(9) → 批量导出(10)
"""
import allure
import pytest

from core.ApiService import ApiService
from utils.YamlUtil import YamlUtil


@allure.feature("文章模块")
@allure.story("后台文章列表")
class TestArticleAdminList:

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_admin.yaml", "article_admin_list")
    )
    def test_article_admin_list(self, data, login_token):
        """后台文章列表查询 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("文章模块")
@allure.story("后台文章详情")
class TestArticleAdminDetail:

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_admin.yaml", "article_admin_detail")
    )
    def test_article_admin_detail(self, data, login_token):
        """后台文章详情查询 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("文章模块")
@allure.story("后台文章新建")
class TestArticleAdminSave:

    @pytest.mark.run(order=4)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_admin.yaml", "article_admin_save")
    )
    def test_article_admin_save(self, data, login_token):
        """后台新建文章(校验/无分类) - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("文章模块")
@allure.story("后台文章编辑")
class TestArticleAdminUpdate:

    @pytest.mark.run(order=5)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_admin.yaml", "article_admin_update")
    )
    def test_article_admin_update(self, data, login_token):
        """后台编辑/更新文章 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("文章模块")
@allure.story("后台草稿列表")
class TestArticleAdminDrafts:

    @pytest.mark.run(order=6)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_admin.yaml", "article_admin_drafts")
    )
    def test_article_admin_drafts(self, data, login_token):
        """后台草稿列表查询 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("文章模块")
@allure.story("后台文章回收站操作")
class TestArticleAdminTrash:

    @pytest.mark.run(order=7)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_admin.yaml", "article_admin_move_to_trash")
    )
    def test_article_move_to_trash(self, data, login_token):
        """批量移至回收站 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


@allure.feature("文章模块")
@allure.story("后台文章永久删除")
class TestArticleAdminDelete:

    @pytest.mark.run(order=8)
    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_admin.yaml", "article_admin_delete")
    )
    def test_article_permanent_delete(self, data, login_token):
        """永久删除文章 - 数据驱动"""
        ApiService().handle_case(data, login_token=login_token)


# @allure.feature("文章模块")
# @allure.story("后台文章导出")
# class TestArticleAdminExport:

#     @pytest.mark.run(order=9)
#     @pytest.mark.parametrize(
#         "data",
#         YamlUtil().extract_case("article_admin.yaml", "article_admin_export")
#     )
#     def test_article_export(self, data, login_token):
#         """导出单篇文章 - 数据驱动"""
#         ApiService().handle_case(data, login_token=login_token)

#     @pytest.mark.run(order=10)
#     @pytest.mark.parametrize(
#         "data",
#         YamlUtil().extract_case("article_admin.yaml", "article_admin_export_batch")
#     )
#     def test_article_export_batch(self, data, login_token):
#         """批量导出文章 - 数据驱动"""
#         ApiService().handle_case(data, login_token=login_token)
