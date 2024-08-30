import re
import os
import json
import logging
logger = logging.getLogger()

from mvp.mvp_utils import safe_mkdir
from vo.paper_data import Paper



def validate_arxiv_url(url):
    # 定义arXiv URL的正则表达式
    arxiv_url_pattern = re.compile(r'^https?://arxiv\.org/abs/\d{4}\.\d{5}(v\d+)?$')

    # 使用正则表达式进行匹配
    if arxiv_url_pattern.match(url):
        msg = "这是一个有效的arXiv URL链接。"
        return True, msg
    else:
        msg = "无效的arXiv URL链接，请输入正确的链接，例如：https://arxiv.org/abs/2404.07738"
        return False, msg

def save_content_to_file(content, save_path):
    with open(save_path, 'w') as fw:
        fw.write(content)


if __name__ == '__main__':
    # 测试函数
    url = "https://arxiv.org/abs/2404.07738"
    validate_arxiv_url(url)

    url = "https://example.com/abs/2404.07738"
    validate_arxiv_url(url)
