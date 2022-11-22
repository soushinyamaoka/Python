
# パッケージインストール
import sys;print(sys.prefix);print(sys.path)
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

import datetime
import json
import os
import time


# ユーザー情報
ID = 'XXXXXXXXXX_XXXXXX@gmail.com'
PASS = 'password'
PROFILE_PATH = 'Users/username/AppData/Local/Google/Chrome/User Data'
# アクセスアドレス
ADRESS = 'https://www.amazon.co.jp/'
# ファイルの保存先
DOWNLOAD_PATH = r'C:\Users\username\Downloads' # pdfダウンロードしてデフォルトで保存される先のパス
SAVE_PATH = r'C:\Users\username\Desktop\amazon_pdfs' # ファイルの保存先のパス 

# pdf保存のための初期設定
chrome_options = webdriver.ChromeOptions()
settings = {"recentDestinations": [{"id": "Save as PDF",
                                    "origin": "local",
                                    "account": ""}],
            "selectedDestinationId": "Save as PDF", 
            "version": 2}
prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')
driver = webdriver.Chrome(r"chromedriver.exe", options=chrome_options)

# クッキー
options = webdriver.chrome.options.Options()
options.add_argument('--user-data-dir=' + PROFILE_PATH)
# ブラウザ立ち上げ
driver.get(ADRESS)
time.sleep(2)

#ログイン
login_btn = driver.find_element_by_id('nav-link-accountList')
login_btn.click()
time.sleep(1)

login_email = driver.find_element_by_id('ap_email')
login_email.send_keys(ID)
next_btn = driver.find_element_by_id('continue')
next_btn.click()
time.sleep(1)

login_pass = driver.find_element_by_id('ap_password')
login_pass.send_keys(PASS)
login_btn = driver.find_element_by_id('signInSubmit')
login_btn.click()

# 携帯電話登録のページがでてくる場合は後でとする
try:
    mobile_skip = driver.find_element_by_id('ap-account-fixup-phone-skip-link')
    mobile_skip.click()
except:
    pass

time.sleep(1)

# 注文履歴画面へ
order_history = driver.find_element_by_id('nav-orders')
order_history.click()
time.sleep(2)
#すべてのページで行う
while True:

    main_handle = driver.current_window_handle
    receipt_links = driver.find_elements_by_link_text('領収書等')
    # 1ページないのすべての領収書で行う
    for receipt_link in receipt_links:

        receipt_link.click()
        time.sleep(1)
        receipt_purchase_link = driver.find_element_by_link_text('領収書／購入明細書')

        # クリック前のハンドルリスト
        handles_before = driver.window_handles
        # 新しいタブで開く
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL)
        actions.click(receipt_purchase_link)
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
        # pdf化したものをダウンロードフォルダから指定フォルダに名前を変更して保存する

        new_filename = driver.find_element_by_class_name('h1').text + '.pdf'# 新しいファイル名
        timestamp_now = time.time() # 現在時刻
        # ダウンロードフォルダを走査
        for (dirpath, dirnames, filenames) in os.walk(DOWNLOAD_PATH):
            for filename in filenames:
                if filename.lower().endswith(('.pdf')):
                    full_path = os.path.join(DOWNLOAD_PATH, filename)
                    timestamp_file = os.path.getmtime(full_path) # ファイルの時間
                    # 3秒以内に生成されたpdfを移動する
                    if (timestamp_now - timestamp_file) < 3: 
                        full_new_path = os.path.join(SAVE_PATH, new_filename)
                        os.rename(full_path, full_new_path)
                        print(full_path+' is moved to '+full_new_path)  

        time.sleep(1)
        driver.close()
        driver.switch_to.window(main_handle)
    # 次へのボタンが押せなくなった時点で終了
    try:
        driver.find_element_by_class_name('a-last').find_element_by_tag_name('a')
        driver.find_element_by_class_name('a-last').click()
        driver.switch_to.window(driver.window_handles[-1])
    except:
        break 

driver.quit()
