import tkinter as tk
from tkinter import ttk
from . import frame


class TitleView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.title_f = frame.TitleFrame(self)


class LoginView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.info_f = frame.InfoFrame(self)
        self.login_f = frame.LoginFrame(self)
        self.eq_f = frame.QuitAndSettingFrame(self)

        self.info_f.info.set("ログインしてください\n")


class MainView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.status_f = frame.StatusFrame(self)
        self.act_f = frame.ActionFrame(self)
        self.eq_f = frame.QuitAndSettingFrame(self)


class TagSearchView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.info_f = frame.InfoFrame(self)
        self.tag_f = frame.TagSearchFrame(self)
        self.eq_f = frame.QuitAndSettingFrame(self)

        self.info_f.info.set("タグ検索結果にいいねし続けます\nタグは日本語もOKです")
        self.eq_f.etc_b['text'] = "戻る"


class TimeLineView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.info_f = frame.InfoFrame(self)
        self.tl_f = frame.TimeLineFrame(self)
        self.eq_f = frame.QuitAndSettingFrame(self)

        self.info_f.info.set("タイムライン上のメディアにいいねします\n")
        self.eq_f.etc_b['text'] = "戻る"


class FollowerView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.info_f = frame.InfoFrame(self)
        self.fl_f = frame.FollowerFrame(self)
        self.eq_f = frame.QuitAndSettingFrame(self)

        self.info_f.info.set("フォロワーを取得して\nフォローしたり、やめたりできます\nこの作業はブラウザを立ち上げます")
        self.eq_f.etc_b['text'] = "戻る"


class ConfirmationView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.info_f = frame.InfoFrame(self)
        self.cf_f = frame.ConfirmationFrame(self)
        self.quit_f = frame.QuitFrame(self)


class ProcessingView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.info_f = frame.InfoFrame(self)
        self.quit_f = frame.QuitFrame(self)


class FollowerWindowView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        nb = ttk.Notebook(self)
        self.fr_tbf = ttk.Frame(nb)
        self.fg_tbf = ttk.Frame(nb)

        nb.add(self.fr_tbf, text='　　　　一方的フォロワー　　　　')
        nb.add(self.fg_tbf, text='　　　一方的フォローイング　　　')

        self.fr_f = frame.OneSidedFollowerFrame(self.fr_tbf)
        self.fg_f = frame.OneSidedFollowingFrame(self.fg_tbf)

        nb.pack()


class UtilView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.util_f = frame.UtilFrame(self)
        self.util_f.quit_b['command'] = master.withdraw
