# -*- coding:utf-8 -*-
"""
describe：SL Blog 文章模块 - 前台接口自动化测试
author：AI 生成

测试覆盖场景：
  1. 获取最新已发布文章列表（分页）   → code=200, 验证分页数据
  2. 获取热门文章                     → code=200, 验证返回数据
  3. 获取最新创建文章                 → code=200, 验证返回数据
  4. 获取前台文章详情                 → code=200, 验证文章标题和内容
"""
import allure
import pytest

from core.ApiService import ApiService
from utils.YamlUtil import YamlUtil


@allure.feature("文章模块")
@allure.story("前台文章接口")
class TestArticleFronted:

    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_fronted.yaml", "article_fronted_list")
    )
    def test_article_latest_list(self, data):
        """获取最新已发布文章列表 - 数据驱动"""
        ApiService().handle_case(data)

    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_fronted.yaml", "article_fronted_popular")
    )
    def test_article_popular(self, data):
        """获取热门文章 - 数据驱动"""
        ApiService().handle_case(data)

    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_fronted.yaml", "article_fronted_new")
    )
    def test_article_new(self, data):
        """获取最新创建文章 - 数据驱动"""
        ApiService().handle_case(data)


@allure.feature("文章模块")
@allure.story("前台文章详情")
class TestArticleFrontedDetail:

    @pytest.mark.parametrize(
        "data",
        YamlUtil().extract_case("article_fronted.yaml", "article_fronted_detail")
    )
    def test_article_fronted_detail(self, data):
        """获取前台文章详情 - 数据驱动"""
        ApiService().handle_case(data)
