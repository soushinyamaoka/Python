import configparser
import Const.ConfigConst as ConfigConst
import os
import datetime
from logging import getLogger
# loggerオブジェクトの宣言
logger = getLogger("Log")

class ConfigData:
    def __init__(self):
        logger.info("設定ファイル取得")
        
        conf_const: ConfigConst.ConfigConst = ConfigConst.ConfigConst()

        # 設定ファイル読み込み
        config_ini = configparser.ConfigParser()
        config_ini.read(conf_const.FILE_NAME, encoding=conf_const.ENCODING)
        config = config_ini[conf_const.DEFAULT]
        # 出力モード
        self.mode = config.get(conf_const.MODE)
        # ユーザー情報
        self.id = config.get(conf_const.USER_ID)
        self.password = config.get(conf_const.PASSWORD)
        self.profile_path = config.get(conf_const.PRFILE_PATH)
        # アクセスアドレス
        self.adress = config.get(conf_const.ADRESS)
        # ファイルの保存先
        self.download_path = config.get(conf_const.DOWNLOAD_PATH)  # pdfダウンロードしてデフォルトで保存される先のパス
        self.download_dir = config.get(conf_const.DOWNLOAD_DIR)  # ファイルの保存先ディレクトリ
        if not self.download_dir:
            # 現在時刻のディレクトリ
            now = datetime.datetime.now()
            current_time = now.strftime("%Y-%m-%d-%H-%M")
            self.download_path = os.path.join(self.download_path, current_time)
        else:
            self.download_path = os.path.join(self.download_path, self.download_dir)
        # エクセル保存先
        self.excel_path = config.get(conf_const.EXCEL_PATH)
        # 商品名取得時除外文字列
        self.exclusion_text = config.get(conf_const.EXCLUSION_TEXT).split('::')