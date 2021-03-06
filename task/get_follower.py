from __init__ import get_module_logger
from selenium.common.exceptions import WebDriverException
import json
import time
from .helper import TaskHelper


logger = get_module_logger(__name__)


class GetFollowerTask(TaskHelper):
    def __init__(self):
        super().__init__()

    # フォロワー・フォロー中ユーザー取得
    def get_follower(self):
        logger.info("START")
        self.info.set("{}を実行中..\nフォロワー画面を開きます\n".format(self.task_name))

        # script要素にあるwindow._sharedData(JSON)を取得し、
        # JSONを解析、アカウント情報を得る
        try:
            self.bs.get(self.PROFILE_URL)
            time.sleep(2)
            profile_json = self.bs.find_element_by_xpath(self.ACCOUNT_JSONDATA_XPATH)
            # script要素からJSONデータのみを抜き出す
            # ele.textは画面に表示されるもの限定なので使えない
            # script要素にはアトリビュートtextContentで中身にアクセスする
            profile_json = profile_json.get_attribute('textContent').replace('window._sharedData = ', '')[:-1]
        except WebDriverException:
            self.task_end('get_follower', "アカウント情報の取得に失敗しました\n{}を終了します\n".format(self.task_name), "JSON data get failed", 'ERROR')
            return False
        # JSONデータの読み込み
        try:
            profile = json.loads(profile_json)
        except json.decoder.JSONDecodeError:
            self.task_end('get_follower', "アカウント情報の取得に失敗しました\n{}を終了します\n".format(self.task_name), "JSON data get failed", 'ERROR')
            return False
        # フォロワー取得
        self.follower_n = profile["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"]
        # フォロー中取得
        self.following_n = profile["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_follow"]["count"]

        try:
            # フォロワー画面をポップアップ
            self.bs.find_element_by_xpath(self.FOLLOWER_WINDOW_XPATH).click()
            time.sleep(2)
            # フォロワー画面を取得
            self.dialog = self.bs.find_element_by_xpath(self.SCROLLABLE_ARIA_XPATH)
        except WebDriverException:
            self.task_end('get_follower', "フォロワー画面の取得に失敗しました\n{}を終了します\n".format(self.task_name), "get follower window failed", 'ERROR')
            return False

        try:
            # フォロワー画面のスクロール位置取得
            self.scroll_pos = self.bs.execute_script("return arguments[0].scrollTop", self.dialog)
        except WebDriverException:
            self.task_end('get_follower', "JavaScriptのクエリを実行できませんでした\nスクロール位置取得失敗\n{}を終了します".format(self.task_name), "execute JavaScript failed", 'ERROR')
            return False

        self.follower_s = set()  # フォロワーセット
        cnt = 1  # フォロワー取得カウント
        limit = self.follower_n
        # フォロワー画面のスクロール下限取得
        self.dialog_hight = self.bs.execute_script("return arguments[0].scrollHeight", self.dialog)
        time.sleep(2)

        while True:
            try:
                # フォロワー名取得
                name = self.bs.find_element_by_xpath(self.FOLLOWER_NAME_XPATH.format(cnt)).text
                self.follower_s.add(name)
                cnt += 1
                self.info.set("{}を実行中..\nフォロワー {}/{}\n{}".format(self.task_name, cnt - 1, limit, name))
            except WebDriverException:
                # スクロール位置をリスト１つ分増加
                self.scroll_pos += 54
                # スクロールする
                self.bs.execute_script("arguments[0].scrollTop = arguments[1]", self.dialog, self.scroll_pos)
                # DOMの読込みを待つ
                if not self.is_scroll_and_load():
                    # スクロール位置が下限に到達した場合
                    if cnt + 4 >= limit:
                        # フォロワー取得完了
                        break
                    else:
                        self.task_end('get_follower', "フォロワーの読込みに失敗しました\n再度実行してみてください\n", "scroll down limit")
                        return False
            if self.stop_fl:
                self.task_end('get_follower', "{}を停止しました\n\n".format(self.task_name))
                return False

        self.info.set("{}を実行中..\nフォロワーリストの作成が完了しました\n次にフォロー中リストを作成します".format(self.task_name))

        try:
            self.bs.find_element_by_xpath(self.FOLLOWER_WINDOW_CLOSE_XPATH).click()
            time.sleep(2)
            # フォロー中画面をポップアップ
            self.bs.find_element_by_xpath(self.FOLLOWING_WINDOW_XPATH).click()
            time.sleep(2)
            # フォロワー画面を取得
            self.dialog = self.bs.find_element_by_xpath(self.SCROLLABLE_ARIA_XPATH)
        except WebDriverException:
            self.task_end('get_following', "フォロー中画面の取得に失敗しました\n{}を終了します\n".format(self.task_name), "get following window failed")
            return False

        try:
            # フォロワー画面のスクロール位置取得
            self.scroll_pos = self.bs.execute_script("return arguments[0].scrollTop", self.dialog)
        except WebDriverException:
            self.task_end('get_following', "JavaScriptのクエリを実行できませんでした\nスクロール位置取得失敗\n{}を終了します".format(self.task_name), "execute JavaScript failed")
            return False

        self.following_s = set()  # フォロー中セット
        cnt = 1  # フォロー中取得カウント
        limit = self.following_n
        # フォロー中画面のスクロール下限取得
        self.dialog_hight = self.bs.execute_script("return arguments[0].scrollHeight", self.dialog)
        time.sleep(2)

        while True:
            try:
                # フォロー中 名取得
                name = self.bs.find_element_by_xpath(self.FOLLOWER_NAME_XPATH.format(cnt)).text
                self.following_s.add(name)
                cnt += 1
                self.info.set("{}を実行中..\nフォロー中 {}/{}\n{}".format(self.task_name, cnt - 1, limit, name))
            except WebDriverException:
                # スクロール位置をリスト１つ分増加
                self.scroll_pos += 54
                # スクロールする
                self.bs.execute_script("arguments[0].scrollTop = arguments[1]", self.dialog, self.scroll_pos)
                # DOMの読込みを待つ
                if not self.is_scroll_and_load():
                    # スクロール位置が下限に到達した場合
                    if cnt + 4 >= limit:
                        # フォロー中取得完了
                        break
                    else:
                        self.task_end('get_following', "フォロー中の読込みに失敗しました\n再度実行してみてください\n", "scroll down limit")
                        return False
            if self.stop_fl:
                self.task_end('get_following', "{}を停止しました\n\n".format(self.task_name))
                return False

        return True
