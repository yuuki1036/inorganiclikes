from __init__ import get_module_logger
import threading


logger = get_module_logger(__name__)


class Trigger():  # ユーザーアクションに対する処理
    # 設定ウインドウの自動ログインチェックボックスを押した時の挙動
    def clicked_login_save(self):
        if self.util_v.util_f.login_save.get() == 1:
            self.util_v.util_f.auto_login_c.state(['!disabled'])
        else:
            self.util_v.util_f.auto_login_c.state(['disabled'])
        # 設定の変更を保存
        self.change_util_param('login_save', self.util_v.util_f.login_save.get())
        logger.debug("complete")

    # タイムラインの終了条件によってタイムラインビューの表示を切り替える
    def clicked_timeline_condition(self):
        if self.util_v.util_f.timeline_condition.get() == 0:
            self.tl_v.info_f.info.set("タイムライン上のメディアにいいねし続けます\n終了条件：指定回数達成")
            self.tl_v.tl_f.timeline_entry.set(self.util_param['timeline_liked_limit'])
        else:
            self.tl_v.info_f.info.set("タイムライン上のメディアにいいねし続けます\n終了条件：既いいねメディアが指定回数続く")
            self.tl_v.tl_f.timeline_entry.set(self.util_param['timeline_continue_liked_limit'])
        # 設定の変更を保存
        self.change_util_param('timeline_condition', self.util_v.util_f.timeline_condition.get())
        logger.debug("complete")

    # ログインボタンを押した
    def pushed_login(self):
        self.saved_user_info()  # ログイン情報を保存
        self.info.set("ログイン処理中..\ninstagramを開いています\n")
        self.display_confirmation("停止")
        self.task_fl = True
        self.task_name = 'ログイン処理'
        # 停止処理の別スレッド実行を停止ボタンに設定
        self.cf_v.cf_f.cf_b['command'] = threading.Thread(target=self.stopped_task).start
        # 別スレッドでログインタスクを実行
        threading.Thread(name='login', target=self.execute_first_time_login).start()

    # タグ検索実行ボタンを押した
    def pushed_tag_search(self):
        self.saved_tag_search_info()  # 条件を保存
        self.display_confirmation("停止")
        self.task_fl = True
        self.task_name = 'タグ検索自動いいね'
        # リトライ可能にするため、この時点でカウンターを定義する
        self.tag_search_liked_cnt = 0  # いいねカウンター
        # 停止処理の別スレッド実行を停止ボタンに設定
        self.cf_v.cf_f.cf_b['command'] = threading.Thread(name='stopper',  target=self.stopped_task).start
        # 別スレッドでタグ検索タスクを実行
        threading.Thread(name='tag', target=self.execute_task, args=[self.tag_search]).start()

    # タイムライン実行ボタンを押した
    def pushed_timeline(self):
        mode = self.util_v.util_f.timeline_condition.get()  # 終了条件を取得
        self.saved_timeline_info(mode)  # 条件を保存
        self.display_confirmation("停止")
        self.task_fl = True
        self.task_name = 'タイムライン自動いいね'
        # リトライ可能にするため、この時点でカウンターを定義する
        self.timeline_liked_cnt = 0  # いいねカウンター
        self.already_liked_cnt_continue = 0  # 連続する既いいねのカウンター
        # 停止処理の別スレッド実行を停止ボタンに設定
        self.cf_v.cf_f.cf_b['command'] = threading.Thread(name='stopper', target=self.stopped_task).start
        # 別スレッドでタイムラインタスクを実行
        threading.Thread(name='timeline', target=self.execute_task, args=[self.timeline, mode]).start()

    # フォロワー取得ボタンを押した
    def pushed_follower(self):
        self.display_confirmation("停止")
        self.task_fl = True
        self.task_name = 'フォロワーリスト取得'
        # ブラウザがヘッドレスモードであれば、新たに非ヘッドレスモードで起動する
        if self.util_param['display_browser'] == 1:
            self.display_browser()
        # 停止処理の別スレッド実行を停止ボタンに設定
        self.cf_v.cf_f.cf_b['command'] = threading.Thread(name='stopper', target=self.stopped_task).start
        # 別スレッドでフォロワー取得タスクを実行
        threading.Thread(name='follower', target=self.execute_get_follower).start()

    # フォローバックボタンを押した
    def pushed_followback(self):
        self.display_confirmation("停止")
        self.task_fl = True
        self.task_name = 'フォローバック処理'
        self.followback_l = []
        for i in range(len(self.fr_c_l)):
            if self.fr_c_v_l[i].get() == 1:
                self.followback_l.append(self.fr_c_l[i].cget('text'))
        # 停止処理の別スレッド実行を停止ボタンに設定
        self.cf_v.cf_f.cf_b['command'] = threading.Thread(name='stopper', target=self.stopped_task).start
        # 別スレッドでフォローバックタスクを実行
        threading.Thread(name='followback', target=self.execute_task, args=[self.followback]).start()
        # 2重タスク防止
        self.fl_master.withdraw()

    def pushed_unfollow(self):
        self.display_confirmation("停止")
        self.task_fl = True
        self.task_name = 'フォローやめる処理'
        self.unfollow_l = []
        for i in range(len(self.fg_c_l)):
            if self.fg_c_v_l[i].get() == 1:
                self.unfollow_l.append(self.fg_c_l[i].cget('text'))
        # 停止処理の別スレッド実行を停止ボタンに設定
        self.cf_v.cf_f.cf_b['command'] = threading.Thread(name='stopper', target=self.stopped_task).start
        # 別スレッドでフォローやめるタスクを実行
        threading.Thread(name='unfollow', target=self.execute_task, args=[self.unfollow]).start()
        # 2重タスク防止
        self.fl_master.withdraw()
