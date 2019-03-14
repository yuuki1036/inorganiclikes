from __init__ import get_module_logger
from selenium.common.exceptions import WebDriverException
import time
from task import LoginTask
from task import TagSearchTask
from task import TimelineTask
from task import GetFollowerTask
from task import FollowBackTask
from task import UnFollowTask


logger = get_module_logger(__name__)


class TaskManager(LoginTask, TagSearchTask, TimelineTask, GetFollowerTask, FollowBackTask, UnFollowTask):  # タスク実行時のラッパー処理
    def __init__(self):
        super().__init__()

    # タスク終了時に呼ばれる。確認画面の作成・表示
    # task:タスクの種類, info_str:確認ビューに表示する文字列
    # log_str:ロガー出力文字列, level:ロガーレベル
    def task_end(self, task, info_str, log_str='', level='INFO'):
        # 確認ビューセットアップ
        self.info.set(info_str)
        self.cf_v.cf_f.cf_b['text'] = "OK"
        if task == 'login':
            # ログインタスクは失敗時のみにこの関数が呼ばれる
            # ドライバーを削除する
            try:
                self.bs.close()
            except WebDriverException:
                pass
            delattr(self, 'bs')
            # 確認ボタントリガー
            self.cf_v.cf_f.cf_b['command'] = self.login_v.tkraise
            # 自動ログインの場合、確認ビューが表示されていないので表示する
            if self.util_param['auto_login'] == 1:
                self.cf_v.tkraise()
        else:  # ログインタスク以外の全て
            # 確認ボタントリガー
            self.cf_v.cf_f.cf_b['command'] = self.display_main
            # トップページにしておく
            self.bs.get(self.TOP_URL)

        # ロガーを出力
        if self.stop_fl:  # 停止処理の場合
            logger.info("{} task stopped".format(task))
            self.stop_fl = False
        else:  # 停止処理以外（正常終了・異常終了）
            if level == 'INFO':
                logger.info(log_str)
            elif level == 'ERROR':
                logger.error(log_str)

    # ログイン時のポップアップがあれば閉じる
    def close_modal(self):
        try:
            self.bs.find_element_by_xpath(self.MODAL_XPATH).click()
        except WebDriverException:
            pass

    # ドライバー作成
    def create_driver(self):
        time.sleep(1)
        self.info.set("{}を実行中..\n作業ブラウザを起動します\n".format(self.task_name))
        try:
            # 新規ウインドウを起動
            self.bs = self.web_driver_setup(self.util_param['display_browser'])
        except WebDriverException:
            logger.info("NG")
            self.info.set("google chromeがありません\nインストールしてください\n")

    # ドライバーをチェック
    def is_check_driver(self):
        self.info.set("{}を実行中..\n作業ブラウザをチェックしています\n".format(self.task_name))
        time.sleep(2)
        # bsアトリビュートを持っているか
        if not hasattr(self, 'bs'):
            return False
        # ドライバーの存在を確認
        try:
            drivers = self.bs.window_handles
        except WebDriverException:
            logger.info("driver not found")
            self.info.set("{}を実行中..\n作業ドライバーが見当たりません\n".format(self.task_name))
            return False
        # 使用できるブラウザの有無確認
        if drivers:
            logger.info("OK")
            return True
        else:
            logger.info("browser not found")
            self.info.set("{}を実行中..\n作業ブラウザが見当たりません\n".format(self.task_name))
            return False

    # インターネットの接続確認
    def is_check_network_connect(self):
        self.info.set("{}を実行中..\n通信をチェックしています\n".format(self.task_name))
        # インターネット接続エラー画面が表示されるかどうか
        try:
            self.bs.get(self.TOP_URL)
            time.sleep(3)
            self.bs.find_element_by_xpath(self.NETWORK_ERROR_XPATH)
        except WebDriverException:
            return True
        logger.info("NG")
        return False

    # ログイン状態をチェック
    def is_check_auth(self):
        self.info.set("{}を実行中..\nログイン状態をチェックしています\n".format(self.task_name))
        time.sleep(2)
        # ログアウト時のみの要素が取得されるかどうか
        try:
            self.bs.find_element_by_xpath(self.AUTH_CHECK_XPATH)
        except WebDriverException:
            return True
        logger.info("NG")
        self.info.set("{}を実行中..\n接続がタイムアウトしました\n再度ログインを試みます".format(self.task_name))
        return False

    # 初回ログイン前処理
    def execute_first_time_login(self):
        # ドライバーとインターネット接続をチェック
        if not self.is_check_driver():
            self.create_driver()
        if not self.is_check_network_connect():
            self.task_end('login', "通信できません\nインターネットの接続を確認してください\n", "network not connected")
            return
        time.sleep(2)
        # ログインタスク実行
        self.info.set("{}を実行中..\nログイン情報を入力しています\n".format(self.task_name))
        # ログインタスクは処理結果を返す
        login_status = self.login()
        if login_status == 'complete':
            logger.info("complete")
            self.info.set("{}を実行中..\nログインしました\n続いてアカウント情報を取得します".format(self.task_name))
            time.sleep(2)
            # アカウント情報を取得する
            self.get_account_info()
        elif login_status == 'failed':
            self.task_end('login', "{}に失敗しました。入力情報が\n間違っているか、一時的にログインできない状態です\nその場合はしばらく時間をおいてください".format(self.task_name), "login failed")
        elif login_status == 'stop':
            self.task_end('login', "{}を停止しました\n\n".format(self.task_name))

    # タスク実行前処理
    # task: 実行タスク関数OBJ, *args:タスクに必要な引数
    def execute_task(self, task, *args):
        # ドライバーとインターネット接続をチェック
        if not self.is_check_driver():
            self.create_driver()
        if not self.is_check_network_connect():
            self.task_end('login', "通信できません\nインターネットの接続を確認してください\n", "network not connected")
            return
        # ログイン状態をチェック
        if self.is_check_auth():
            time.sleep(3)
            # フォロワー取得タスクは真偽値を返す
            if task == self.get_follower:
                return task(*args)  # タスク実行
            else:
                task(*args)  # タスク実行
            return
        time.sleep(3)
        # ログインし直す
        self.info.set("{}を実行中..\nログイン情報を入力しています\n".format(self.task_name))
        login_status = self.login()
        if login_status == 'complete':
            logger.info("login complete")
            self.info.set("{}を実行中..\nログインしました\nタスクを継続します".format(self.task_name))
            time.sleep(3)
            # ログインしたのでタスクを実行する
            if task == self.get_follower:
                return task(*args)
            else:
                task(*args)
        elif login_status == 'failed':
            self.task_end('login', "ログインに失敗しました\n入力情報を確認してもう一度試してください\n{}を終了します".format(self.task_name), "login failed")
        elif login_status == 'stop':
            self.task_end('check', "ログイン処理を停止しました\n{}を終了します\n".format(self.task_name))

    # フォロワー取得タスクラッパー処理
    def execute_get_follower(self):
        # タスクを実行する
        if not self.execute_task(self.get_follower):
            return
        # タスク完了時はtask_endを呼ばないので必要な処理を行う
        self.bs.get(self.TOP_URL)
        # ２つのフォロワーセットから一方的リストを作成
        self.follower_os_l = list(self.follower_s.difference(self.following_s))
        self.following_os_l = list(self.following_s.difference(self.follower_s))
        # リストのユーザー数を取得
        self.follower_os_n = len(self.follower_os_l)
        self.following_os_n = len(self.following_os_l)
        # フォロワーリストウインドウを立ち上げ
        self.deiconify_follower_window()
        logger.info("complete")
