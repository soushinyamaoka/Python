import time
from selenium import webdriver
import Common.Config as Config
import Service.OutPutExcel as OutPutExcel
import Service.OutPutPdf as OutPutPdf
import Common.DriverCommon as DriverCommon
import Common.LogCommon as LogCommon
from logging import getLogger
import traceback

# loggerオブジェクトの宣言
logger = getLogger("Log")
# 設定ファイル情報
conf: Config.ConfigData = None
# WebDriver
driver: webdriver.Chrome = None

# メイン処理
def main():

    try:
        
        global conf
        logger.info('処理を開始します')
        # 初期処理
        init()

        # ブラウザ立ち上げ
        driver.get(conf.adress)
        time.sleep(2)

        # ログイン
        DriverCommon.login(conf, driver)
        time.sleep(1)
    
        # PDF出力モードの場合
        if conf.mode == "1":
            try:
                # 購入履歴PDF取得
                OutPutPdf.main(conf, driver)                
            except:
                logger.error("pdf化処理でエラーが発生しました。")
                raise

        # Excel出力モードの場合
        elif conf.mode == "2":
            try:
                # 購入履歴をエクセル出力
                OutPutExcel.main(conf, driver)               
            except:
                logger.error("Excel出力情報取得処理でエラーが発生しました。")
                raise

    except Exception as e:
        logger.error("エラーが発生しました。")
        logger.error(traceback.format_exc())
    finally:
        if driver is not None:
            # 終了
            driver.quit()
    

# 初期処理
# param : WebDriver
# return : 無し
def init():

    # 設定ファイル情報取得
    global conf
    conf = Config.ConfigData()

    # driverを取得
    global driver
    driver = DriverCommon.get_driver(conf)

    # Cookie設定
    DriverCommon.setCookie(conf)



if __name__ == '__main__':

    # ログ初期化
    LogCommon.log_init()

    main()