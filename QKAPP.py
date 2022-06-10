from http.cookiejar import CookiePolicy
from multiprocessing.sharedctypes import Value
from re import X
import tkinter as tk
from tkinter import Y, Scrollbar, Variable, ttk
import tkinter
from turtle import width

#不同课类别
lessons_class=["https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleTjxk&jxbid=202220231{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleCxcy&jxbid=202220231{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleTykxk&jxbid=202220231{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleBfakc&jxbid=202220231{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleKzyxk&jxbid=202220231{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleQxgxk&jxbid=202220231{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleWljx&jxbid=202220231{}&glJxbid=",
               ]

class QK(tk.Frame):
    def __init__(self,root_window=None):
        super().__init__(root_window)
        self.root_window = root_window
        self.pack()
        self.check_login()
    
    def check_login(self):
        self.bt_cookie  = tk.Button(self,text="cookies操作",command=self.cookie,width=40).pack(anchor = tk.CENTER,ipady=10,pady=20)
        self.bt_session = tk.Button(self,text="登陆操作",command=self.session,width=40).pack(anchor = tk.CENTER,ipady=10)
    
    def cookie(self):
        self.cookie_window = tk.Toplevel(root_window)
        self.cookie_window.title("cookies操作")
        self.cookie_window.geometry("700x500")

        # 左边布局
        left_frame = tk.Frame(self.cookie_window)
        left_frame.pack(side=tk.LEFT,padx=5,pady=5)

        # 左边布局 参数设置
        prame_frame = tk.LabelFrame(left_frame,text="参数设置",padx=5,pady=5)
        prame_frame.pack()

        tk.Label(prame_frame,text="时间间隔").pack(anchor=tk.W)

        times = ttk.Combobox(prame_frame)
        times["values"] = ['2s','1s','0.5s','0.2s']
        times.current(0)
        times.pack(anchor=tk.W)

        tk.Label(prame_frame,text="cookies").pack(anchor=tk.W)

        entry_cookies = tk.Text(prame_frame,height=800,width=10)
        entry_cookies.pack(anchor=tk.W,fill=tk.X,pady=10)

        # 添加滚动条
        scroll = tk.Scrollbar(entry_cookies)
        scroll.pack(side=tk.RIGHT,fill=Y,ipady=30)
        # 两控件关联
        scroll.config(command=entry_cookies.yview)
        entry_cookies.config(yscrollcommand=scroll.set)




        tk.Label(prame_frame,text="选课类别").pack(anchor=tk.W)

        # 类别按钮
        self.kind = tk.IntVar()
        self.kind.set(1)
        tk.Radiobutton(prame_frame,variable=self.kind,value=0,text="推荐选课").pack(anchor=tk.W)
        tk.Radiobutton(prame_frame,variable=self.kind,value=2,text="体育选课").pack(anchor=tk.W)
        tk.Radiobutton(prame_frame,variable=self.kind,value=1,text="创新创业选课").pack(anchor=tk.W)
        tk.Radiobutton(prame_frame,variable=self.kind,value=3,text="方案内选课").pack(anchor=tk.W)
        tk.Radiobutton(prame_frame,variable=self.kind,value=4,text="方案外选课").pack(anchor=tk.W)
        tk.Radiobutton(prame_frame,variable=self.kind,value=5,text="通识课(网络)").pack(anchor=tk.W)
        tk.Radiobutton(prame_frame,variable=self.kind,value=6,text="通识课(课堂)").pack(anchor=tk.W)

    
        tk.Button(prame_frame,text="Start",command=self.qk).pack(anchor=tk.CENTER,ipadx=30)

        # 右边布局
        right_frame = tk.Frame(self.cookie_window)
        right_frame.pack(side=tk.RIGHT,padx=5,pady=5)

        # 右边布局 返回结果
        prame_result = tk.LabelFrame(right_frame,text="返回结果")
        prame_result.pack(anchor=tk.W)
        out_result = tk.Text(prame_result)
        out_result.pack(anchor=tk.W,fill=tk.X,pady=10,ipadx=500)

        # 添加滚动条
        scroll2 = tk.Scrollbar(out_result)
        scroll2.pack(side=tk.RIGHT,fill=Y,ipady=190)
        # 两控件关联
        scroll2.config(command=out_result.yview)
        out_result.config(yscrollcommand=scroll2.set)

    def qk(self):
        s = self.kind.get()
        print(s)

    def session(self):
        self.session_window = tk.Toplevel(root_window)
        self.session_window.title("登陆操作")
        self.session_window.geometry("700x500")

if __name__ == "__main__":
    root_window = tk.Tk()
    root_window.title("选课助手 v0.0.1")
    root_window.geometry("400x200+300+300")
    qk = QK(root_window)

    root_window.mainloop()