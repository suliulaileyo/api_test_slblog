import jsonpath


class AssertUtil:
    @staticmethod
    def equals(check_value, expect_value):
        """相等"""
        assert check_value == expect_value, (
            f'{check_value!r} == {expect_value!r} '
            f'(类型: {type(check_value).__name__} vs {type(expect_value).__name__})'
        )

    @staticmethod
    def less_than(check_value, expect_value):
        """小于"""
        assert check_value < expect_value, f'{check_value} < {expect_value}'

    @staticmethod
    def less_than_or_equals(check_value, expect_value):
        """小于等于"""
        assert check_value <= expect_value, f'{check_value} <= {expect_value}'

    @staticmethod
    def greater_than(check_value, expect_value):
        """大于"""
        assert check_value > expect_value, f'{check_value} > {expect_value}'

    @staticmethod
    def greater_than_or_equals(check_value, expect_value):
        """大于等于"""
        assert check_value >= expect_value, f'{check_value} >= {expect_value}'

    @staticmethod
    def not_equals(check_value, expect_value):
        """不等于"""
        assert check_value != expect_value, f'{check_value} != {expect_value}'

    @staticmethod
    def contains(check_value, expect_value):
        """包含
        智能判断：如果 expect_value 是列表/数组，检查 check_value 是否在其中；
                  如果 check_value 是列表/数组，检查 expect_value 是否在其中；
                  否则按字符串包含检查
        """
        # 情况1：expect_value 是列表，检查 check_value 在列表中
        if isinstance(expect_value, (list, tuple)):
            assert check_value in expect_value, f'{check_value} in {expect_value}'
        # 情况2：check_value 是列表，检查 expect_value 在列表中
        elif isinstance(check_value, (list, tuple)):
            assert expect_value in check_value, f'{expect_value} in {check_value}'
        # 情况3：都不是列表，按字符串包含检查
        else:
            assert str(check_value) in str(expect_value), f'{str(check_value)} in {str(expect_value)}'

    @staticmethod
    def startswith(check_value, expect_value):
        """以什么开头"""
        assert str(check_value).startswith(str(expect_value)),f'{str(check_value)} startswith {str(expect_value)})'

    @staticmethod
    def endswith(check_value, expect_value):
        """以什么结尾"""
        assert str(check_value).endswith(str(expect_value)), f'{str(check_value)} endswith {str(expect_value)})'

    @staticmethod
    def length(check_value, expect_value):
        """校验数量"""
        assert len(check_value) == len(expect_value), f'{len(check_value)} == {len(expect_value)}'

    def extract_by_jsonpath(self,extract_value: dict,extract_expression: str):
        """
        从响应结果中提取值跟预期结果比对：使用jsonpath
        :param extract_value: response.json()
        :param extract_expression: 例如：'$.code'
        :return: None或者提取的第一个值或者全部
        """

        # 校验extract_expression是不是字符串，不是字符串直接返回原格式内容
        if not isinstance(extract_expression, str):
            return extract_expression
        extract_value = jsonpath.jsonpath(extract_value, extract_expression) # 使用jsonpath表达式将所需内容提取出来
        if not extract_value:
            return
        elif len(extract_value) == 1:
            return extract_value[0]
        else:
            return extract_value

    def validate_response(self, response, validate_check):
        """校验结果"""
        for check in validate_check:
            for check_type,check_value in check.items():
                # 实际结果
                actual_value = self.extract_by_jsonpath(response,check_value[0])
                # 预期结果
                expect_value = check_value[1]
                # 判定检查方法是什么，去执行对应的方法
                if check_type in ["eq","equals","equal"]:
                    self.equals(actual_value,expect_value)
                elif check_type in ["lt","less"]:
                    self.less_than(actual_value,expect_value)
                elif check_type in ["le","less_or_equals"]:
                    self.less_than_or_equals(actual_value,expect_value)
                elif check_type in ["gt","greater_than"]:
                    self.greater_than(actual_value,expect_value)
                elif check_type in ["gte","greater_or_equals"]:
                    self.greater_than_or_equals(actual_value,expect_value)
                elif check_type in ["ne","not_equals"]:
                    self.not_equals(actual_value,expect_value)
                elif check_type in ["contains"]:
                    self.contains(actual_value,expect_value)
                elif check_type in ["startswith"]:
                    self.startswith(actual_value,expect_value)
                elif check_type in ["endswith"]:
                    self.endswith(actual_value,expect_value)
                elif check_type in ["length"]:
                    self.length(actual_value,expect_value)
                else:
                    print(f"{check_type} not valid check type")



