from __init__ import get_module_logger
import threading
import time
import trigger


logger = get_module_logger(__name__)


class Controller(trigger.Trigger):  # メインモデルクラス
    def __init__(self):
        super().__init__()

    # メインコントロールビューのステータスを更新する
    def update_status(self):
        # 表示の書換え
        self.st_info['text'] = "@{}   {}/{}".format(self.login_v.login_f.username.get(), self.util_param['act_cnt'], self.util_param['act_limit'])
        self.main_v.status_f.low_l['text'] = "投稿{}件  フォロワー{}人  フォロー中{}人".format(self.post_n, self.follower_n, self.following_n)
        # 行動回数を保存
        sql = "UPDATE util SET act_cnt={0[act_cnt]} WHERE id=1".format(self.util_param)
        self.execute_db(sql)
        # 経過時間をチェック（行動回数をリセットするため）
        self.execute_time()
        logger.info("complete")

    # ユーザーのログイン情報を保存する
    def saved_user_info(self):
        if self.util_param['login_save'] == 1:
            sql = "UPDATE util SET username='{}', password='{}' WHERE id=1".format(self.login_v.login_f.username.get(), self.login_v.login_f.password.get())
            self.execute_db(sql)
            logger.info('saving complete')

    # タグ検索自動いいねの指定条件を保存する
    def saved_tag_search_info(self):
        sql = "UPDATE util SET tag_name='{}', tag_liked_limit={} WHERE id=1".format(self.tag_v.tag_f.tag.get(), self.tag_v.tag_f.liked_limit.get())
        self.execute_db(sql)
        logger.info('saving complete')

    # 設定ウインドウでの設定の変更を保存する
    def change_util_param(self, key, val):
        self.util_param[key] = val
        sql = "UPDATE util SET {}={} WHERE id=1".format(key, val)
        self.execute_db(sql)
        logger.info("{} -> {}".format(key, val))

    # スタートアップビューを表示
    def display_startup(self):
        if self.util_param['username'] == '' or self.util_param['auto_login'] == 0:
            # 手動ログイン時
            logger.info("MANUAL mode")
            self.title_v.title_f.info_l['text'] = "ようこそ"
            self.master.deiconify()  # メインウインドウ表示
            time.sleep(1)
            self.login_v.tkraise()  # ログインビューを表示
        else:
            # 自動ログイン時
            logger.info("AUTO mode")
            self.master.deiconify()  # メインウインドウ表示

            # pushed_loginを介さないので、実行前設定を行う
            self.task_fl = True
            self.task_name = 'ログイン処理'
            # 別スレッドでログインタスクを実行
            threading.Thread(name='login', target=self.execute_first_time_login).start()

    # メインビューを表示
    def display_main(self):
        self.update_status()
        self.main_v.tkraise()
        # 確認ビューの時にアカウント情報更新タスクがかかると
        # 確認ビューの表示が変更されるため、OKボタンを押して
        # メインビューに戻った時にタスクフラグを下ろす
        self.task_fl = False
        logger.info("SHOW")

    # タイムラインビューを表示
    def display_timeline(self):
        # 終了条件設定に応じた表示を作成
        self.clicked_timeline_condition()
        self.tl_v.tkraise()

    # 確認ビューを表示（タスク終了時）
    # str:ボタンに表示する文字列
    def display_confirmation(self, str="OK"):
        self.cf_v.cf_f.cf_b['text'] = str
        self.cf_v.tkraise()
        logger.info("SHOW")

    # タイムライン指定条件を保存
    # mode: 0(指定回数達成), 1(既いいね連続回数)
    def saved_timeline_info(self, mode):
        if mode == 0:
            sql = "UPDATE util SET timeline_liked_limit={} WHERE id=1".format(self.tl_v.tl_f.timeline_entry.get())
        else:
            sql = "UPDATE util SET timeline_continue_liked_limit={} WHERE id=1".format(self.tl_v.tl_f.timeline_entry.get())
        self.execute_db(sql)
        logger.info('saving complete')

    # フォロワーリストウインドウを表示
    def deiconify_follower_window(self):
        # フォロワーリスト表示時はメインウインドウの他タスク及び更新を実行させない
        self.task_fl = True
        self.ps_v.info_f.info.set("フォロワーリストを表示します\n作業を選択してください\n終了時は閉じるボタンを押してください")
        self.ps_v.tkraise()
        # リストからチェックボックスを作成
        self.put_follower_list()
        self.put_following_list()
        # 先にウインドウが立ち上がってしまうため少し待機
        self.master.after(3000, self.fl_master.deiconify)
        # フォロワーリスト表示画面を有効にする
        self.fl_v.fl_f.fl_deic_b.state(['!disabled'])
        logger.info("SHOW")

    # フォロワーリストウインドウを閉じる
    def withdraw_follower_window(self):
        self.task_fl = False
        self.fl_master.withdraw()
        self.fl_v.tkraise()
        logger.info("CLOSE")
