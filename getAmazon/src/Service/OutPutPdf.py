
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import Common.Config as Config
from logging import getLogger
import Common.DriverCommon as DriverCommon

# loggerオブジェクトの宣言
logger = getLogger("Log")
# 設定ファイル情報
conf: Config.ConfigData = None
# WebDriver
driver: webdriver.Chrome = None

# メイン処理
# param :
#       :
# return : 無し
def main(paramConf: Config.ConfigData, paramDriver: webdriver.Chrome):
    logger.info("購入履歴PDF出力処理開始")
    global conf
    conf = paramConf
    global driver
    driver = paramDriver

    # 購入履歴PDF取得
    get_history_on_pdf()
    logger.info("購入履歴PDF出力処理終了")

# 購入履歴PDF取得処理
# param : 設定ファイル情報
# param : WebDriver
# return : 無し
def get_history_on_pdf():
    # 保存先ディレクトリ作成
    os.makedirs(conf.download_path, exist_ok=True)

    # 注文履歴画面へ
    order_history = driver.find_elements(By.ID, 'nav-orders')
    order_history[0].click()
    time.sleep(2)
    # すべてのページで行う
    while True:

        main_handle = driver.current_window_handle
        receipt_links = driver.find_elements(By.LINK_TEXT, '領収書等')
        # 1ページないのすべての領収書で行う
        for receipt_link in receipt_links:

            receipt_link.click()
            time.sleep(1)
            receipt_purchase_link = driver.find_elements(By.LINK_TEXT, '領収書／購入明細書')

            # クリック前のハンドルリスト
            handles_before = driver.window_handles

            # 新しいタブで開く
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL)
            actions.click(receipt_purchase_link[0])
            actions.perform()

            # 新しいタブが開くまで最大30秒待機
            WebDriverWait(driver, 30).until(lambda a: len(driver.window_handles) > len(handles_before))

            # クリック後のハンドルリスト
            handles_after = driver.window_handles

            # ハンドルリストの差分
            handle_new = list(set(handles_after) - set(handles_before))

            # 新しいタブに移動
            driver.switch_to.window(handle_new[0])

            # pdf化
            driver.execute_script('window.print();')
            time.sleep(1)
            driver.close()
            driver.switch_to.window(main_handle)

            # ページ切り替え
            if not DriverCommon.switchWindow(driver):
                # 切り替え不可の場合は終了
                break


            