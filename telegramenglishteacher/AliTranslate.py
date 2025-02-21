import os
import sys

from typing import List

from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class AliTranslate:
    @staticmethod
    def create_client() -> alimt20181012Client:
        config = open_api_models.Config(
            access_key_id=os.getenv("AccessKey_ID"),
            access_key_secret=os.getenv("AccessKey_Secret"),
        )
        config.endpoint = f"mt.cn-hangzhou.aliyuncs.com"
        return alimt20181012Client(config)

    @staticmethod
    def translate(
        trans_text,
    ) -> None:
        client = AliTranslate.create_client()

        # 要翻译的文本
        text_to_translate = "你好，世界"  # 这里替换为你想要翻译的文本

        # 创建翻译请求对象
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            source_text={trans_text},  # 设置要翻译的文本
            source_language="en",  # 源语言，"zh" 表示中文
            target_language="zh",  # 目标语言，"en" 表示英文
            format_type="text",  # 设置格式类型，通常为 "text" 或 "html"
        )

        runtime = util_models.RuntimeOptions()
        try:
            # 发起翻译请求
            response = client.translate_general_with_options(
                translate_general_request, runtime
            )

            # 打印翻译结果
            return response.body.data.translated
        except Exception as error:
            # 打印异常的错误信息
            print(f"Error: {str(error)}")  # 或者 print(f"Error: {error.args}")
