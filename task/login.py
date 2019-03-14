from __init__ import get_module_logger
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import json


logger = get_module_logger(__name__)


class LoginTask():
    # ログイン処理
    def login(self):
        logger.info("START")
        # ログイン情報入力後エンターを押す
        try:  # 入力フォームを取得
            self.bs.get(self.LOGIN_URL)
            time.sleep(3)
            un_fd = self.bs.find_element_by_name("username")
            pw_fd = self.bs.find_element_by_name("password")
        except WebDriverException:
            return 'failed'

        un_fd.send_keys(self.login_v.login_f.username.get())
        pw_fd.send_keys(self.login_v.login_f.password.get())
        time.sleep(1)
        pw_fd.send_keys(Keys.RETURN)

        time.sleep(3)
        # ポップアップがあればクリックする
        self.close_modal()

        # 停止ボタンが押された場合
        if self.stop_fl:
            return 'stop'

        if self.bs.current_url == self.TOP_URL:
            return 'complete'
        else:
            return 'failed'

    # アカウント情報取得
    def get_account_info(self, mode='init'):
        logger.info("{} mode". format(mode))
        self.PROFILE_URL = self.PROFILE_URL.format(self.login_v.login_f.username.get())

        # script要素にあるwindow._sharedData(JSON)を取得し、
        # JSONを解析、アカウント情報を得る
        try:
            self.bs.get(self.PROFILE_URL)  # プロフィールページに遷移
            time.sleep(3)
            profile_json = self.bs.find_element_by_xpath(self.ACCOUNT_JSONDATA_XPATH)
            # script要素からJSONデータのみを抜き出す
            # ele.textは画面に表示されるもの限定なので使えない
            # script要素にはアトリビュートtextContentで中身にアクセスする
            profile_json = profile_json.get_attribute('textContent').replace('window._sharedData = ', '')[:-1]
        except WebDriverException:
            if mode == 'update':
                # 通信エラーを知らせる
                self.st_info['text'] = "@{}    [圏外]".format(self.login_v.login_f.username.get())
                self.tag_v.tag_f.tag_exec_b.state(['!disabled'])
                self.tl_v.tl_f.tl_exec_b.state(['!disabled'])
                logger.info("network not connected")
            else:
                self.task_end('login', "アカウント情報の取得に失敗しました\n\n", "JSON data get failed", 'ERROR')
            return
        # JSONデータの読み込み
        try:
            profile = json.loads(profile_json)
        except json.decoder.JSONDecodeError:
            self.task_end('login', "アカウント情報の取得に失敗しました\n\n", "JSON load failed", 'ERROR')
            return

        # 投稿数取得
        self.post_n = profile["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["count"]
        # フォロワー取得
        self.follower_n = profile["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]
        # フォロー中取得
        self.following_n = profile["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_follow"]["count"]

        # 停止ボタンが押された場合
        if self.stop_fl:
            self.task_end('login', "ログイン処理を停止しました\n\n")
            return

        # 初回ログイン時かどうか
        if mode == 'init':
            self.login_fl = True
            self.display_main()
        elif mode == 'update':  # メイン画面に遷移しない
            self.update_status()
            self.tag_v.tag_f.tag_exec_b.state(['!disabled'])
            self.tl_v.tl_f.tl_exec_b.state(['!disabled'])
            self.fl_v.fl_f.fl_exec_b.state(['!disabled'])
            self.fl_v.fl_f.fl_deic_b.state(['!disabled'])
        self.bs.get(self.TOP_URL)
        self.task_fl = False
        logger.info("complete")
