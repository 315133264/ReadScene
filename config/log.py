import logging

# 配置日志
logging.basicConfig(
    filename='capture.log',
    level=logging.INFO | logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)