from __init__ import get_module_logger
from selenium.common.exceptions import WebDriverException
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

        try:
            self.bs.get(self.PROFILE_URL)
            time.sleep(2)
            # フォロワー画面をポップアップ
            self.bs.find_element_by_xpath(self.FOLLOWER_WINDOW_XPATH).click()
            time.sleep(2)
            # フォロワー画面を取得
            self.dialog = self.bs.find_element_by_xpath(self.SCROLLABLE_ARIA_XPATH)
        except WebDriverException:
            self.task_end('get_follower', "フォロワー画面の取得に失敗しました\n{}を終了します\n".format(self.task_name), "get follower window failed")
            return False

        try:
            # フォロワー画面のスクロール位置取得
            self.scroll_pos = self.bs.execute_script("return arguments[0].scrollTop", self.dialog)
        except WebDriverException:
            self.task_end('get_follower', "JavaScriptのクエリを実行できませんでした\nスクロール位置取得失敗\n{}を終了します".format(self.task_name), "execute JavaScript failed")
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
                    if cnt - 1 >= limit:
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
                    if cnt - 1 >= limit:
                        # フォロー中取得完了
                        break
                    else:
                        self.task_end('get_following', "フォロー中の読込みに失敗しました\n再度実行してみてください\n", "scroll down limit")
                        return False
            if self.stop_fl:
                self.task_end('get_following', "{}を停止しました\n\n".format(self.task_name))
                return False

        return True

    # フォローバック処理
    def followback(self):
        logger.info("start")
        self.info.set("{}を実行中..\nフォロワー画面を開きます\n".format(self.task_name))

        try:
            self.bs.get(self.PROFILE_URL)
            time.sleep(2)
            # フォロワー画面をポップアップ
            self.bs.find_element_by_xpath(self.FOLLOWER_WINDOW_XPATH).click()
            time.sleep(2)
            # フォロワー画面を取得
            self.dialog = self.bs.find_element_by_xpath(self.SCROLLABLE_ARIA_XPATH)
        except WebDriverException:
            self.task_end('followback', "フォロワー画面の取得に失敗しました\n{}を終了します\n".format(self.task_name), "get follower window failed")
            return False

        try:
            # フォロワー画面のスクロール位置取得
            self.scroll_pos = self.bs.execute_script("return arguments[0].scrollTop", self.dialog)
        except WebDriverException:
            self.task_end('followback', "JavaScriptのクエリを実行できませんでした\nスクロール位置取得失敗\n{}を終了します".format(self.task_name), "execute JavaScript failed")
            return False

        cnt = 1  # フォロワー取得カウント
        followback_cnt = 0  # フォローバックカウント
        interval = self.util_param['liked_interval']  # いいねの間隔
        # フォロー中画面のスクロール下限取得
        self.dialog_hight = self.bs.execute_script("return arguments[0].scrollHeight", self.dialog)
        self.info.set("{}を実行中..\nユーザーを探しています\n".format(self.task_name))
        time.sleep(2)

        while True:
            try:
                # フォロワー名取得
                name = self.bs.find_element_by_xpath(self.FOLLOWER_NAME_XPATH.format(cnt)).text
                # フォローバック対象の場合
                if name in self.followback_l:
                    # フォローバック対象までゆっくりスクロール
                    while (cnt - 1) * 54 >= self.scroll_pos:
                        self.scroll_pos += 2
                        self.bs.execute_script("arguments[0].scrollTop = arguments[1]", self.dialog, self.scroll_pos)
                    time.sleep(3)
                    try:
                        # フォローするボタンクリック
                        self.bs.find_element_by_xpath(self.FOLLOWBACK_XPATH.format(cnt)).click()
                        followback_cnt += 1
                        self.util_param['act_cnt'] += 1
                        self.info.set("{}を実行中..\n{}/{}  {}\nをフォローバックしました".format(self.task_name, followback_cnt, len(self.followback_l), name))
                        # タスク完了
                        if followback_cnt == len(self.followback_l):
                            time.sleep(3)
                            self.task_end('followback', "選択した{}人全てのユーザーをフォローバックしました\n{}を終了します\n".format(followback_cnt, self.task_name), "complete")
                            break
                        time.sleep(interval - 3)
                    except WebDriverException:
                        logger.info("followback failed")
                cnt += 1
            except WebDriverException:
                # スクロール位置をリスト１つ分増加
                self.scroll_pos += 54
                # スクロールする
                self.bs.execute_script("arguments[0].scrollTop = arguments[1]", self.dialog, self.scroll_pos)
                # DOMの読込みを待つ
                if not self.is_scroll_and_load():
                    # スクロール位置が下限に到達した場合
                    self.task_end('followback', "{}人中{}人のユーザーをフォローバックしました\n{}を終了します\n".format(len(self.followback_l), followback_cnt, self.task_name), "scroll down limit")
                    break
            if self.stop_fl:
                self.task_end('followback', "{}を停止しました\n\n".format(self.task_name))
                break

    # フォローやめる処理
    def unfollow(self):
        logger.info("start")
        self.info.set("{}を実行中..\nフォロワー画面を開きます\n".format(self.task_name))

        try:
            self.bs.get(self.PROFILE_URL)
            time.sleep(2)
            # フォロー中画面をポップアップ
            self.bs.find_element_by_xpath(self.FOLLOWING_WINDOW_XPATH).click()
            time.sleep(2)
            # フォロー中画面を取得
            self.dialog = self.bs.find_element_by_xpath(self.SCROLLABLE_ARIA_XPATH)
        except WebDriverException:
            self.task_end('unfollow', "フォロワー画面の取得に失敗しました\n{}を終了します\n".format(self.task_name), "get following window failed")
            return False

        try:
            # フォロー中画面のスクロール位置取得
            self.scroll_pos = self.bs.execute_script("return arguments[0].scrollTop", self.dialog)
        except WebDriverException:
            self.task_end('unfollow', "JavaScriptのクエリを実行できませんでした\nスクロール位置取得失敗\n{}を終了します".format(self.task_name), "execute JavaScript failed")
            return False

        cnt = 1  # フォロワー取得カウント
        unfollow_cnt = 0  # フォローやめたカウント
        interval = self.util_param['liked_interval']  # いいねの間隔
        # フォロー中画面のスクロール下限取得
        self.dialog_hight = self.bs.execute_script("return arguments[0].scrollHeight", self.dialog)
        self.info.set("{}を実行中..\nユーザーを探しています\n".format(self.task_name))
        time.sleep(2)

        while True:
            try:
                # フォロー中 名取得
                name = self.bs.find_element_by_xpath(self.FOLLOWER_NAME_XPATH.format(cnt)).text
                # フォローやめる対象の場合
                if name in self.unfollow_l:
                    # フォローやめる対象までゆっくりスクロール
                    while (cnt - 1) * 54 >= self.scroll_pos:
                        self.scroll_pos += 2
                        self.bs.execute_script("arguments[0].scrollTop = arguments[1]", self.dialog, self.scroll_pos)
                    time.sleep(3)
                    try:
                        # フォロー中ボタンクリック
                        self.bs.find_element_by_xpath(self.UNFOLLOW_XPATH.format(cnt)).click()
                        time.sleep(2)
                        # フォローやめるボタンクリック
                        self.bs.find_element_by_xpath(self.UNFOLLOW_TRUTH_XPATH).click()
                        unfollow_cnt += 1
                        self.util_param['act_cnt'] += 1
                        self.info.set("{}を実行中..\n{}/{}  {}\nのフォローをやめました".format(self.task_name, unfollow_cnt, len(self.unfollow_l), name))
                        # タスク完了
                        if unfollow_cnt == len(self.unfollow_l):
                            time.sleep(3)
                            self.task_end('unfollow', "選択した{}人全てのユーザーのフォローをやめました\n{}を終了します\n".format(unfollow_cnt, self.task_name), "complete")
                            break
                        time.sleep(interval - 5)
                    except WebDriverException:
                        logger.info("unfollow failed")
                cnt += 1
            except WebDriverException:
                # スクロール位置をリスト１つ分増加
                self.scroll_pos += 54
                # スクロールする
                self.bs.execute_script("arguments[0].scrollTop = arguments[1]", self.dialog, self.scroll_pos)
                # DOMの読込みを待つ
                if not self.is_scroll_and_load():
                    # スクロール位置が下限に到達した場合
                    self.task_end('unfollow', "{}人中{}人のユーザーのフォローをやめました\n{}を終了します\n".format(len(self.unfollow_l), unfollow_cnt, self.task_name), "scroll down limit")
                    break
            if self.stop_fl:
                self.task_end('unfollow', "{}を停止しました\n\n".format(self.task_name))
                break
