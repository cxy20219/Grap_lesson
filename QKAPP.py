from pickle import TRUE
import time
import tkinter as tk
from tkinter import DISABLED, Y,ttk
import threading
import requests
# 字典
d = {
    # 时间间隔
    '2s':2,
    "1s":1,
    '0.5s':0.5,
    '0.2s':0.2,
    # 选课年份
    '2022-2023学年第一学期':"202220231",
    '2022-2023学年第二学期':"202220232",
    '2023-2024学年第一学期':"202320241",
    '2023-2024学年第二学期':"202320242",
    '2024-2025学年第一学期':"202420251",
    '2024-2025学年第二学期':"202420252",
}

#线程列表
threads = []

#不同课类别
lessons_class=["https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleTjxk&jxbid={}{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleCxcy&jxbid={}{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleTykxk&jxbid={}{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleBfakc&jxbid={}{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleKzyxk&jxbid={}{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleQxgxk&jxbid={}{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleWljx&jxbid={}{}&glJxbid=",
               ]

class QK(tk.Frame):
    def __init__(self,root_window=None):
        super().__init__(root_window)
        self.root_window = root_window
        self.pack()
        self.check_login()
    
    def check_login(self):
        self.bt_cookie  = tk.Button(self,text="cookies操作",command=self.cookie,width=40).pack(anchor = tk.CENTER,ipady=10,pady=20)
        self.bt_session = tk.Button(self,text="登陆操作",command=self.session,width=40,state=DISABLED).pack(anchor = tk.CENTER,ipady=10)
    
    def cookie(self):
        self.cookie_window = tk.Toplevel(root_window)
        self.cookie_window.title("cookies操作")
        self.cookie_window.geometry("720x550")

        # 左边布局
        left_frame = tk.Frame(self.cookie_window)
        left_frame.pack(side=tk.LEFT,padx=5,pady=5)

        # 左边布局 参数设置
        prame_frame = tk.LabelFrame(left_frame,text="参数设置",padx=5,pady=5)
        prame_frame.pack()

        tk.Label(prame_frame,text="时间间隔").pack(anchor=tk.W)

        self.times = ttk.Combobox(prame_frame)
        self.times["values"] = ['2s','1s','0.5s','0.2s']
        self.times.current(0)
        self.times.pack(anchor=tk.W)

        tk.Label(prame_frame,text="选课时间").pack(anchor=tk.W)

        self.years = ttk.Combobox(prame_frame)
        self.years["values"] = [
            '2022-2023学年第一学期','2022-2023学年第二学期','2023-2024学年第一学期',
            '2023-2024学年第二学期','2024-2025学年第一学期','2024-2025学年第二学期'
        ]
        self.years.current(0)
        self.years.pack(anchor=tk.W)

        tk.Label(prame_frame,text="cookies").pack(anchor=tk.W)

        self.entry_cookies = tk.Text(prame_frame,height=800,width=10)
        self.entry_cookies.pack(anchor=tk.W,fill=tk.X,pady=10)

        # 添加滚动条
        scroll = tk.Scrollbar(self.entry_cookies)
        scroll.pack(side=tk.RIGHT,fill=Y,ipady=30)
        # 两控件关联
        scroll.config(command=self.entry_cookies.yview)
        self.entry_cookies.config(yscrollcommand=scroll.set)




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

        #输入课程序号
        prame_classid = tk.LabelFrame(right_frame,text="课程序号")
        prame_classid.pack(anchor=tk.W)
        input_examp = tk.Text(prame_classid,height=8)
        input_examp.insert(tk.END,'相关课为:课程号+课序号 例:21210001181801\n关联实验课为：课程号+S+课序号：课程号+S+课序号 例:212100011818S01\n!!!每行请输入一门课!!!\n示例输入:\n21210001181801\n212100011818S01\n21224324324234\n21210124124141')
        input_examp.config(state=DISABLED)
        input_examp.pack(anchor=tk.W,fill=tk.X)

        tk.Label(prame_classid,text="输入").pack(anchor=tk.W)
        self.input_classid = tk.Text(prame_classid,height=15)
        self.input_classid.pack(anchor=tk.W,fill=tk.X,pady=10)
        # 添加滚动条
        scroll3 = tk.Scrollbar(self.input_classid)
        scroll3.pack(side=tk.RIGHT,fill=Y,ipady=30)
        # 两控件关联
        scroll3.config(command=self.input_classid.yview)
        self.input_classid.config(yscrollcommand=scroll3.set)

        # 右边布局 返回结果
        prame_result = tk.LabelFrame(right_frame,text="返回结果")
        prame_result.pack(anchor=tk.W)
        self.out_result = tk.Text(prame_result,height=95)
        self.out_result.pack(anchor=tk.W,fill=tk.X,pady=10,ipadx=500)

        # 添加滚动条
        scroll2 = tk.Scrollbar(self.out_result)
        scroll2.pack(side=tk.RIGHT,fill=Y,ipady=70)
        # 两控件关联
        scroll2.config(command=self.out_result.yview)
        self.out_result.config(yscrollcommand=scroll2.set)


    #抢课模块
    def grab_lessons(self,t,cookies_dict,url,id):
        #     if json_message['success'] == False:
        #         self.out_result.insert(tk.END,"\n"+json_message['message'])
        #         time.sleep(float(d[t]))
        #         self.grab_lessons(url)
        #     if json_message.get('message',None) is None:
        #         self.out_result.insert(tk.END,'\n抢课成功') 
        # except:
        #     if json_message.get('message',None) is None:
        #         self.out_result.insert(tk.END,'\n抢课成功:') 
        #     self.out_result.insert(tk.END,'\ncookies失效或服务器请求超时重新运行程序')
        try:
            r=requests.get(url,headers={"user-agent":"Mozilla/5.0"},cookies=cookies_dict,timeout=5)
            r.encoding=r.apparent_encoding
            json_message=r.json()
            r.raise_for_status()
            if json_message['success'] == False:
                self.out_result.insert(tk.END,"\n"+json_message['message']+id)
                self.out_result.update()
                time.sleep(t)
                self.grab_lessons(t,cookies_dict,url,id)
            if json_message.get('message',None) is None:
                self.out_result.insert(tk.END,'\n抢课成功'+id) 
                self.out_result.update()
        except:
            if json_message.get('message',None) is None:
                self.out_result.insert(tk.END,'\n抢课成功'+id) 
                self.out_result.update()
            self.out_result.insert(tk.END,'\ncookies失效或服务器请求超时重新运行程序')
            self.out_result.update()

    def qk(self):
        lesson_class = self.kind.get()
        year = self.years.get()
        entry_classid = self.input_classid.get("0.0","end")
        cookie = self.entry_cookies.get("0.0","end").strip()
        cookies_dict={i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}
        t = d[self.times.get()]
        for i in entry_classid.strip().split("\n"):
            url = lessons_class[lesson_class].format(d[year],i)
            thread = threading.Thread(target=self.grab_lessons,args=(t,cookies_dict,url,i))
            thread.setDaemon(True)
            thread.start()
            thread.join()
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