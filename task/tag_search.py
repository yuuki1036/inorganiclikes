from __init__ import get_module_logger
from selenium.common.exceptions import WebDriverException
import time
import urllib.parse


logger = get_module_logger(__name__)


class TagSearchTask():
    def tag_search(self):
        logger.info("START")
        interval = self.util_param['liked_interval']  # いいねの間隔
        self.info.set("{}を実行中..\nタグ検索画面を開きます\n".format(self.task_name))
        liked_limit = self.tag_v.tag_f.liked_limit.get()  # 指定した回数
        tag_name = self.tag_v.tag_f.tag.get()  # 検索タグ
        # タグ検索URL作成
        encoded_tag = urllib.parse.quote(tag_name)  # エンコード
        self.TAG_SEARCH_URL = self.TAG_SEARCH_URL.format(encoded_tag)
        time.sleep(1)

        try:
            # 検索結果ページにアクセス
            self.bs.get(self.TAG_SEARCH_URL)
            time.sleep(3)
            # メディアを選択し、ポップアップさせる
            self.bs.find_element_by_xpath(self.TAG_MEDIA_XPATH).click()
        except WebDriverException:
            self.task_end('tag_search', "メディアを取得できませんでした\n{}を終了します\n".format(self.task_name), "confirm TAG_MEDIA_XPATH", 'ERROR')
            return
        self.info.set("{}を実行中..\nメディアを選択、いいねを開始します\n".format(self.task_name))

        # いいねとメディア移動を繰り返す
        while True:
            time.sleep(5)
            try:
                # 既いいねチェック
                self.bs.find_element_by_xpath(self.TAG_ALREADY_LIKE_XPATH)
                # 次のメディアへ
                self.bs.find_element_by_xpath(self.TAG_NEXT_MEDIA_XPATH).click()
                self.info.set("{}を実行中..\n# {}\n既いいねのためスキップします".format(self.task_name, tag_name))
                logger.info("already liked")
                continue
            except WebDriverException:
                try:
                    # 未いいねなのでいいねする
                    self.bs.find_element_by_xpath(self.TAG_LIKE_XPATH).click()
                    self.tag_search_liked_cnt += 1
                    self.util_param['act_cnt'] += 1
                    self.info.set("{}を実行中..\n# {}\nいいね！ {}/{}".format(self.task_name, tag_name, self.tag_search_liked_cnt, liked_limit))
                    time.sleep(interval-5)
                    # 次のメディアへ
                    self.bs.find_element_by_xpath(self.TAG_NEXT_MEDIA_XPATH).click()
                except WebDriverException:
                    try:  # いいね失敗
                        self.bs.find_element_by_xpath(self.TAG_NEXT_MEDIA_XPATH).click()
                        self.info.set("{}を実行中..\n# {}\nメディアが表示されません。スキップします".format(self.task_name, tag_name))
                        logger.info("media skip")
                    except WebDriverException:
                        if self.util_v.util_f.retry.get() == 1:
                            logger.info("next media not found... retry")
                            self.info.set("次のメディアが見当たりません\n{}を再度実行します\n".format(self.task_name))
                            time.sleep(5)
                            self.tag_search()
                            return
                        else:
                            self.task_end('tag_search', "次のメディアが見当たりません\n{}を終了します\n{}回中{}回いいねしました".format(self.task_name, liked_limit, self.tag_search_liked_cnt), "next media not found")
                        return
            if self.stop_fl:
                self.task_end('tag_search', "{}を停止しました\n{}回中{}回いいねしました\n".format(self.task_name, liked_limit, self.tag_search_liked_cnt))
                return
            if self.tag_search_liked_cnt >= liked_limit:
                self.task_end('tag_search', "指定回数に到達しました\n{}を終了します\n{}回中{}回いいねしました".format(self.task_name, liked_limit, self.tag_search_liked_cnt), "complete")
                return
            if self.util_param['act_cnt'] >= self.util_param['act_limit']:
                self.task_end('tag_search', "今日の行動回数が上限に達しました\n{}を終了します\n{}回中{}回いいねしました".format(self.task_name, liked_limit, self.tag_search_liked_cnt), "reached today's limit")
                return
