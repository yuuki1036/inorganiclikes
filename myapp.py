from __init__ import get_module_logger
import tkinter as tk
from tkinter import messagebox
import threading
import time
import re
from view_manager import ViewManager
from controller import Controller
from task_manager import TaskManager
from definition import Definition
from util import Util
import help


logger = get_module_logger(__name__)


class Application(Util, Definition, ViewManager, Controller, TaskManager):
    def __init__(self, master, util_master, fl_master):
        super().__init__()
        self.master = master  # メイン画面マスター
        self.util_master = util_master  # 設定画面マスター
        self.fl_master = fl_master  # フォロワー画面マスター
        # 初期化
        self.define_constant()  # 各種定数を定義
        self.setup_db()  # DBに接続して設定を読み込む
        self.create_view()  # GUI作成
        # 画面位置を指定
        master.geometry(self.util_param['root_pos'])
        util_master.geometry(self.util_param['util_pos'])
        fl_master.geometry(self.util_param['fl_pos'])

        # フラグ定義
        self.login_fl = False  # 初回ログイン判定
        self.task_fl = None  # ドライバーを使用するタスクの重複を防ぐ
        self.stop_fl = False  # タスク停止フラグ
        self.timer_fl = False  # タイマーの状態
        # タスクの名前
        self.task_name = ''
        # ショートカット
        self.info = self.cf_v.info_f.info  # 確認画面info
        self.st_info = self.main_v.status_f.up_l  # メイン画面info

        # 設定画面のパラメータをロード
        self.set_util_param()

        # スタートアップ画面立ち上げ
        self.master.after(2000, threading.Thread(name='start_up', target=self.display_startup).start)
        # メインスレッドを入力待ちにする
        threading.Thread(name='update', target=self.update_widgets).start()

    # メインスレッドはここでループする
    def update_widgets(self):
        # ログイン後タスク実行待機時
        if self.login_fl and not self.task_fl:
            logger.info("update")
            # 2重タスク防止
            self.tag_v.tag_f.tag_exec_b.state(['disabled'])
            self.tl_v.tl_f.tl_exec_b.state(['disabled'])
            self.fl_v.fl_f.fl_exec_b.state(['disabled'])
            self.fl_v.fl_f.fl_deic_b.state(['disabled'])
            self.st_info['text'] = "@{}    更新中..".format(self.login_v.login_f.username.get())
            # アカウント情報更新
            threading.Thread(name='update', target=self.execute_task, args=[self.get_account_info, 'update']).start()
        # 指定時間後に再帰する
        self.master.after(int(self.util_param['account_update_interval'])*60000, self.update_widgets)

    # 設定画面のUIをパラメータに合わせる
    def set_util_param(self):
        # checkboxは作成時に変数がセットされない。また半選択状態を解除する
        if self.util_param['login_save'] == 1:
            self.util_v.util_f.login_save.set(self.util_param['login_save'])
            self.util_v.util_f.login_save_c.state(['!alternate'])  # 半選択解除
            self.util_v.util_f.login_save_c.state(['selected'])  # 選択する
        if self.util_param['auto_login'] == 1:
            self.util_v.util_f.auto_login.set(self.util_param['auto_login'])
            self.util_v.util_f.auto_login_c.state(['!alternate'])
            self.util_v.util_f.auto_login_c.state(['selected'])
        if self.util_param['display_browser'] == 1:
            self.util_v.util_f.display_browser.set(self.util_param['display_browser'])
            self.util_v.util_f.display_browser_c.state(['!alternate'])
            self.util_v.util_f.display_browser_c.state(['selected'])
        if self.util_param['retry'] == 1:
            self.util_v.util_f.retry_c.set(self.util_param['retry'])
            self.util_v.util_f.retry_c.state(['!alternate'])  # 半選択解除
            self.util_v.util_f.retry_c.state(['selected'])  # 選択する
        # 自動ログインを無効にする
        if self.util_param['login_save'] == 0:
            self.util_v.util_f.auto_login_c.state(['disabled'])

    # 表示されている全てのユーザーを選択する・解除する
    def checked_all(self, val, c_v_l):
        if val == 1:
            for i in range(len(c_v_l)):
                c_v_l[i].set(1)
        else:
            for i in range(len(c_v_l)):
                c_v_l[i].set(0)

    # ヘルプ画面のテキスト読込み
    def open_help(self):
        messagebox.showinfo('HELP', help.help_txt)

    # 停止ボタンを押した時に別スレッドで動作する
    # 作業中のタスクスレッドに停止フラグを送る
    def stopped_task(self):
        if self.task_fl:
            logger.info("execute")
            self.stop_fl = True
            self.ps_v.info_f.info.set("{}を停止しています..\nしばらくお待ちください\n".format(self.task_name))
            self.ps_v.tkraise()
            # タスクスレッドがフラグを下ろすまで待機
            while self.stop_fl:
                time.sleep(1)
            self.cf_v.tkraise()

    # 終了処理
    def quit_application(self):
        # 終了時点の行動回数を取得
        act_cnt = self.util_param['act_cnt']
        # 各種ウインドウの位置のみ取得
        root_pos = re.sub('[0-9]*x[0-9]*', '', self.master.geometry())
        util_pos = re.sub('[0-9]*x[0-9]*', '', self.util_master.geometry())
        fl_pos = re.sub('[0-9]*x[0-9]*', '', self.fl_master.geometry())
        # サイズも取得する場合
        # root_pos = self.master.geometry()

        # 保存する
        sql = "UPDATE util SET act_cnt={}, root_pos='{}', util_pos='{}', fl_pos='{}' WHERE id=1".format(act_cnt, root_pos, util_pos, fl_pos)
        self.execute_db(sql)

        # ブラウザの位置を保存
        if hasattr(self, 'bs') and self.util_param['display_browser'] == 0:
            bs_pos_d = self.bs.get_window_position()
            browser_pos = "{0[x]}-{0[y]}".format(bs_pos_d)
            sql = "UPDATE util SET browser_pos='{}' WHERE id=1".format(browser_pos)
            self.execute_db(sql)
            self.bs.close()

        # GUIを終了する
        self.master.destroy()
        logger.info("complete")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("InorganicLikes")
    root.resizable(0, 0)  # ウインドウのサイズ変更禁止
    root.withdraw()  # ウインドウを隠す
    util_master = tk.Toplevel(root)  # サブウインドウ作成
    util_master.title("設定")
    util_master.resizable(0, 0)
    util_master.withdraw()
    fl_master = tk.Toplevel(root)
    fl_master.title("フォロワーリスト")
    fl_master.resizable(0, 0)
    fl_master.withdraw()
    Application(root, util_master, fl_master)
    root.mainloop()
