import time
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
import Common.Config as Config
from logging import getLogger

# loggerオブジェクトの宣言
logger = getLogger("Log")

# webdriver取得処理
# param : 無し
# return : WebDriver
def get_driver(conf: Config.ConfigData):
    logger.info("webdriver取得")
    # pdf保存のための初期設定
    chrome_options = webdriver.ChromeOptions()
    settings = {"recentDestinations": [{"id": "Save as PDF",
                                        "origin": "local",
                                        "account": ""}],
                "selectedDestinationId": "Save as PDF",
                "version": 2}
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        "savefile.default_directory": conf.download_path  # ダウンロード先を指定
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')
    return webdriver.Chrome(r"chromedriver.exe", options=chrome_options)


# ログイン処理
# param : WebDriver
# return : 無し
def login(conf: Config.ConfigData, driver: webdriver.Chrome):
    logger.info("ログイン")
    # ログイン
    login_btn = driver.find_elements(By.ID, 'nav-link-accountList')
    login_btn[0].click()
    time.sleep(1)
    login_email = driver.find_elements(By.ID, 'ap_email')
    login_email[0].send_keys(conf.id)  # ログイン失敗するとlogin_emailは取得できない
    next_btn = driver.find_elements(By.ID, 'continue')
    next_btn[0].click()
    time.sleep(1)
    login_pass = driver.find_elements(By.ID, 'ap_password')
    login_pass[0].send_keys(conf.password)
    login_btn = driver.find_elements(By.ID, 'signInSubmit')
    login_btn[0].click()
    # セキュリティのため、次の宛先に送信された通知を承認してください。
    # 携帯電話登録のページがでてくる場合は後でとする
    try:
        mobile_skip = driver.find_elements(
            By.ID, 'ap-account-fixup-phone-skip-link')
        mobile_skip[0].click()
    except:
        pass

# Cookie設定処理
# param : 設定ファイル情報
# return : 無し
def setCookie(conf: Config.ConfigData):
    logger.info("Cookie設定")
    # クッキー
    options = webdriver.chrome.options.Options()
    options.add_argument('--user-data-dir=' + conf.profile_path)

# ページ切り替え処理
# param : WebDriver
# return : 切り替え成功 True
#        : 切り替え不可 False
def switchWindow(driver: webdriver.Chrome):
    logger.info("ページ切り替え")
    # 次へボタンの要素を取得
    last_el = driver.find_elements(By.CLASS_NAME, 'a-last')[0]
    # 次へボタンが押せなくなった場合は終了
    if (len(last_el.find_elements(By.TAG_NAME, 'a')) > 0):
        # 次へボタンが押下できる場合、タブを切り替えて続行
        driver.find_elements(By.CLASS_NAME, 'a-last')[0].click()
        driver.switch_to.window(driver.window_handles[-1])
        return True
    else:
        return False