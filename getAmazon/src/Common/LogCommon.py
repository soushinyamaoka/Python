import logging

def log_init():
    # "example.log"を出力先とするファイルハンドラ作成
    ch = logging.FileHandler(filename="example.log")
    #DEBUGレベルまで見る
    ch.setLevel(logging.DEBUG)

    # ログの記述フォーマット
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s [%(module)s][%(funcName)s] %(message)s')

    # ファイルハンドラにフォーマット情報を与える
    ch.setFormatter(formatter)

    # インスタンスの作成
    logger = logging.getLogger("Log")
    logger.setLevel(logging.DEBUG)

    # logger(インスタンス)にファイルハンドラの情報を与える
    logger.addHandler(ch)