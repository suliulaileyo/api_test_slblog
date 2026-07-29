import os.path

import yaml


class YamlUtil:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data/")

    def read_extract_yaml(self):
        """只读取data下面的extract.yaml"""
        with open(self.data_path + "extract.yaml", mode="r", encoding="utf8") as f:
            value = yaml.safe_load(f)
            return value

    def read_testcases_yaml(self, yaml_name, key_name=None):
        """读取yaml内容，支持传入文件名和key值"""
        with open(self.data_path + yaml_name, mode='r', encoding="utf8") as f:
            value = yaml.safe_load(f)
            if key_name:
                return value[key_name]
            return value

    def extract_case(self, yaml_name, key_name):
        """用来配合测试用例使用，将yaml内容格式转换"""
        case_value = self.read_testcases_yaml(yaml_name, key_name)[0]
        new_case = []
        # 此处的case_info时根据yaml文件中的键值来的
        for value in case_value['case_info']:
            new_case.append({"request_info": case_value['request_info'], "case_info": value})
        return new_case

    def write_extra_yaml(self, data):
        """写入数据到yaml，data为字典"""
        with open(self.data_path + "extract.yaml", mode="a", encoding="utf8") as f:
            # 读取之前的yaml内容
            old_value = self.read_extract_yaml()
            if old_value:
                # 判断extract.yaml中原本是否有内容
                # 和新传入的数据做结合
                for key,value in data.items():
                    old_value[key] = value
                # 清空数据
                self.clear_extract_yaml()
                # ...
                yaml.dump(data=old_value, stream=f, allow_unicode=True, sort_keys=False)
            else:
                yaml.dump(data=data, stream=f, allow_unicode=True, sort_keys=False)

    def clear_extract_yaml(self):
        """清理extract.yaml"""
        with open(self.data_path + "extract.yaml", mode="w", encoding="utf8") as f:
            f.truncate() # truncate()：作用是截断字符串。默认开头开始
            f.flush()
            f.close()