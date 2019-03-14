from __init__ import get_module_logger
from selenium.common.exceptions import WebDriverException
import time
from .helper import TaskHelper


logger = get_module_logger(__name__)


class TimelineTask(TaskHelper):
    def __init__(self):
        super().__init__()

    # タイムライン自動いいね処理
    def timeline(self, mode):
        self.info.set("{}を実行中..\nメディアを取得します\n".format(self.task_name))
        if mode == 0:
            logger.info("LIKED LIMIT mode")
            liked_limit = self.tl_v.tl_f.timeline_entry.get()
        else:
            logger.info("CONTINUE LIKED LIMIT mode")
            continue_liked_limit = self.tl_v.tl_f.timeline_entry.get()

        interval = self.util_param['liked_interval']  # いいねの間隔
        self.timeline_liked_cnt = 0  # いいねカウンター
        self.already_liked_cnt_continue = 0  # 連続する既いいねのカウンター
        time.sleep(2)

        # 読込まれたメディアの１つ目を取得
        try:
            post = self.bs.find_element_by_xpath(self.TIMELINE_MEDIA_XPATH)
        except WebDriverException:
            self.task_end('timeline', "メディアを取得できませんでした\n{}を終了します\n".format(self.task_name), "confirm TIMELINE_MEDIA_XPATH", 'ERROR')
            return

        while True:
            time.sleep(2)
            post_y = post.location['y']  # メディアの上端スクロール位置
            self.scroll_down(post_y)  # メディアの位置までスクロールする
            time.sleep(2)
            try:  # 既いいねかどうか確認
                post.find_element_by_xpath(self.TIMELINE_ALREADY_LIKE_XPATH)
                self.already_liked_cnt_continue += 1
                if mode == 0:
                    self.info.set("{}を実行中..\nいいね！ {}/{}\n既いいねのためスキップします".format(self.task_name, self.timeline_liked_cnt, liked_limit))
                else:
                    self.info.set("{}を実行中..\nいいね！ {}回\n既いいねのためスキップします".format(self.task_name, self.timeline_liked_cnt))
            except WebDriverException:  # 未いいねの場合
                try:  # いいねボタンをクリック
                    post.find_element_by_xpath(self.TIMELINE_LIKE_XPATH).click()
                    self.timeline_liked_cnt += 1
                    self.util_param['act_cnt'] += 1
                    self.already_liked_cnt_continue = 0  # リセット
                    if mode == 0:
                        self.info.set("{}を実行中..\nいいね！ {}/{}\n".format(self.task_name, self.timeline_liked_cnt, liked_limit))
                    else:
                        self.info.set("{}を実行中..\nいいね！ {}回\n".format(self.task_name, self.timeline_liked_cnt))
                    time.sleep(interval - 4)
                except WebDriverException:  # クリック失敗
                    self.info.set("{}を実行中..\nいいねを失敗しました\n".format(self.task_name))
                    logger.info("liked failed")
            if self.stop_fl:
                if mode == 0:
                    self.task_end('timeline', "{}を停止しました\n{}回中{}回いいねしました\n".format(self.task_name, liked_limit, self.timeline_liked_cnt))
                else:
                    self.task_end('timeline', "{}を停止しました\n計{}回いいねしました".format(self.task_name, self.timeline_liked_cnt))
                return
            if mode == 0 and self.timeline_liked_cnt >= liked_limit:
                self.task_end('timeline', "指定回数に到達しました\n{}を終了します\n{}回中{}回いいねしました".format(self.task_name, liked_limit, self.timeline_liked_cnt), "complete")
                return
            if mode == 1 and self.already_liked_cnt_continue >= continue_liked_limit:
                self.task_end('timeline', "既いいねが指定回数連続しました\n{}を終了します\n計{}回いいねしました".format(self.task_name, self.timeline_liked_cnt), "complete")
                return
            if self.util_param['act_cnt'] >= self.util_param['act_limit']:
                self.task_end('timeline', "今日の行動回数が上限に達しました\n{}を終了します\n計{}回いいねしました".format(self.task_name, self.timeline_liked_cnt), "reached today's limit")
                return

            # 次のメディアをスクロールしながら探す
            post = self.get_next_post(post)
            if not post:
                if self.util_v.util_f.retry.get() == 1:  # リトライ時
                    logger.info("next media not found... retry")
                    self.info.set("次のメディアが見当たりません\n{}を再度実行します\n".format(self.task_name))
                    time.sleep(5)
                    self.timeline(mode)
                else:
                    self.task_end('timeline', "メディアが取得できません\n{}を終了します\n計{}回いいねしました".format(self.task_name, self.timeline_liked_cnt), "next media not found")
                return
