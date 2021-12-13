#3.0版本更新主要是提升了适用性
#适用所有抢课
#下一版本4.0版本展望：加入登录模块实现自动登录抢课,实现可选学期选课
import requests
import time
import threading
#登录模块
def login():
    cookies=input("请输入你的cookies:").strip()
    cookies_dict={i.split("=")[0]:i.split("=")[-1] for i in cookies.split("; ")}
    return cookies_dict
#不同课类别
lessons_class=["https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleTjxk&jxbid=202120222{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleCxcy&jxbid=202120222{}&glJxbid=",
               "https://xk.webvpn.scuec.edu.cn/xsxk/xkOper.xk?method=handleTykxk&jxbid=202120222{}&glJxbid="]
#进程存放
threads=[]
#抢课模块
def grab_lessons(id,lesson_class):
    #延时模块
    global delay
    url=lesson_class.format(str(id))
    try:
        r=requests.get(url,headers={"user-agent":"Mozilla/5.0"},cookies=cookies_dict,timeout=5)
        r.encoding=r.apparent_encoding
        json_message=r.json()
        r.raise_for_status()
        if json_message['success'] == False:
            print(json_message['message'])
            time.sleep(delay)
            grab_lessons(id,lesson_class)
        if json_message.get('message',None) is None:
            print('抢课成功:',id) 
    except:
        if json_message.get('message',None) is None:
            print('抢课成功:',id) 
        print('cookies失效或服务器请求超时重新运行程序')
if __name__=="__main__":
    #注意事项
    input("本程序只是个人研究使用，请勿另作他用，如使用不当造成的损失和影响与原作者无关！！！(回车继续):")
    #登录
    cookies_dict=login()
    class_id=input("1:推荐选课\n2:创新创业选课\n3:体育选课\n请输入选课类别(请输入整数数字:)：")
    lesson_class=lessons_class[int(class_id)-1]
    delay=float(input("请输入每次选课间隔(单位为:秒)(推荐0.3~0.7之间,太快使服务器崩溃后果自负):").strip())
    print('!!!有关联实验课的需要抢两门 实验课就是在课程号后面加上大S!!!')
    print('相关课为:课程号+课序号 例:21210001181801\n关联实验课为：课程号+S+课序号：课程号+S+课序号 例:212100011818S01')
    lesson_num=input("请输入想选的课程数目(只能输入整数):").strip()
    while True:
        if lesson_num.isdigit()==True:
            for i in range(int(lesson_num)):
                lesson_id=input("请输入想要选择的课程(课程号+课序号 例:21210001181801):").strip()
                threads.append(threading.Thread(target=grab_lessons,args=(lesson_id,lesson_class)))
            break
        else:
            n=input("请输入想抢的课程数目(只能输入整数):").strip(
            )
    print("=="*10+'开始选课'+'=='*10)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    input("回车退出")
