import json
import logging
import datetime
import time

from utils.AssertUtil import AssertUtil
from utils.YamlUtil import YamlUtil
from utils.log_util import logger


class ExtractUtil:
    def __init__(self):
        self.jsonpath_util = AssertUtil() # 引入自己封装的断言工具类
        self.yaml_util = YamlUtil() # 引入yaml文件操作工具类

    # ==================== 时间戳相关方法开始 ====================
    
    def get_current_time(self, fmt="%Y-%m-%d %H:%M:%S"):
        """
        获取当前时间
        
        Args:
            fmt: 时间格式，默认为 "%Y-%m-%d %H:%M:%S"
            
        Returns:
            str: 格式化后的当前时间字符串
            
        使用示例（在YAML文件中）:
            name: "报告_${get_current_time()}"
            # 结果: 报告_2026-04-20 15:30:45
        """
        return datetime.datetime.now().strftime(fmt)
    
    def get_timestamp(self):
        """
        获取当前时间戳（秒级）
        
        Returns:
            str: 当前时间戳字符串
            
        使用示例（在YAML文件中）:
            timestamp: "${get_timestamp()}"
        """
        return str(int(time.time()))
    
    def get_timestamp_ms(self):
        """
        获取当前时间戳（毫秒级）
        
        Returns:
            str: 当前毫秒时间戳字符串
            
        使用示例（在YAML文件中）:
            timestamp: "${get_timestamp_ms()}"
        """
        return str(int(time.time() * 1000))
    
    def append_time(self, prefix="", suffix="", fmt="%Y-%m-%d %H:%M:%S"):
        """
        在文本前后追加时间戳
        
        Args:
            prefix: 前缀文本
            suffix: 后缀文本
            fmt: 时间格式
            
        Returns:
            str: 拼接后的字符串
            
        使用示例（在YAML文件中）:
            title: "${append_time(测试精彩)}"
            # 结果: 测试精彩-2026-04-20 15:30:45
            
            keyword: "${append_time(, -测试)}"
            # 结果: 2026-04-20 15:30:45 - 测试
        """
        current_time = self.get_current_time(fmt)
        if prefix and suffix:
            return f"{prefix}-{current_time}-{suffix}"
        elif prefix:
            return f"{prefix}-{current_time}"
        elif suffix:
            return f"{current_time}-{suffix}"
        else:
            return current_time
    
    def prefix_time(self, text, fmt="%Y%m%d%H%M%S"):
        """
        给文本添加时间前缀
        
        Args:
            text: 原始文本
            fmt: 时间格式，默认紧凑格式
            
        Returns:
            str: 带时间前缀的文本
            
        使用示例（在YAML文件中）:
            name: "${prefix_time(测试视频)}"
            # 结果: 20260420153045_测试视频
        """
        current_time = self.get_current_time(fmt)
        return f"{current_time}_{text}"
    
    def suffix_time(self, text, fmt="%Y%m%d%H%M%S"):
        """
        给文本添加时间后缀
        
        Args:
            text: 原始文本
            fmt: 时间格式，默认紧凑格式
            
        Returns:
            str: 带时间后缀的文本
            
        使用示例（在YAML文件中）:
            name: "${suffix_time(测试视频)}"
            # 结果: 测试视频_20260420153045
        """
        current_time = self.get_current_time(fmt)
        return f"{text}_{current_time}"
    
    # ==================== 时间戳相关方法结束 ====================

    def extract_data(self, res, extract):
        """
        将接口的响应结果提取出来存入到yaml中
        :param res: res.json
        :param extract: eg:$.token
        :return:
        """
        if extract:
            for key,expression in extract.items():
                try:
                    value = self.jsonpath_util.extract_by_jsonpath(res,expression)
                    logger.info(f"====================从文件中获取到的extract的内容为：{value}")
                    print(f"====================从文件中获取到的extract的内容为：{value}")
                    # 写入value
                    self.yaml_util.write_extra_yaml({key:value})
                except Exception as e:
                    logger.error(f"变量{key}写入extract.yaml失败，请检查，error={e}")

    def get_extract_value(self, key):
        """从extract.yaml中获取内容"""
        try:
            data = self.yaml_util.read_extract_yaml()
            return data[key]
        except Exception as e:
            logger.error(f"从extract.yaml文件中根据{key}获取不到内容，error={e}")

    def extract_url(self,url):
        """
            检查 url是否包含 ${...}这样的占位符。
            如果有，则调用 process_data方法处理并替换占位符
            如果没有，则直接返回原始 url
        """
        if "${" in url and "}" in url:
            return self.process_data(url)
        return url

    def process_data(self,data):
        """处理函数"""
        # 保留旧代码作为参考
        # for i in range(data.count("${")):
        #     if "${" in data and "{" in data:
        #         start_index = data.index('$') # 找到 $的位置
        #         end_index = data.index('}') # 找到 }的位置
        #         # 获取函数中的方法
        #         func_full_name = data[start_index:end_index+1] # 此处的end_index+1是因为切片的尾部不是闭区间
        #         # 获取函数名
        #         func_name = data[start_index+2:data.index('(')] # eg: /orders/${get_extract_value(order_id)}/  get_extract_value
        #         # 获取函数中的参数
        #         func_params = data[data.index('(')+1:data.index(')')] # eg: /orders/${get_extract_value(order_id)}/  order_id
        #         # 先进行getattr获取对象
        #         extract_data = getattr(self,func_name,None)
        #         if extract_data is not None:
        #             # 1.拆分参数
        #             if func_params: # 如果func_name不是空字符串
        #                 param_list = func_params.split(",") # 按逗号分割成列表
        #             else:
        #                 param_list = []
        #
        #             # 2.如果有数字，尝试将参数转换为整数
        #             processed_params = []
        #             for param in param_list:
        #                 if param.isdigit(): # 检查是否是纯数字字符串（如"123"）
        #                     processed_params.append(int(param))
        #                 else:
        #                     processed_params.append(param)
        #             # 3.调用方法并传入处理后的参数
        #             result = extract_data(*processed_params) # 相当于extract_data(params1,params2,...)
        #             extract_data = result # 更新 extract_data 为调用后的返回值
        #         data = data.replace(func_full_name, str(extract_data))
        # return data
        
        # 新代码：修复嵌套JSON中}匹配问题
        for i in range(data.count("${")):
            if "${" in data and "(" in data:
                start_index = data.index('${') # 找到 ${ 的位置
                # 找到匹配的右括号，处理嵌套括号的情况
                paren_count = 0
                end_index = start_index
                for j in range(start_index, len(data)):
                    if data[j] == '(':
                        paren_count += 1
                    elif data[j] == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            # 找到函数调用的结束位置，还要包含后面的 }
                            if j + 1 < len(data) and data[j + 1] == '}':
                                end_index = j + 1
                            break
                
                if end_index <= start_index:
                    continue  # 没有找到匹配的括号，跳过
                
                # 获取函数中的方法
                func_full_name = data[start_index:end_index+1]
                # 获取函数名
                func_name_start = start_index + 2
                func_name_end = data.index('(', start_index)
                func_name = data[func_name_start:func_name_end]
                # 获取函数中的参数
                func_params_start = func_name_end + 1
                # 找到与第一个 ( 匹配的 )
                paren_count = 1
                func_params_end = func_params_start
                for k in range(func_params_start, len(data)):
                    if data[k] == '(':
                        paren_count += 1
                    elif data[k] == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            func_params_end = k
                            break
                
                func_params = data[func_params_start:func_params_end]
                
                # 先进行getattr获取对象
                extract_data = getattr(self,func_name,None)
                if extract_data is not None:
                    # 1.拆分参数
                    if func_params: # 如果func_name不是空字符串
                        param_list = func_params.split(",") # 按逗号分割成列表
                    else:
                        param_list = []

                    # 2.如果有数字，尝试将参数转换为整数
                    processed_params = []
                    for param in param_list:
                        param = param.strip()
                        if param.isdigit(): # 检查是否是纯数字字符串（如"123"）
                            processed_params.append(int(param))
                        elif param.startswith('"') and param.endswith('"'): # 处理字符串参数
                            processed_params.append(param[1:-1])
                        elif param.startswith("'") and param.endswith("'"): # 处理单引号字符串参数
                            processed_params.append(param[1:-1])
                        else:
                            processed_params.append(param)
                    # 3.调用方法并传入处理后的参数
                    result = extract_data(*processed_params) # 相当于extract_data(params1,params2,...)
                    extract_data = result # 更新 extract_data 为调用后的返回值
                # 根据数据类型选择合适的序列化方式，保留原始类型
                # 判断 ${...} 是否被外层双引号完整包裹（即该占位符独占一个 JSON value）
                is_quoted_value = (
                    start_index > 0 and data[start_index - 1] == '"' and
                    end_index + 1 < len(data) and data[end_index + 1] == '"'
                )
                logger.info(
                    f"占位符替换: {func_full_name} -> {extract_data!r} "
                    f"(类型: {type(extract_data).__name__}, 独占value: {is_quoted_value})"
                )

                if isinstance(extract_data, (list, dict)):
                    # 数组/字典：独占 value 时去掉引号，用 JSON 原样嵌入；否则做字符串替换
                    if is_quoted_value:
                        data = data[:start_index - 1] + json.dumps(extract_data) + data[end_index + 2:]
                    else:
                        data = data.replace(func_full_name, json.dumps(extract_data))
                elif isinstance(extract_data, bool):
                    # bool 是 int 子类，必须单独处理，避免被 int 分支提前匹配
                    if is_quoted_value:
                        data = data[:start_index - 1] + ('true' if extract_data else 'false') + data[end_index + 2:]
                    else:
                        data = data.replace(func_full_name, 'true' if extract_data else 'false')
                elif isinstance(extract_data, (int, float)):
                    # 数值型：独占 value 时去掉外层双引号，保持 int/float 类型
                    if is_quoted_value:
                        data = data[:start_index - 1] + str(extract_data) + data[end_index + 2:]
                    else:
                        data = data.replace(func_full_name, str(extract_data))
                elif extract_data is None:
                    # null 也要保留原始类型
                    if is_quoted_value:
                        data = data[:start_index - 1] + 'null' + data[end_index + 2:]
                    else:
                        data = data.replace(func_full_name, 'null')
                else:
                    # 字符串或其他不可识别对象：按字符串替换
                    data = data.replace(func_full_name, str(extract_data))
        return data

    def _has_binary_data(self, data):
        """递归检查数据是否包含二进制数据
        
        Args:
            data: 要检查的数据
            
        Returns:
            bool: 如果包含二进制数据则返回 True，否则返回 False
        """
        if isinstance(data, dict):
            for value in data.values():
                if self._has_binary_data(value):
                    return True
        elif isinstance(data, list):
            for item in data:
                if self._has_binary_data(item):
                    return True
        elif isinstance(data, tuple):
            for item in data:
                if self._has_binary_data(item):
                    return True
        elif isinstance(data, bytes):
            return True
        elif hasattr(data, 'read') and callable(data.read):
            # 检查是否为文件对象（如BufferedReader）
            return True
        return False
    
    def extract_case(self, case_info):
        """处理用例数据中的动态变量
        
        处理 case_info 中的动态变量，支持包含二进制数据的字典
        
        Args:
            case_info: 用例数据，可能包含二进制数据
            
        Returns:
            dict: 处理后的用例数据
        """
        # 递归检查 case_info 是否包含二进制数据
        has_binary_data = self._has_binary_data(case_info)
        
        # 如果包含二进制数据，直接处理字符串字段，不进行 JSON 序列化
        if has_binary_data:
            # 递归处理所有字符串字段中的动态变量
            def process_dict(d):
                for key, value in d.items():
                    if isinstance(value, str):
                        d[key] = self.process_data(value)
                    elif isinstance(value, dict):
                        process_dict(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                process_dict(item)
                            elif isinstance(item, str):
                                item = self.process_data(item)
            
            if isinstance(case_info, dict):
                process_dict(case_info)
            
            return case_info
        else:
            # 没有二进制数据，使用原来的 JSON 序列化方式处理
            str_case_info = json.dumps(case_info) # 将 case_info 转为 JSON 字符串
            data = self.process_data(str_case_info) # 调用 process_data 方法解析字符串中的动态占位符
            return json.loads(data) # 将处理后的字符串重新转回 JSON 结构
