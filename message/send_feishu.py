import base64
import hashlib
import hmac
import json
import os
import time
import urllib

import requests
from jenkins import Jenkins

jenkins_url = "http://localhost:8080/"
server = Jenkins(jenkins_url, username='suliulaile', password='cf2000...')
job_name = "job/SL_Blog"
job_url = server.get_info(job_name)['url']
job_last_number = server.get_info(job_name)['lastBuild']['number']
report_url = job_url + str(job_last_number) + '/allure'
script_dir = os.path.dirname(os.path.abspath(__file__))

# 飞书机器人配置
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/9da63224-64ee-4f59-a3cf-8f8b50f7203f"
FEISHU_SECRET = "NSDtp0f7zGhhiVXppWrmbh"  # ⚠️ 必须填写！

def generate_sign(secret, timestamp):
    """生成飞书签名"""
    # 拼接字符串
    string_to_sign = f'{timestamp}\n{secret}'
    # 使用 HMAC-SHA256 加密
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # Base64 编码
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

def push_message():
    # 1. 读取 prometheusData.txt
    content = {}
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "allure-report/export/prometheusData.txt")
    # file_path = os.path.dirname(os.getcwd()) + '/allure-report/export/prometheusData.txt'
    f = open(file_path)
    for line in f.readlines():
        launch_name = line.strip('\n').split(' ')[0]
        num = line.strip('\n').split(' ')[1]
        content.update({launch_name: num})
    f.close()
    print(content)
    # 2.提取数据
    passed_num = content['launch_status_passed']  # 通过数量
    failed_num = content['launch_status_failed']  # 失败数量
    broken_num = content['launch_status_broken']  # 阻塞数量
    skipped_num = content['launch_status_skipped']  # 跳过数量
    case_num = content['launch_retries_run']  # 总数量

    # 3. 生成飞书签名
    # timestamp = str(int(time.time()))
    # print("当前时间戳:", timestamp)
    # print("对应时间:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp))))
    # sign = generate_sign(FEISHU_SECRET, timestamp)

    # print(f"sign:====={sign}")
    # ✅ 新增：对 sign 进行 URL 编码
    # sign_encoded = urllib.parse.quote_plus(sign)  # 关键修复！
    # 4. 构造带签名的 URL
    # signed_url = f"{FEISHU_WEBHOOK_URL}?timestamp={timestamp}&sign={sign_encoded}"
    """
    # 5. 构造消息体，通过webhook发送消息
    """
    # text格式
    # content = {
    #     # "timestamp": timestamp,
    #     # "sign": sign,
    #     "msg_type": "text",
    #     "content": {
    #         "text": "接口自动化脚本执行结果：\n运行总数" + case_num
    #                    + "\n通过数量：" + passed_num
    #                    + "\n失败数量：" + failed_num
    #                    + "\n阻塞数量：" + broken_num
    #                    + "\n跳过数量：" + skipped_num
    #                    + "\n构建地址：\n" + job_url
    #                    + "\n报告地址：" + report_url
    #     }
    # }


    # interactive格式
    content = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "🧪 接口自动化测试报告"
                },
                "template": "green"  # 绿色主题
            },
            "elements": [
                # 统计卡片区域
                {
                    "tag": "column_set",
                    "flex_mode": "bisect",  # 两列布局
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"**✅ 通过**\n`{passed_num}`"
                                    },
                                    "background_style": "success"  # 成功背景色
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"**❌ 失败**\n`{failed_num}`"
                                    },
                                    "background_style": "danger"  # 危险背景色
                                }
                            ]
                        }
                    ]
                },
                {
                    "tag": "column_set",
                    "flex_mode": "bisect",
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"**⏸️ 阻塞**\n`{broken_num}`"
                                    },
                                    "background_style": "warning"  # 警告背景色
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "elements": [
                                {
                                    "tag": "div",
                                    "text": {
                                        "tag": "lark_md",
                                        "content": f"**⏭️ 跳过**\n`{skipped_num}`"
                                    },
                                    "background_style": "secondary"  # 次要背景色
                                }
                            ]
                        }
                    ]
                },
                {
                    "tag": "hr"
                },
                # 总计信息
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**📋 总计**: `{case_num}` 个测试用例"
                    }
                },
                {
                    "tag": "hr"
                },
                # 操作按钮
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "🔍 查看构建详情"
                            },
                            "type": "primary",
                            "url": job_url
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "📊 查看完整报告"
                            },
                            "type": "default",
                            "url": report_url
                        }
                    ]
                }
            ]
        }
    }
    # 6. 发送请求
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    res = requests.post(url=FEISHU_WEBHOOK_URL, json=content, headers=headers)
    print("📬 飞书响应:", res.text)
    if res.status_code == 200:
        result = res.json()
        if result.get("code") == 0:
            print("✅ 飞书通知发送成功！")
        else:
            print(f"❌ 飞书返回错误: {result}")
    else:
        print(f"❌ HTTP 请求失败: {res.status_code}, {res.text}")


push_message()
