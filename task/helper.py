from __init__ import get_module_logger
from selenium.common.exceptions import WebDriverException
import time


logger = get_module_logger(__name__)


class TaskHelper():
    # timeline
    def scroll_down(self, y):
        # Javascriptで現在のスクロール位置を取得
        now_scroll_pos = self.bs.execute_script("return window.scrollY;")
        # スクロール量を算出
        move_amount = y - now_scroll_pos
        # 指定位置になるまで1pxずつスクロールする
        while move_amount > 45:  # 少し行き過ぎるので手前でストップ
            self.bs.execute_script("window.scrollTo(0, window.pageYOffset + 1);")
            move_amount -= 1

    # timeline
    def get_next_post(self, post):
        loop_cnt = 0
        # スクロールでDOMを出現させ、取得する
        while loop_cnt < 1000:  # スクロール量が1000pxを超えたら終了
            # 1pxスクロール
            self.bs.execute_script("window.scrollTo(0, window.pageYOffset + 1);")
            try:
                # 現在のメディアのすぐ後ろの兄弟要素取得
                post = post.find_element_by_xpath("following-sibling::article")
                return post
            except WebDriverException:
                loop_cnt += 1
        return False

    # get_follower, followback, unfollow
    def is_scroll_and_load(self):
        time.sleep(0.02)
        if self.scroll_pos + 1000 < self.dialog_hight:
            return True
        else:
            if self.scroll_pos + 500 >= self.dialog_hight:
                time.sleep(0.1)
            elif self.scroll_pos + 250 >= self.dialog_hight:
                time.sleep(0.5)
            elif self.scroll_pos >= self.dialog_hight:
                time.sleep(1)
            self.dialog_hight = self.bs.execute_script("return arguments[0].scrollHeight", self.dialog)
            if self.scroll_pos < self.dialog_hight:
                return True
            return False
