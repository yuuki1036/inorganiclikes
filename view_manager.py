from __init__ import get_module_logger
import tkinter as tk
from tkinter import ttk
import view


logger = get_module_logger(__name__)


class ViewManager():  # GUIの親クラス
    def create_view(self):
        # メインウインドウのラッパーフレーム作成・配置
        master = ttk.Frame(self.master)
        master.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))

        # メインウインドウの各種ビューフレームを作成
        self.login_v = view.LoginView(master)  # ログインビュー
        self.main_v = view.MainView(master)  # メインコントロールビュー
        self.tag_v = view.TagSearchView(master)  # タグ検索ビュー
        self.tl_v = view.TimeLineView(master)  # タイムラインビュー
        self.fl_v = view.FollowerView(master)  # フォロワービュー
        self.cf_v = view.ConfirmationView(master)  # タスクの進行状況ビュー
        self.ps_v = view.ProcessingView(master)  # 処理中ビュー
        self.title_v = view.TitleView(master)  # スタートアップビュー

        # その他ウインドウの作成
        self.util_v = view.UtilView(self.util_master)  # 設定ウインドウ
        self.flw_v = view.FollowerWindowView(self.fl_master)  # フォロワーリストウインドウ

        self.set_style()
        self.main_window_setup()
        self.util_window_setup()
        self.follower_window_setup()
        logger.debug("complete")

    # ウィジェットのスタイル設定
    def set_style(self):
        self.style = ttk.Style()  # スタイルクラス呼び出し
        self.style.configure('TLabel', font=('Hiragino Maru Gothic ProN', '12'))
        self.style.configure('TEntry', font=('Hiragino Maru Gothic ProN', '12'))
        self.style.configure('title.TLabel', font=('futura', '23', 'bold'))
        self.style.configure('TButton', font=('Hiragino Maru Gothic ProN', '12'))
        self.style.configure('TCheckbutton', font=('Hiragino Maru Gothic ProN', '12'))
        self.style.configure('TCombobox', font=('Hiragino Maru Gothic ProN', '12'))
        self.style.configure('TEntry', font=('Hiragino Maru Gothic ProN', '12'))
        self.style.configure('TRadiobutton', font=('Hiragino Maru Gothic ProN', '12'))
        self.style.configure('TNotebook', font=('Hiragino Maru Gothic ProN', '12'))

    # メインウインドウウィジェット追加設定
    def main_window_setup(self):
        # LoginView
        self.login_v.login_f.login_exec_b['command'] = self.pushed_login
        self.login_v.eq_f.etc_b['command'] = self.util_master.deiconify
        self.login_v.login_f.username.set(self.util_param['username'])
        self.login_v.login_f.password.set(self.util_param['password'])
        self.login_v.eq_f.quit_b['command'] = self.quit_application
        self.login_v.eq_f.help_b['command'] = self.open_help
        # MainView
        self.main_v.act_f.tag_b['command'] = self.tag_v.tkraise
        self.main_v.act_f.tl_b['command'] = self.display_timeline
        self.main_v.act_f.fl_b['command'] = self.fl_v.tkraise
        self.main_v.eq_f.etc_b['command'] = self.util_master.deiconify
        self.main_v.eq_f.quit_b['command'] = self.quit_application
        self.main_v.eq_f.help_b['command'] = self.open_help
        # TagSearchView
        self.tag_v.tag_f.tag.set(self.util_param['tag_name'])
        self.tag_v.tag_f.liked_limit.set(self.util_param['tag_liked_limit'])
        self.tag_v.tag_f.tag_exec_b['command'] = self.pushed_tag_search
        self.tag_v.eq_f.etc_b['command'] = self.display_main
        self.tag_v.eq_f.help_b['command'] = self.open_help
        self.tag_v.eq_f.quit_b['command'] = self.quit_application
        # TimeLineView
        self.tl_v.tl_f.tl_exec_b['command'] = self.pushed_timeline
        self.tl_v.eq_f.etc_b['command'] = self.display_main
        self.tl_v.eq_f.help_b['command'] = self.open_help
        self.tl_v.eq_f.quit_b['command'] = self.quit_application
        if self.util_param['timeline_condition'] == 0:
            self.tl_v.info_f.info.set("タイムライン上のメディアにいいねし続けます\n終了条件：指定回数達成")
            self.tl_v.tl_f.timeline_entry.set(self.util_param['timeline_liked_limit'])
        else:
            self.tl_v.info_f.info.set("タイムライン上のメディアにいいねし続けます\n終了条件：既いいねメディアが指定回数続く")
            self.tl_v.tl_f.timeline_entry.set(self.util_param['timeline_continue_liked_limit'])
        # FollowerView
        self.fl_v.fl_f.fl_exec_b['command'] = self.pushed_follower
        self.fl_v.fl_f.fl_deic_b['command'] = self.deiconify_follower_window
        self.fl_v.fl_f.fl_deic_b.state(['disabled'])
        self.fl_v.eq_f.etc_b['command'] = self.display_main
        self.fl_v.eq_f.quit_b['command'] = self.quit_application
        self.fl_v.eq_f.help_b['command'] = self.open_help
        # ConfirmationView
        self.cf_v.cf_f.cf_b['command'] = self.display_main
        self.cf_v.quit_f.quit_b['command'] = self.quit_application

    # 設定ウインドウウィジェット追加設定
    def util_window_setup(self):
        # ログイン情報保存
        self.util_v.util_f.login_save_c['command'] = self.clicked_login_save
        # 自動ログイン
        self.util_v.util_f.auto_login_c['command'] = lambda: self.change_util_param('auto_login', self.util_v.util_f.auto_login.get())
        # ヘッドレス選択
        self.util_v.util_f.display_browser_c['command'] = lambda: self.change_util_param('display_browser', self.util_v.util_f.display_browser.get())
        # 行動回数
        self.util_v.util_f.act_limit_cb.set(self.util_param['act_limit'])
        self.util_v.util_f.act_limit_cb.bind('<<ComboboxSelected>>', lambda e: self.change_util_param('act_limit', self.util_v.util_f.act_limit_cb.get()))
        # いいね待機時間
        self.util_v.util_f.liked_interval_cb.set(self.util_param['liked_interval'])
        self.util_v.util_f.liked_interval_cb.bind('<<ComboboxSelected>>', lambda e: self.change_util_param('liked_interval', self.util_v.util_f.liked_interval_cb.get()))
        # アカウント情報更新間隔
        self.util_v.util_f.account_update_interval_cb.set(self.util_param['account_update_interval'])
        self.util_v.util_f.account_update_interval_cb.bind('<<ComboboxSelected>>', lambda e: self.change_util_param('account_update_interval', self.util_v.util_f.account_update_interval_cb.get()))
        # タイムラインの終了条件
        self.util_v.util_f.timeline_condition.set(self.util_param['timeline_condition'])
        self.util_v.util_f.timeline_condition_r1['command'] = self.clicked_timeline_condition
        self.util_v.util_f.timeline_condition_r2['command'] = self.clicked_timeline_condition
        # リトライ
        self.util_v.util_f.retry_c['command'] = lambda: self.change_util_param('retry', self.util_v.util_f.retry.get())

    # フォロワーリストウインドウウィジェット追加設定
    def follower_window_setup(self):
        # OneSidedFollowerFrame
        self.flw_v.fr_f.ud_b['command'] = self.update_follower_window
        self.flw_v.fr_f.quit_b['command'] = self.withdraw_follower_window
        self.flw_v.fr_f.exec_b['command'] = self.pushed_followback
        self.flw_v.fr_f.all_on_c['command'] = lambda: self.checked_all(self.flw_v.fr_f.all_on_c_v.get(), self.fr_c_v_l)
        # OneSidedFollowingFrame
        self.flw_v.fr_f.ud_b['command'] = self.update_follower_window
        self.flw_v.fg_f.quit_b['command'] = self.withdraw_follower_window
        self.flw_v.fg_f.exec_b['command'] = self.pushed_unfollow
        self.flw_v.fg_f.all_on_c['command'] = lambda: self.checked_all(self.flw_v.fg_f.all_on_c_v.get(), self.fg_c_v_l)

    # 一方的フォロワーリストからチェックボックス作成・配置
    def put_follower_list(self):
        self.flw_v.fr_f.fr_l['text'] = "あなたのフォロワーは全部で{}人\nそのうち{}人があなたを一方的にフォローしています\nフォローバックしたいユーザーを選択しててください".format(self.follower_n, self.follower_os_n)
        idx, row, column = 0, 0, 0
        # 既に作成されているウィジェットを削除
        if hasattr(self, 'fr_c_l'):
            for i in range(len(self.fr_c_l)):
                self.fr_c_l[i].destroy()
        self.fr_c_v_l = []  # チェックボックスの値リスト
        self.fr_c_l = []  # チェックボックスのリスト
        while idx < self.follower_os_n:
            c_val = tk.IntVar()
            fr_c = ttk.Checkbutton(self.flw_v.fr_f.sc_a, text=self.follower_os_l[idx], variable=c_val, onvalue=1, offvalue=0)
            fr_c.grid(row=row, column=column, sticky=tk.W)
            c_val.set(0)  # 未選択にしておく
            self.fr_c_v_l.append(c_val)
            self.fr_c_l.append(fr_c)
            idx += 1
            # 3列で配置する
            if column < 2:
                column += 1
            else:
                column = 0
                row += 1
        # キャンバスウィジェットを更新
        self.flw_v.fr_f.sc_a.update()

    # 一方的フォロー中リストからチェックボックス作成・配置
    def put_following_list(self):
        self.flw_v.fg_f.fg_l['text'] = "あなたがフォローしているユーザーは全部で{}人\nそのうち{}人をあなたが一方的にフォローしています\nフォローをやめたいユーザーを選択してください".format(self.following_n, self.following_os_n)
        idx, row, column = 0, 0, 0
        # 既に作成されているウィジェットを削除
        if hasattr(self, 'fg_c_l'):
            for i in range(len(self.fg_c_l)):
                self.fg_c_l[i].destroy()
        self.fg_c_v_l = []  # チェックボックスの値リスト
        self.fg_c_l = []  # チェックボックスのリスト
        while idx < self.following_os_n:
            c_val = tk.IntVar()
            fg_c = ttk.Checkbutton(self.flw_v.fg_f.sc_a, text=self.following_os_l[idx], variable=c_val, onvalue=1, offvalue=0)
            fg_c.grid(row=row, column=column, sticky=tk.W)
            c_val.set(0)  # 未選択にしておく
            self.fg_c_v_l.append(c_val)
            self.fg_c_l.append(fg_c)
            idx += 1
            # 3列で配置する
            if column < 2:
                column += 1
            else:
                column = 0
                row += 1
        # キャンバスウィジェットを更新
        self.flw_v.fg_f.sc_a.update()
