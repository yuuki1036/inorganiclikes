from __init__ import get_module_logger
from selenium import webdriver
from pysqlcipher3 import dbapi2 as sqlite
import datetime
import os
import inspect


logger = get_module_logger(__name__)


class WebDriver():
    def web_driver_setup(self, mode):
        # chromedriverのパス作成
        current_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
        chromedriver = os.path.join(current_folder, "chromedriver")
        options = webdriver.ChromeOptions()  # 起動オプション
        if mode == 0:
            pos_x, pos_y = self.util_param['browser_pos'].split('-')
            options.add_argument('--window-size=800,900')
            options.add_argument('--window-position={},{}'.format(pos_x, pos_y))
        else:
            options.add_argument('--headless')  # ヘッドレスモード
            options.add_argument('--disable-gpu')  # ヘッドレスモードに必要
            options.add_argument('--window-size=800,900')
        # ドライバー作成。ブラウザが起動する
        self.bs = webdriver.Chrome(executable_path=chromedriver, options=options)
        return self.bs


class DB():
    def connect_db(self):
        # sqliteのコネクトは作成も兼ねている
        self.conn = sqlite.connect("util.db")
        self.c = self.conn.cursor()  # カーソル
        # 暗号化したDBにアクセス
        self.c.execute("PRAGMA key={}".format(self.db_key))

    def setup_db(self):
        self.connect_db()
        # テーブル存在確認
        sql = "SELECT * FROM sqlite_master WHERE type='table'"
        self.c.execute(sql)  # テーブル一覧請求
        if not self.c.fetchall():
            self.create_table()

        # ユーティリティ辞書作成
        db_col_li = self.c.execute('SELECT * FROM util')  # コラムリスト取得
        # pythonリストに変換
        db_col_li = list(map(lambda x: x[0], db_col_li.description))
        # レコード取得
        db_record = self.c.execute("SELECT * FROM util WHERE id=1")
        db_record = db_record.fetchall()[0]
        db_record = list(db_record)

        self.util_param = dict(zip(db_col_li, db_record))
        logger.debug(self.util_param)

        # パラメータの状態に合わせて初期化
        self.util_initialize_setting()
        logger.debug("complete")

        self.conn.close()

    # アプリケーション初回起動時
    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS util (id INTEGER, username TEXT, password TEXT, time TEXT, elapsed_time INTEGER, login_elapsed_time INTEGER, tag_elapsed_time INTEGER, timeline_elapsed_time INTEGER, login_save INTEGER,  auto_login INTEGER, display_browser INTEGER, act_cnt INTEGER, act_limit INTEGER, liked_interval INTEGER, account_update_interval INTEGER, root_pos TEXT, util_pos TEXT, fl_pos TEXT, browser_pos TEXT, browser_size TEXT, tag_name TEXT, tag_liked_limit INTEGER, timeline_condition INTEGER, timeline_liked_limit INTEGER, timeline_continue_liked_limit INTEGER, retry INTEGER)"
        self.c.execute(sql)
        # 初期パラメータ
        record = "INSERT INTO util VALUES (1, '', '', '2019-02-15', 0, 40000, 40000, 40000, 1, 0, 0, 0, 500, 30, 10, '+1000+500', '+900+100', '+1100+100', '0-65', '', '', 0, 0, 30, 5, 1)"
        self.c.execute(record)
        self.conn.commit()

    def util_initialize_setting(self):
        # ユーザー情報の削除
        if self.util_param['login_save'] == 0:
            self.util_param['username'] = ''
            self.util_param['password'] = ''
            sql = "UPDATE util SET username='', password='' WHERE id=1"
            self.execute_db(sql)
            logger.info("deleted user info")

    # 前回起動時からの経過時間
    def execute_time(self):
        # DB保存時間取得
        db_date = datetime.datetime.strptime(self.util_param['time'], '%Y-%m-%d').date()
        now_date = datetime.date.today()  # 現在時刻

        elapsed_time = now_date - db_date

        if elapsed_time.days >= 1:  # 1日以上経過時
            self.util_param['time'] = now_date.strftime('%Y-%m-%d')
            self.util_param['act_cnt'] = 0  # 行動回数リセット
            sql = "UPDATE util SET time='{0[time]}', act_cnt={0[act_cnt]} WHERE id=1".format(self.util_param)
            self.execute_db(sql)
            logger.info("reset act_cnt")

    # SQL文の実行
    def execute_db(self, sql):
        self.connect_db()
        try:
            self.c.execute(sql)
        except sqlite.OperationalError:
            logger.error("failed sql>>{}".format(sql))
        self.conn.commit()
        self.conn.close()


class Util(DB, WebDriver):
    def __init__(self):
        super().__init__()
