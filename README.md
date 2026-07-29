该项目是一个基于 Python 的 API 自动化测试框架，适用于对 Web 接口进行自动化测试。框架结合了常用的测试库如 `pytest` 和 `allure`，并封装了日志记录、断言、YAML 文件读取、接口请求等模块，以提高测试脚本的可维护性和可读性。

---

## 📌 主要功能模块

- **core**: 提供核心接口请求功能，封装了 `RestClient` 类用于发送 HTTP 请求。
- **utils**: 工具类模块，包含断言工具 `AssertUtil`、YAML 文件读取工具 `YamlUtil`、日志工具 `Logger`



## 🌈 使用说明

首先，下载项目源码后，在根目录下找到 `requirements.txt` 文件，然后通过 pip 工具安装 requirements.txt 依赖，执行命令（确保当前是pip还是pip3）：

```shell
pip3 install -r requirements.txt
```



接着，修改 `config/setting.ini` 配置文件，主要配置接口域名和mysql数据库信息。

安装相应依赖之后，在命令行窗口执行命令：

```shell
pytest
```

**注意**：因为我这里是针对示例的接口项目进行测试，公司使用请重新编写测试用例



## ⛄ 项目结构

- config ====>> 配置文件
- core ====>> requests请求方法封装、关键字返回结果类
- data ====>> 测试用例数据
- log ====>> 日志
- report ====>> 测试报告文件夹
- testcases ====>> 项目的测试用例
- utils ====>> 工具类
- pytest.ini ====>> pytest配置文件
- requirements.txt ====>> 相关依赖包文件



## 🚀 测试报告效果展示

在命令行执行命令：`pytest` 运行用例后，会得到一个测试报告的原始文件，但这个时候还不能打开成HTML的报告，还需要在项目根目录下，执行命令启动 `allure` 服务：

```shell
# 需要提前配置allure环境，才可以直接使用命令行
allure serve ./report
```

