import tkinter as tk
from tkinter import ttk
from .helper import Scrollable


class TitleFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.title_l = ttk.Label(self, text="InorganicLikes", style="title.TLabel")
        self.version_l = ttk.Label(self, text="ver.1.0")
        self.info_l = ttk.Label(self, text="ログインしています..")

        ttk.Label(self).pack()
        self.title_l.pack()
        self.info_l.pack()
        ttk.Label(self).pack()
        self.version_l.pack()


class InfoFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X)
        self.info = tk.StringVar()
        self.info_l = ttk.Label(self, textvariable=self.info, anchor="center")

        self.info_l.pack()


class LoginFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X, pady=5)
        self.username = tk.StringVar()
        self.un_l = ttk.Label(self, text="   username")
        self.un_e = ttk.Entry(self, textvariable=self.username, width=19)
        self.password = tk.StringVar()
        self.pw_l = ttk.Label(self, text="password")
        self.pw_e = ttk.Entry(self, show="*", textvariable=self.password, width=19)
        self.login_exec_b = ttk.Button(self, text="login")

        self.un_l.grid(row=0, column=0, sticky=tk.E)
        self.un_e.grid(row=0, column=1, sticky=tk.W)
        self.pw_l.grid(row=1, column=0, sticky=tk.E)
        self.pw_e.grid(row=1, column=1, sticky=tk.W)
        self.login_exec_b.grid(row=1, column=2, sticky=tk.E)


class StatusFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self['relief'] = 'raised'
        self['borderwidth'] = 5
        self.pack(fill=tk.X)
        self.up_l = ttk.Label(self, anchor="center")
        self.low_l = ttk.Label(self, anchor="center")

        self.up_l.pack()
        self.low_l.pack()


class ActionFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X, pady=7)
        self.tl_b = ttk.Button(self, text="タイムライン", width=10)
        self.tag_b = ttk.Button(self, text="タグ検索", width=10)
        self.fl_b = ttk.Button(self, text="フォロワー", width=10)

        self.tl_b.grid(row=0, column=0)
        self.tag_b.grid(row=0, column=1)
        self.fl_b.grid(row=0, column=2)


class TagSearchFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X, pady=5)
        self.tag = tk.StringVar()
        self.tag_l = ttk.Label(self, text="               タグ")
        self.tag_e = ttk.Entry(self, width=17, textvariable=self.tag)
        self.liked_limit = tk.IntVar()
        self.ll_l = ttk.Label(self, text="回数")
        self.ll_e = ttk.Entry(self, width=17, textvariable=self.liked_limit)
        self.tag_exec_b = ttk.Button(self, text="実行")

        self.tag_l.grid(row=0, column=0, sticky=tk.E)
        self.tag_e.grid(row=0, column=1, sticky=tk.W)
        self.ll_l.grid(row=1, column=0, sticky=tk.E)
        self.ll_e.grid(row=1, column=1, sticky=tk.W)
        self.tag_exec_b.grid(row=1, column=2, padx=1, sticky=tk.W)


class TimeLineFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X, pady=15)
        self.tl_l = ttk.Label(self, text="　　　　　　回数")
        self.timeline_entry = tk.IntVar()
        self.tl_e = ttk.Entry(self, width=8, textvariable=self.timeline_entry)
        self.tl_exec_b = ttk.Button(self, text="実行")

        self.tl_l.grid(row=0, column=0, sticky=tk.E)
        self.tl_e.grid(row=0, column=1, sticky=tk.W)
        self.tl_exec_b.grid(row=0, column=2, padx=1, sticky=tk.W)


class FollowerFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X, pady=7)
        self.fl_exec_b = ttk.Button(self, text="フォロワー取得", width=12)
        self.fl_deic_b = ttk.Button(self, text="一覧表示", width=12)

        self.fl_exec_b.grid(row=0, column=0)
        self.fl_deic_b.grid(row=0, column=1)


class ConfirmationFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X)
        self.cf_b = ttk.Button(self)

        self.cf_b.pack(pady=5)


class QuitFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X, side=tk.BOTTOM)
        self.quit_b = ttk.Button(self, text="終了")

        self.quit_b.pack(side=tk.RIGHT)


class QuitAndSettingFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.X, side=tk.BOTTOM)
        self.quit_b = ttk.Button(self, text="終了")
        self.etc_b = ttk.Button(self, text="設定")
        self.help_b = ttk.Button(self, text="ヘルプ")

        self.etc_b.pack(side=tk.LEFT)
        self.help_b.pack(side=tk.LEFT)
        self.quit_b.pack(side=tk.RIGHT)


class OneSidedFollowerFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH)
        self.dc_f = ttk.Frame(self)
        self.fl_sc = ttk.Frame(self)
        self.act_f = ttk.Frame(self)

        self.dc_f.pack(fill=tk.X)
        self.fl_sc.pack(fill=tk.X, pady=5)
        self.act_f.pack(fill=tk.X)

        self.fr_l = ttk.Label(self.dc_f, text="")
        self.ud_b = ttk.Button(self.dc_f, text="更新")
        self.sc_a = Scrollable(self.fl_sc)
        self.all_on_c_v = tk.IntVar()
        self.all_on_c = ttk.Checkbutton(self.act_f, text="全て選択", variable=self.all_on_c_v, onvalue=1, offvalue=0)
        self.exec_b = ttk.Button(self.act_f, text="フォローバック")
        self.quit_b = ttk.Button(self.act_f, text="閉じる")

        self.fr_l.pack(fill=tk.X)
        self.ud_b.pack(anchor=tk.E, padx=5)
        self.all_on_c.grid(row=0, column=0, sticky=tk.W)
        self.exec_b.grid(row=0, column=1, padx=169)
        self.quit_b.grid(row=0, column=2, sticky=tk.E)

        self.all_on_c_v.set(0)


class OneSidedFollowingFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=tk.BOTH)
        self.dc_f = ttk.Frame(self)
        self.fl_sc = ttk.Frame(self)
        self.act_f = ttk.Frame(self)

        self.dc_f.pack(fill=tk.X)
        self.fl_sc.pack(fill=tk.X, pady=5)
        self.act_f.pack(fill=tk.X)

        self.fg_l = ttk.Label(self.dc_f, text="")
        self.ud_b = ttk.Button(self.dc_f, text="更新")
        self.sc_a = Scrollable(self.fl_sc)
        self.all_on_c_v = tk.IntVar()
        self.all_on_c = ttk.Checkbutton(self.act_f, text="全て選択", variable=self.all_on_c_v, onvalue=1, offvalue=0)
        self.exec_b = ttk.Button(self.act_f, text="フォローをやめる")
        self.quit_b = ttk.Button(self.act_f, text="閉じる")

        self.fg_l.pack(fill=tk.X)
        self.ud_b.pack(anchor=tk.E, padx=5)
        self.all_on_c.grid(row=0, column=0, sticky=tk.W)
        self.exec_b.grid(row=0, column=1, padx=163)
        self.quit_b.grid(row=0, column=2, sticky=tk.E)

        self.all_on_c_v.set(0)


class UtilFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=7, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.login_save = tk.IntVar()
        self.login_save_c = ttk.Checkbutton(self, text="ログイン情報を保存", variable=self.login_save)
        self.auto_login = tk.IntVar()
        self.auto_login_c = ttk.Checkbutton(self, text="起動時に自動的にログインする（ログイン情報保存時のみ）", variable=self.auto_login)
        self.display_browser = tk.IntVar()
        self.display_browser_c = ttk.Checkbutton(self, text="作業ブラウザを表示しない（動作が少し軽くなります）", variable=self.display_browser)

        self.act_limit_l = ttk.Label(self, text="1日の行動回数上限（回）推奨500回以下")
        self.act_limit_cb = ttk.Combobox(self, values=(300, 350, 400, 450, 500, 550, 600, 650, 700), state='readonly', width=7)

        self.liked_interval_l = ttk.Label(self, text="いいねの間隔（秒）推奨30秒以上")
        self.liked_interval_cb = ttk.Combobox(self, values=(20, 25, 30, 35, 40, 45, 50, 55, 60), state='readonly', width=7)

        self.account_update_interval_l = ttk.Label(self, text="アカウント情報（フォロワーなど）更新間隔（分）")
        self.account_update_interval_cb = ttk.Combobox(self, values=(1, 3, 5, 10, 20, 30, 60), state='readonly', width=7)
        self.account_update_interval_al = ttk.Label(self, text="※更新時に5〜10秒間通信します")

        self.timeline_condition = tk.IntVar()
        self.timeline_condition_l = ttk.Label(self, text="タイムライン終了条件")
        self.timeline_condition_r1 = ttk.Radiobutton(self, text="いいねの回数が指定した数に達した場合", value=0, variable=self.timeline_condition)
        self.timeline_condition_r2 = ttk.Radiobutton(self, text="既にいいねをしたメディアが指定した数だけ連続した場合", value=1, variable=self.timeline_condition)

        self.retry = tk.IntVar()
        self.retry_c = ttk.Checkbutton(self, text="読込みエラーで作業が中断した場合、リトライする", variable=self.retry)

        self.quit_b = ttk.Button(self, text="閉じる")

        self.login_save_c.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.auto_login_c.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.display_browser_c.grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.act_limit_l.grid(row=3, column=0, sticky=tk.W)
        self.act_limit_cb.grid(row=3, column=1, sticky=tk.E)
        self.liked_interval_l.grid(row=5, column=0, sticky=tk.W)
        self.liked_interval_cb.grid(row=5, column=1, sticky=tk.E)
        self.account_update_interval_l.grid(row=7, column=0, sticky=tk.W)
        self.account_update_interval_cb.grid(row=7, column=1, sticky=tk.E)
        self.account_update_interval_al.grid(row=8, column=0, sticky=tk.W)
        ttk.Label(self).grid(row=9, column=0)
        self.timeline_condition_l.grid(row=10, column=0, sticky=tk.W)
        self.timeline_condition_r1.grid(row=11, column=0, sticky=tk.W)
        self.timeline_condition_r2.grid(row=12, column=0, sticky=tk.W)
        ttk.Label(self).grid(row=13, column=0)
        self.retry_c.grid(row=14, column=0, columnspan=2, sticky=tk.W)
        self.quit_b.grid(row=15, column=1, pady=1, sticky=tk.E)
